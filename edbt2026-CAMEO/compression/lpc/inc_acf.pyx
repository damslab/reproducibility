# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
import numpy as np
cimport numpy as np
from libc.stdlib cimport malloc, free
from libc.math cimport sqrt, fabs
from compression.lpc cimport math_utils
cimport cython


cdef void initialize(AcfPtr model, Py_ssize_t nlags):
    model.sxy = <double*> malloc(nlags * sizeof(double))
    model.xs = <double*> malloc(nlags * sizeof(double))
    model.ys = <double*> malloc(nlags * sizeof(double))
    model.xss = <double*> malloc(nlags * sizeof(double))
    model.yss = <double*> malloc(nlags * sizeof(double))
    model.nlags = nlags


cdef void fit(AcfPtr model, double[:] x):
    cdef Py_ssize_t n = x.shape[0], lag
    cdef double[:] x_cum_sum = np.empty_like(x)
    cdef double[:] power_cum_sum = np.empty_like(x)
    math_utils.cumsum_cumsum(x, x_cum_sum, power_cum_sum)
    model.n = n

    for lag in range(model.nlags):
        model.xs[lag] = x_cum_sum[n-lag-2]
        model.ys[lag] = x_cum_sum[n-1] - x_cum_sum[lag]
        model.xss[lag] = power_cum_sum[n-lag-2]
        model.yss[lag] = power_cum_sum[n-1] - power_cum_sum[lag]
        model.sxy[lag] = math_utils.dot_product(x[:n-lag-1], x[lag+1:])


@cython.cdivision(True)
cdef void get_acf(AcfPtr model, double* result):
    cdef Py_ssize_t lag, n = model.n

    for lag in range(model.nlags):
        n -= 1
        result[lag] = (n*model.sxy[lag] - model.xs[lag]*model.ys[lag])/\
                      sqrt((n*model.xss[lag] - model.xs[lag]*model.xs[lag])*
                           (n*model.yss[lag] - model.ys[lag]*model.ys[lag]))


@cython.cdivision(True)
cdef void update(AcfPtr model, double[:] x, const double x_a, const Py_ssize_t index):
    cdef double delta, delta_ss
    delta = x_a - x[index]
    delta_ss = delta * (2 * x[index] + delta)
    if delta != 0:
        if index <= model.nlags or index >= model.n-model.nlags:
            update_inside_lags(model, x, delta, delta_ss, index)
        else:
            update_outside_lags(model, x, delta, delta_ss, index)

        x[index] = x_a


@cython.cdivision(True)
cdef double look_ahead_impact(AcfPtr model, double[:] x, double *raw_acf, const double x_a, const Py_ssize_t index) nogil:
    cdef double delta, delta_ss, ys, yss, xs, xss, sxy, lag_acf, impact = 0.0
    cdef Py_ssize_t lag, n = model.n-1
    delta = x_a - x[index]
    delta_ss = delta * (2 * x[index] + delta)
    if delta != 0:
        if index <= model.nlags or index >= model.n-model.nlags:
            for lag in range(model.nlags):
                ys = model.ys[lag]
                yss = model.yss[lag]
                xs = model.xs[lag]
                xss = model.xss[lag]
                sxy = model.sxy[lag]
                if index >= lag + 1:
                    ys = ys + delta
                    yss = yss + delta_ss
                    sxy = sxy + delta * x[index - lag - 1]
                if index < n:
                    xs = xs + delta
                    xss = xss + delta_ss
                    sxy = sxy + delta * x[index + lag + 1]
                lag_acf = (n * sxy - xs * ys) / sqrt((n * xss - xs * xs) * (n * yss - ys * ys))
                impact += fabs(lag_acf - raw_acf[lag])
                n = n - 1
        else:
            for lag in range(model.nlags):
                ys = model.ys[lag] + delta
                yss = model.yss[lag] + delta_ss
                xs = model.xs[lag] + delta
                xss = model.xss[lag] + delta_ss
                sxy = model.sxy[lag] + delta * (x[index + lag + 1] + x[index - lag - 1])
                lag_acf = (n * sxy - xs * ys) / sqrt((n * xss - xs * xs) * (n * yss - ys * ys))
                impact += fabs(lag_acf - raw_acf[lag])
                n = n - 1

    return impact/model.nlags


cdef inline void update_inside_lags(AcfPtr model, double[:] x,
                                    const double delta,
                                    const double delta_ss,
                                    const Py_ssize_t index):
    cdef Py_ssize_t lag, n = model.n - 1
    for lag in range(model.nlags):
        if index >= lag+1:
            model.ys[lag] += delta
            model.yss[lag] += delta_ss
            model.sxy[lag] += delta*x[index - lag - 1]
        if index < n-lag:
            model.xs[lag] += delta
            model.xss[lag] += delta_ss
            model.sxy[lag] += delta*x[index + lag + 1]


cdef inline void update_outside_lags(AcfPtr model, double[:] x,
                                     const double delta,
                                     const double delta_ss,
                                     const Py_ssize_t index):
    cdef Py_ssize_t lag
    for lag in range(model.nlags):
        model.ys[lag] += delta
        model.yss[lag] += delta_ss
        model.xs[lag] += delta
        model.xss[lag] += delta_ss
        model.sxy[lag] += delta * (x[index + lag + 1] + x[index-lag-1])


cdef void interpolate_update(AcfPtr model, double[:] x, Py_ssize_t start, Py_ssize_t end):
    if start <= model.nlags or end >= model.n-model.nlags:
        interpolate_update_inside_lags(model, x, start, end)
    else:
        interpolate_update_outside_lags(model, x, start, end)

