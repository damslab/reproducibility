# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
cimport cython
from libc.math cimport fabs, sqrt
from cython.parallel cimport prange, parallel
from libc.stdlib cimport malloc, free, abort
from compression.lpc.inc_acf cimport AcfAgg
from numpy.math cimport INFINITY

cdef double csum(double[:] x, Py_ssize_t n):
    cdef:
        Py_ssize_t i
        double result = 0.0

    for i in range(n):
        result += x[i]

    return result

cdef double dot_product(double[:] x, double[:] y):
    cdef:
        Py_ssize_t i, n = x.shape[0]
        double result = 0.0

    for i in range(n):
        result += x[i] * y[i]

    return result


cdef void scan(double[:] x, double[:] out1, double[:] out2) noexcept nogil:
    cdef:
        Py_ssize_t i, n = x.shape[0]

    out1[0] = x[0]
    out2[0] = x[0]*x[0]
    for i in range(1, n):
        out1[i] = out1[i-1] + x[i]
        out2[i] = out2[i-1] + x[i]*x[i]


cdef void cumsum_cumsum(double[:] arr, double[:] cumsum1, double[:] cumsum2):
    cdef:
        Py_ssize_t n = arr.shape[0]
        Py_ssize_t num_threads = 8
        double* sums1 = <double*> malloc(num_threads * sizeof(double))
        double* sums2 = <double*> malloc(num_threads * sizeof(double))
        Py_ssize_t chunk_size = n // num_threads
        Py_ssize_t tid, start, end, i

    for tid in prange(num_threads, nogil=True, num_threads=num_threads, schedule='static'):
        start = tid * chunk_size
        end = start + chunk_size if tid != num_threads - 1 else n
        scan(arr[start:end], cumsum1[start:end], cumsum2[start:end])

    sums1[0] = cumsum1[chunk_size - 1]
    sums2[0] = cumsum2[chunk_size - 1]

    for i in range(1, num_threads - 1):
        sums1[i] = sums1[i - 1] + cumsum1[(i+1) * chunk_size - 1]
        sums2[i] = sums2[i - 1] + cumsum2[(i+1) * chunk_size - 1]


    for tid in prange(1, num_threads, nogil=True, num_threads=num_threads, schedule='static'):
        start = tid * chunk_size
        end = start + chunk_size if tid != num_threads - 1 else n
        for i in range(start, end):
            cumsum1[i] += sums1[tid - 1]
            cumsum2[i] += sums2[tid - 1]

    free(sums1)
    free(sums2)


cdef double no_gil_mae(double *x, double *y, Py_ssize_t n) noexcept nogil:
    cdef:
        double error_sum = 0.0
        Py_ssize_t i

    for i in range(n):
        error_sum += fabs(x[i] - y[i])

    return error_sum / n


cdef double mae(double *x, double *y, Py_ssize_t n):
    cdef:
        double error_sum = 0.0
        Py_ssize_t i

    for i in range(n):
        error_sum += fabs(x[i] - y[i])

    return error_sum / n


cdef double triangle_area(const double &x_p1, const double &y_p1,
                                 const double &x_p2, const double &y_p2,
                                 const double &x_p3, const double &y_p3):

    return fabs(x_p1 * (y_p2 - y_p3) + x_p2 * (y_p3 - y_p1) + x_p3 * (y_p1 - y_p2)) / 2.


cdef double mean(double[:] x):
    cdef Py_ssize_t i, n = x.shape[0]
    cdef double mu = 0

    for i in prange(n, nogil=True):
        mu += x[i]

    return mu/n


cdef double std(double[:] x, const double & mu):
    cdef Py_ssize_t i, n = x.shape[0]
    cdef double sigma = 0

    for i in prange(n, nogil=True):
        sigma += (x[i] - mu)*(x[i] - mu)

    return sigma/(n-1)



cdef double corrcoef(double[:] x, double[:] y):
    cdef double mean_x, mean_y, rho_num = 0, rho_dem_x = 0, rho_dem_y = 0
    cdef Py_ssize_t i

    mean_x = mean(x)
    mean_y = mean(y)

    for i in prange(x.shape[0], nogil=True):
        rho_num += (x[i]-mean_x)*(y[i]-mean_y)
        rho_dem_x += (x[i] - mean_x)*(x[i] - mean_x)
        rho_dem_y += (y[i] - mean_y)*(y[i] - mean_y)

    return rho_num/sqrt(rho_dem_x*rho_dem_y)



