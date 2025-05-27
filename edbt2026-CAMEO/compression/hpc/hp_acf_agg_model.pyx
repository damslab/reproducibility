# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
import numpy as np
cimport numpy as np
from libc.stdlib cimport malloc, free
from libc.stdio cimport printf
from compression.hpc cimport hp_math_lib
from compression.hpc.hp_acf_agg_model cimport AcfPtr
from numpy.math cimport INFINITY
from libc.math cimport fabsl, sqrtl
cimport cython

np.import_array()

cdef void initialize(AcfPtr model, Py_ssize_t nlags):
    model.sxy = <long double*> malloc(nlags * sizeof(long double))
    model.xs = <long double*> malloc(nlags * sizeof(long double))
    model.ys = <long double*> malloc(nlags * sizeof(long double))
    model.xss = <long double*> malloc(nlags * sizeof(long double))
    model.yss = <long double*> malloc(nlags * sizeof(long double))
    model.nlags = nlags


cdef void fit(AcfPtr model, double[:] x, long double [:] aggregates, Py_ssize_t kappa):
    cdef Py_ssize_t n = x.shape[0], an=aggregates.shape[0], lag, i, j
    cdef long double[:] cum_sum = np.empty_like(aggregates, dtype=np.longdouble)
    cdef long double[:] power_cum_sum = np.empty_like(aggregates, dtype=np.longdouble)

    j = 0
    i = 0
    while i < n-kappa+1:
        aggregates[j] = hp_math_lib.csum(x[i:i+kappa], kappa)/kappa # aggregate function
        j += 1
        i += kappa

    if j == an-1:
        aggregates[j] = hp_math_lib.csum(x[i:n], n-i)/(n-i)

    hp_math_lib.cumsum_cumsum(aggregates, cum_sum, power_cum_sum)
    model.n = an

    for lag in range(model.nlags):
        model.xs[lag] = cum_sum[an - lag - 2]
        model.ys[lag] = cum_sum[an - 1] - cum_sum[lag]
        model.xss[lag] = power_cum_sum[an - lag - 2]
        model.yss[lag] = power_cum_sum[an - 1] - power_cum_sum[lag]
        model.sxy[lag] = hp_math_lib.dot_product(aggregates[:an - lag - 1], aggregates[lag + 1:])

cdef void update(AcfPtr model, double[:] x, long double[:] aggregates, long double x_a, Py_ssize_t index, Py_ssize_t kappa):
    cdef Py_ssize_t agg_index = index//kappa
    cdef long double delta, delta_ss
    delta = (x_a - x[index])/kappa # aggregate function
    delta_ss = delta * (2 * aggregates[agg_index] + delta)
    if delta != 0:
        if agg_index <= model.nlags or agg_index >= model.n-model.nlags:
            update_inside_lags(model, aggregates, delta, delta_ss, agg_index)
        else:
            update_outside_lags(model, aggregates, delta, delta_ss, agg_index)

        x[index] = x_a
        aggregates[agg_index] += delta


cdef void get_acf(AcfPtr model, long double * result):
    cdef Py_ssize_t lag, n = model.n

    for lag in range(model.nlags):
        n -= 1
        result[lag] = (n*model.sxy[lag] - model.xs[lag]*model.ys[lag])/\
                      sqrtl((n*model.xss[lag] - model.xs[lag]*model.xs[lag])*
                           (n*model.yss[lag] - model.ys[lag]*model.ys[lag]))

cdef inline void update_inside_lags(AcfPtr model, 
                                    long double[:] aggregates,
                                    long double delta,
                                    long double delta_ss,
                                    Py_ssize_t index_a):
    cdef Py_ssize_t lag, n = model.n - 1
    for lag in range(model.nlags):
        if index_a >= lag+1:
            model.ys[lag] += delta
            model.yss[lag] += delta_ss
            model.sxy[lag] += delta*aggregates[index_a - lag - 1]
        if index_a < n-lag:
            model.xs[lag] += delta
            model.xss[lag] += delta_ss
            model.sxy[lag] += delta*aggregates[index_a + lag + 1]


cdef inline void update_outside_lags(AcfPtr model, 
                                    long double[:] aggregates,
                                    long double delta,
                                    long double delta_ss,
                                    Py_ssize_t index_a):
    cdef Py_ssize_t lag
    for lag in range(model.nlags):
        model.ys[lag] += delta
        model.yss[lag] += delta_ss
        model.xs[lag] += delta
        model.xss[lag] += delta_ss
        model.sxy[lag] += delta * (aggregates[index_a + lag + 1] + aggregates[index_a-lag-1])