@cython.cdivision(True)

cdef void interpolate_update_outside_lags(AcfPtr model, double[:] x, Py_ssize_t start, Py_ssize_t end):
    cdef double delta, delta_ss, slope
    cdef Py_ssize_t i, index, lag, num_lags, num_deltas
    cdef double *deltas
    cdef double *x_as
    num_deltas = (end-start-1)
    slope = (x[end] - x[start]) / (end - start)
    deltas = <double*> malloc(num_deltas*sizeof(double))
    x_as = <double*> malloc(num_deltas*sizeof(double))

    i = 0
    for index in range(start+1, end):
        x_as[i] = slope * (index - start) + x[start]
        delta = x_as[i] - x[index]
        deltas[i] = delta

        delta_ss = delta * (delta + 2 * x[index])
        for lag in range(model.nlags):
            model.xs[lag] += delta
            model.ys[lag] += delta
            model.yss[lag] += delta_ss
            model.xss[lag] += delta_ss
            model.sxy[lag] += delta * (x[index - lag - 1] + x[index + lag + 1])

        i += 1

    num_lags = num_deltas if num_deltas < model.nlags else model.nlags

    for lag in range(num_lags):
        for i in range(num_deltas - lag - 1):
            model.sxy[lag] += deltas[i] * deltas[i + lag + 1]

    i = 0
    for index in range(start + 1, end):
        x[index] = x_as[i]
        i += 1

    free(deltas)
    free(x_as)

@cython.cdivision(True)

cdef void interpolate_update_inside_lags(AcfPtr model, double[:] x, Py_ssize_t start, Py_ssize_t end):
    cdef double delta, delta_ss, slope
    cdef Py_ssize_t i, index, lag, num_lags, num_deltas, n
    cdef double *deltas
    cdef double *x_as
    num_deltas = (end - start - 1)
    slope = (x[end] - x[start]) / (end - start)
    deltas = <double *> malloc(num_deltas * sizeof(double))
    x_as = <double *> malloc(num_deltas * sizeof(double))
    i = 0
    n = model.n - 1
    for index in range(start + 1, end):
        x_as[i] = slope * (index - start) + x[start]
        delta = x_as[i] - x[index]
        deltas[i] = delta

        delta_ss = delta * (delta + 2 * x[index])
        for lag in range(model.nlags):
            if index >= lag + 1:
                model.ys[lag] += delta
                model.yss[lag] += delta_ss
                model.sxy[lag] += delta * x[index - lag - 1]
            if index < n - lag:
                model.xs[lag] += delta
                model.xss[lag] += delta_ss
                model.sxy[lag] += delta * x[index + lag + 1]

        i += 1

    num_lags = num_deltas if num_deltas < model.nlags else model.nlags

    for lag in range(num_lags):
        for i in range(num_deltas - lag - 1):
            model.sxy[lag] += deltas[i] * deltas[i + lag + 1]

    i = 0
    for index in range(start + 1, end):
        x[index] = x_as[i]
        i += 1

    free(deltas)
    free(x_as)


@cython.cdivision(True)

cdef double look_ahead_interpolated_impact(AcfPtr model, double[:] x, double *raw_acf, Py_ssize_t start, Py_ssize_t end) nogil:
    cdef double delta, delta_ss, slope, impact, lag_acf
    cdef Py_ssize_t i, index, lag, num_deltas, n # num_lags
    cdef double * deltas
    cdef double * sxy
    cdef double * ys
    cdef double * yss
    cdef double * xs
    cdef double * xss

    num_deltas = (end - start - 1)
    slope = (x[end] - x[start]) / (end - start)

    deltas = <double *> malloc(num_deltas * sizeof(double))
    sxy = <double *> malloc(model.nlags * sizeof(double))
    ys = <double *> malloc(model.nlags * sizeof(double))
    yss = <double *> malloc(model.nlags * sizeof(double))
    xss = <double *> malloc(model.nlags * sizeof(double))
    xs = <double *> malloc(model.nlags * sizeof(double))

    for lag in range(model.nlags):
        ys[lag] = model.ys[lag]
        yss[lag] = model.yss[lag]
        sxy[lag] = model.sxy[lag]
        xs[lag] = model.xs[lag]
        xss[lag] = model.xss[lag]

    i = 0
    n = model.n - 1
    for index in range(start + 1, end):
        delta = slope * (index - start) + x[start] - x[index]
        deltas[i] = delta
        delta_ss = delta * (delta + 2 * x[index])
        for lag in range(model.nlags):
            if index >= lag + 1:
                ys[lag] += delta
                yss[lag] += delta_ss
                sxy[lag] += delta * x[index - lag - 1]
            if index < n - lag:
                xs[lag] += delta
                xss[lag] += delta_ss
                sxy[lag] += delta * x[index + lag + 1]

        i += 1

    impact = 0
    n = model.n - 1
    for lag in range(model.nlags):
        for i in range(num_deltas - lag - 1):
            sxy[lag] += deltas[i] * deltas[i + lag + 1]
        lag_acf = (n * sxy[lag] - xs[lag] * ys[lag]) / sqrt(
            (n * xss[lag] - xs[lag] * xs[lag]) * (n * yss[lag] - ys[lag] * ys[lag]))
        impact += fabs(lag_acf - raw_acf[lag])
        n -= 1

    free(deltas)
    free(sxy)
    free(ys)
    free(yss)
    free(xss)
    free(xs)
    return impact/model.nlags


cdef void release_memory(AcfPtr model):
    free(model.sxy)
    free(model.ys)
    free(model.xs)
    free(model.xss)
    free(model.yss)
    free(model)