cdef void compute_acf_fall(AcfAgg *model, double[:] x, double * raw_acf, double * acf_error) noexcept nogil:
    cdef double delta, delta_ss, ys, yss, xs, xss, sxy
    cdef double * c_acf
    cdef Py_ssize_t index, lag, n
    acf_error[0] = acf_error[model.n-1] = INFINITY

    with nogil, parallel(num_threads=8):
        c_acf = <double *> malloc(model.nlags * sizeof(double))

        if c_acf is NULL:
            abort()

        for index in prange(1, model.n-1, schedule='static'):
            delta = (x[index-1] + x[index+1]) * 0.5 - x[index]
            delta_ss = delta * (delta + 2*x[index])
            n = model.n - 1
            if model.nlags <= index < model.n - model.nlags:
                # compute_pw_acf_outside_lags
                for lag in range(model.nlags):
                    ys = model.ys[lag] + delta
                    yss = model.yss[lag] + delta_ss
                    xs = model.xs[lag] + delta
                    xss = model.xss[lag] + delta_ss
                    sxy = model.sxy[lag] + delta * (x[index-lag-1] + x[index+lag+1])
                    c_acf[lag] = (n * sxy - xs * ys) / sqrt((n * xss - xs * xs) * (n * yss - ys * ys))
                    n = n - 1

            elif index < model.nlags:
                # compute_pw_acf_bellow_lower_lags
                for lag in range(model.nlags):
                    xs = model.xs[lag] + delta
                    xss = model.xss[lag] + delta_ss
                    sxy = model.sxy[lag] + delta * x[index + lag + 1]
                    ys = model.ys[lag]
                    yss = model.yss[lag]
                    if index >= lag + 1:
                        ys = ys + delta
                        yss = yss + delta_ss
                        sxy = sxy + delta * x[index - lag - 1]
                    c_acf[lag] = (n * sxy - xs * ys) / sqrt((n * xss - xs * xs) * (n * yss - ys * ys))
                    n = n - 1
            else:
                # compute_pw_acf_above_upper_lags
                for lag in range(model.nlags):
                    ys = model.ys[lag] + delta
                    yss = model.yss[lag] + delta_ss
                    sxy = model.sxy[lag] + delta * x[index - lag - 1] # + (delta * x[index + lag + 1]) if index + lag + 1 < model.n else 0
                    xs = model.xs[lag] # + delta if index + lag + 1 < model.n else 0
                    xss = model.xss[lag] # + delta_ss if index + lag + 1 < model.n else 0
                    if index < n:
                        xs = xs + delta
                        xss = xss + delta_ss
                        sxy = sxy + delta * x[index + lag + 1]

                    c_acf[lag] = (n * sxy - xs * ys) / sqrt((n * xss - xs * xs) * (n * yss - ys * ys))
                    n = n - 1

            acf_error[index] = no_gil_mae(raw_acf, c_acf, model.nlags)

        free(c_acf)


cdef void compute_acf_agg_mean_fall(AcfAgg *model, double [:]x, double [:]aggregates,
                               double *raw_acf, double *acf_error, Py_ssize_t x_n, Py_ssize_t kappa) noexcept nogil:
    cdef double delta, delta_ss, ys, yss, xs, xss, sxy
    cdef double *c_acf
    cdef Py_ssize_t index, lag, n, agg_index
    acf_error[0] = acf_error[x_n-1] = INFINITY

    with nogil, parallel():
        c_acf = <double *> malloc(model.nlags * sizeof(double))

        if c_acf is NULL:
            abort()

        for index in prange(1, x_n-1, schedule='static'):
            delta = ((x[index-1] + x[index+1]) * 0.5 - x[index])/kappa
            agg_index = index // kappa
            delta_ss = delta * (2 * aggregates[agg_index] + delta)
            n = model.n - 1
            if model.nlags <= agg_index < model.n - model.nlags:
                # compute_pw_acf_outside_lags
                for lag in range(model.nlags):
                    ys = model.ys[lag] + delta
                    yss = model.yss[lag] + delta_ss
                    xs = model.xs[lag] + delta
                    xss = model.xss[lag] + delta_ss
                    sxy = model.sxy[lag] + delta * (aggregates[agg_index + lag + 1] + aggregates[agg_index-lag-1])
                    c_acf[lag] = (n * sxy - xs * ys) / sqrt((n * xss - xs * xs) * (n * yss - ys * ys))
                    n = n - 1

            elif agg_index < model.nlags:
                # compute_pw_acf_bellow_lower_lags
                for lag in range(model.nlags):
                    xs = model.xs[lag] + delta
                    xss = model.xss[lag] + delta_ss
                    sxy = model.sxy[lag] + delta * aggregates[agg_index + lag + 1]
                    ys = model.ys[lag]
                    yss = model.yss[lag]
                    if agg_index >= lag + 1:
                        ys = ys + delta
                        yss = yss + delta_ss
                        sxy = sxy + delta * aggregates[agg_index-lag-1]
                    c_acf[lag] = (n * sxy - xs * ys) / sqrt((n * xss - xs * xs) * (n * yss - ys * ys))
                    n = n - 1
            else:
                # compute_pw_acf_above_upper_lags
                for lag in range(model.nlags):
                    ys = model.ys[lag] + delta
                    yss = model.yss[lag] + delta_ss
                    sxy = model.sxy[lag] + delta * aggregates[agg_index-lag-1] # + (delta * x[index + lag + 1]) if index + lag + 1 < model.n else 0
                    xs = model.xs[lag] # + delta if index + lag + 1 < model.n else 0
                    xss = model.xss[lag] # + delta_ss if index + lag + 1 < model.n else 0
                    if agg_index < n:
                        xs = xs + delta
                        xss = xss + delta_ss
                        sxy = sxy + delta * aggregates[agg_index + lag + 1]

                    c_acf[lag] = (n * sxy - xs * ys) / sqrt((n * xss - xs * xs) * (n * yss - ys * ys))
                    n = n - 1

            acf_error[index] = no_gil_mae(raw_acf, c_acf, model.nlags)

        free(c_acf)