cdef void interpolate_update(AcfPtr model, double[:] x, 
                                long double[:] aggregates, 
                                Py_ssize_t start, Py_ssize_t end, 
                                Py_ssize_t kappa):

    cdef Py_ssize_t start_index_a = (start+1) // kappa
    cdef Py_ssize_t end_index_a = (end-1) // kappa

    if start_index_a <= model.nlags or end_index_a >= model.n-model.nlags:
        interpolate_update_inside_lags(model, x, aggregates, start, end, start_index_a, end_index_a, kappa)
    else:
        interpolate_update_outside_lags(model, x, aggregates, start, end, start_index_a, end_index_a, kappa)


cdef void interpolate_update_outside_lags(AcfPtr model, 
                                            double[:] x, long double[:] aggregates,
                                            Py_ssize_t start, Py_ssize_t end, 
                                            Py_ssize_t start_index_a,
                                            Py_ssize_t end_index_a, Py_ssize_t kappa):
    cdef Py_ssize_t i, index, lag, num_agg_deltas, agg_index, j
    cdef long double delta, delta_ss, slope, x_a
    cdef long double * sum_agg_deltas

    num_agg_deltas = end_index_a-start_index_a+1
    slope = (x[end] - x[start]) / (end - start)
    sum_agg_deltas = <long double*> malloc(num_agg_deltas*sizeof(long double))

    for i in range(num_agg_deltas):
        sum_agg_deltas[i] = 0.0

    for index in range(start+1, end):
        x_a = slope * (index - start) + x[start]
        agg_index = index//kappa
        i = agg_index - start_index_a
        sum_agg_deltas[i] += (x_a - x[index])
        x[index] = x_a

    i = 0
    for agg_index in range(start_index_a, end_index_a+1):
        sum_agg_deltas[i] /= kappa # aggregate function
        delta = sum_agg_deltas[i]
        delta_ss = delta * (delta + 2 * aggregates[agg_index])
        for lag in range(model.nlags):
            model.xs[lag] += delta
            model.ys[lag] += delta
            model.yss[lag] += delta_ss
            model.xss[lag] += delta_ss
            model.sxy[lag] += delta * (aggregates[agg_index - lag - 1] + aggregates[agg_index + lag + 1])
        i += 1

    num_lags = num_agg_deltas if num_agg_deltas < model.nlags else model.nlags

    for lag in range(num_lags):
        for i in range(num_agg_deltas - lag - 1):
            model.sxy[lag] += sum_agg_deltas[i] * sum_agg_deltas[i + lag + 1]

    i = 0
    for index in range(start_index_a, end_index_a+1):
        aggregates[index] += sum_agg_deltas[i]
        i += 1

    free(sum_agg_deltas)


cdef void interpolate_update_inside_lags(AcfPtr model, double[:] x, 
                                            long double[:] aggregates, Py_ssize_t start, Py_ssize_t end, Py_ssize_t start_index_a,
                                            Py_ssize_t end_index_a, Py_ssize_t kappa):
    cdef long double delta, delta_ss, slope, x_a
    cdef Py_ssize_t i, index, lag, num_agg_deltas, agg_index, j, n = model.n - 1
    cdef long double *sum_agg_deltas
    
    num_agg_deltas = end_index_a-start_index_a+1
    slope = (x[end] - x[start]) / (end - start)
    sum_agg_deltas = <long double*> malloc(num_agg_deltas*sizeof(long double))

    for i in range(num_agg_deltas):
        sum_agg_deltas[i] = 0.0

    for index in range(start+1, end):
        x_a = slope * (index - start) + x[start]
        agg_index = index//kappa
        i = agg_index - start_index_a
        sum_agg_deltas[i] += (x_a - x[index])
        x[index] = x_a

    i = 0
    for agg_index in range(start_index_a, end_index_a+1):
        sum_agg_deltas[i] /= kappa # aggregate function
        delta = sum_agg_deltas[i]
        delta_ss = delta * (delta + 2 * aggregates[agg_index])
        for lag in range(model.nlags):
            if agg_index > lag:
                model.ys[lag] += delta
                model.yss[lag] += delta_ss
                model.sxy[lag] += delta * aggregates[agg_index - lag - 1]
            if agg_index < n - lag:
                model.xs[lag] += delta
                model.xss[lag] += delta_ss
                model.sxy[lag] += delta * aggregates[agg_index + lag + 1]
        i += 1

    num_lags = num_agg_deltas if num_agg_deltas < model.nlags else model.nlags

    for lag in range(num_lags):
        for i in range(num_agg_deltas - lag - 1):
            model.sxy[lag] += sum_agg_deltas[i] * sum_agg_deltas[i + lag + 1]

    i = 0
    for index in range(start_index_a, end_index_a+1):
        aggregates[index] += sum_agg_deltas[i]
        i += 1

    free(sum_agg_deltas)


cdef void release_memory(AcfPtr model):
    free(model.sxy)
    free(model.ys)
    free(model.xs)
    free(model.xss)
    free(model.yss)
    free(model)