cdef void compute_acf_agg_sum_fall(AcfAgg *model, double [:]x, double [:]aggregates,
                               double *raw_acf, double *acf_error, Py_ssize_t x_n, Py_ssize_t kappa) noexcept nogil:
    cdef double delta, delta_ss, ys, yss, xs, xss, sxy
    cdef double *c_acf
    cdef Py_ssize_t index, lag, n, agg_index
    acf_error[0] = acf_error[x_n-1] = INFINITY

    with nogil, parallel():
        c_acf = <double *> malloc(model.nlags * sizeof(double))

        if c_acf is NULL:
            abort()

        for index in prange(1, x_n-1, schedule='static'):
            delta = ((x[index-1] + x[index+1]) * 0.5 - x[index])
            agg_index = index // kappa
            delta_ss = delta * (2 * aggregates[agg_index] + delta)
            n = model.n - 1
            if model.nlags <= agg_index < model.n - model.nlags:
                # compute_pw_acf_outside_lags
                for lag in range(model.nlags):
                    ys = model.ys[lag] + delta
                    yss = model.yss[lag] + delta_ss
                    xs = model.xs[lag] + delta
                    xss = model.xss[lag] + delta_ss
                    sxy = model.sxy[lag] + delta * (aggregates[agg_index + lag + 1] + aggregates[agg_index-lag-1])
                    c_acf[lag] = (n * sxy - xs * ys) / sqrt((n * xss - xs * xs) * (n * yss - ys * ys))
                    n = n - 1

            elif agg_index < model.nlags:
                # compute_pw_acf_bellow_lower_lags
                for lag in range(model.nlags):
                    xs = model.xs[lag] + delta
                    xss = model.xss[lag] + delta_ss
                    sxy = model.sxy[lag] + delta * aggregates[agg_index + lag + 1]
                    ys = model.ys[lag]
                    yss = model.yss[lag]
                    if agg_index >= lag + 1:
                        ys = ys + delta
                        yss = yss + delta_ss
                        sxy = sxy + delta * aggregates[agg_index-lag-1]
                    c_acf[lag] = (n * sxy - xs * ys) / sqrt((n * xss - xs * xs) * (n * yss - ys * ys))
                    n = n - 1
            else:
                # compute_pw_acf_above_upper_lags
                for lag in range(model.nlags):
                    ys = model.ys[lag] + delta
                    yss = model.yss[lag] + delta_ss
                    sxy = model.sxy[lag] + delta * aggregates[agg_index-lag-1] # + (delta * x[index + lag + 1]) if index + lag + 1 < model.n else 0
                    xs = model.xs[lag] # + delta if index + lag + 1 < model.n else 0
                    xss = model.xss[lag] # + delta_ss if index + lag + 1 < model.n else 0
                    if agg_index < n:
                        xs = xs + delta
                        xss = xss + delta_ss
                        sxy = sxy + delta * aggregates[agg_index + lag + 1]

                    c_acf[lag] = (n * sxy - xs * ys) / sqrt((n * xss - xs * xs) * (n * yss - ys * ys))
                    n = n - 1

            acf_error[index] = no_gil_mae(raw_acf, c_acf, model.nlags)

        free(c_acf)


