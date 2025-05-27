# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
from compression.hpc cimport hp_acf_agg_model
from compression.hpc cimport hp_heap 
from compression.hpc cimport hp_math_lib
from compression.hpc.hp_acf_agg_model cimport HPAcfAgg
from compression.hpc.hp_heap cimport HPHeap, HPNode
from libcpp.unordered_map cimport unordered_map
from cython.parallel cimport prange, parallel
from numpy.math cimport INFINITY
from libc.stdlib cimport malloc, free
from libc.math cimport sqrtl, fabsl
import numpy as np
cimport numpy as np


cdef void parallel_look_ahead_reheap(HPAcfAgg *acf_model, 
                                        HPHeap *acf_errors, 
                                        unordered_map[Py_ssize_t, Py_ssize_t] &map_node_to_heap,
                                        double[:] ts, 
                                        long double[:] aggregates, 
                                        long double *raw_acf,
                                        HPNode &removed_node, 
                                        Py_ssize_t hops, 
                                        Py_ssize_t kappa, 
                                        Py_ssize_t num_threads):
    cdef: # Private var
        Py_ssize_t i, ii, index, lag, end, n, num_deltas, num_lags, start
        Py_ssize_t end_index_a, start_index_a, agg_index, num_agg_deltas, diff
        long double delta, delta_ss, x_a, lag_acf, slope
        long double sxy, xs, xss, ys, yss
        HPNode neighbor_node
    cdef:
        Py_ssize_t real_size, max_nd
        Py_ssize_t left_node_index, right_node_index
        Py_ssize_t N = ts.shape[0], NAGG = aggregates.shape[0]
        HPNode left_node, right_node
        HPNode * neighbors = <HPNode *> malloc(2 * hops * sizeof(HPNode))
        long double *nb_imp = <long double *> malloc(2 * hops * sizeof(long double))
        long double *sum_agg_deltas
        long double *sxy_s
        long double *ys_s
        long double *yss_s
        long double *xs_s
        long double *xss_s

    real_size = 0
    left_node_index = removed_node.left
    right_node_index = removed_node.right

    # Look for neighbor nodes left and right and store them
    max_nd = 2
    for i in range(hops):
        if left_node_index > 0:
            left_node = acf_errors.values[map_node_to_heap[left_node_index]]
            neighbors[real_size] = left_node
            left_node_index = left_node.left
            diff = left_node.right//kappa - left_node_index//kappa + 1
            if diff > max_nd:
                max_nd = diff + 1
            real_size += 1
        if right_node_index < N - 1:
            right_node = acf_errors.values[map_node_to_heap[right_node_index]]
            neighbors[real_size] = right_node
            right_node_index = right_node.right
            diff = right_node_index//kappa - right_node.left//kappa + 1
            if diff > max_nd:
                max_nd = diff + 1
            real_size += 1

    with nogil, parallel(num_threads=num_threads):
        sxy_s = <long double *> malloc(acf_model.nlags * sizeof(long double))
        ys_s = <long double *> malloc(acf_model.nlags * sizeof(long double))
        yss_s = <long double *> malloc(acf_model.nlags * sizeof(long double))
        xss_s = <long double *> malloc(acf_model.nlags * sizeof(long double))
        xs_s = <long double *> malloc(acf_model.nlags * sizeof(long double))
        sum_agg_deltas = <long double *> malloc(max_nd * sizeof(long double))

        for i in prange(real_size, schedule='guided'):
            neighbor_node = neighbors[i]
            start = neighbor_node.left
            end = neighbor_node.right

            if start + 2 < end:
                slope = (ts[end] - ts[start]) / (end - start)

                for lag in range(acf_model.nlags):
                    ys_s[lag] = acf_model.ys[lag]
                    yss_s[lag] = acf_model.yss[lag]
                    sxy_s[lag] = acf_model.sxy[lag]
                    xs_s[lag] = acf_model.xs[lag]
                    xss_s[lag] = acf_model.xss[lag]

                start_index_a = (start + 1) // kappa
                end_index_a = (end - 1) // kappa

                num_agg_deltas = end_index_a - start_index_a + 1
                for ii in range(num_agg_deltas):
                    sum_agg_deltas[ii] = 0.0

                for index in range(start + 1, end):
                    agg_index = index // kappa
                    sum_agg_deltas[agg_index - start_index_a] += (slope * (index - start) + ts[start] - ts[index])

                ii = 0
                n = NAGG - 1
                for agg_index in range(start_index_a, end_index_a + 1):
                    sum_agg_deltas[ii] /= kappa # aggregate function
                    delta = sum_agg_deltas[ii]
                    delta_ss = delta * (delta + 2 * aggregates[agg_index])
                    for lag in range(acf_model.nlags):
                        if agg_index > lag:
                            ys_s[lag] += delta
                            yss_s[lag] += delta_ss
                            sxy_s[lag] += delta * aggregates[agg_index - lag - 1]
                        if agg_index < n - lag:
                            xs_s[lag] += delta
                            xss_s[lag] += delta_ss
                            sxy_s[lag] += delta * aggregates[agg_index + lag + 1]

                    ii = ii + 1

                num_lags = num_agg_deltas if num_agg_deltas < acf_model.nlags else acf_model.nlags
                nb_imp[i] = 0
                for lag in range(acf_model.nlags):
                    for ii in range(num_agg_deltas - lag - 1):
                        sxy_s[lag] = sxy_s[lag] + sum_agg_deltas[ii] * sum_agg_deltas[ii + lag + 1]
                    lag_acf = (n * sxy_s[lag] - xs_s[lag] * ys_s[lag]) / sqrtl(
                        (n * xss_s[lag] - xs_s[lag] * xs_s[lag]) * (n * yss_s[lag] - ys_s[lag] * ys_s[lag]))
                    nb_imp[i] += fabsl(lag_acf - raw_acf[lag])
                    n -= 1

                nb_imp[i] /= acf_model.nlags
            else:
                x_a = (ts[end] - ts[start]) / (end - start) + ts[start]
                start = start + 1
                agg_index = start // kappa
                delta = (x_a - ts[start])/kappa # aggregate function
                delta_ss = delta * (2 * aggregates[agg_index] + delta)
                nb_imp[i] = 0
                n = NAGG - 1
                if delta != 0:
                    for lag in range(acf_model.nlags):
                        ys = acf_model.ys[lag]
                        yss = acf_model.yss[lag]
                        xs = acf_model.xs[lag]
                        xss = acf_model.xss[lag]
                        sxy = acf_model.sxy[lag]
                        if agg_index > lag:
                            ys = ys + delta
                            yss = yss + delta_ss
                            sxy = sxy + delta * aggregates[agg_index - lag - 1]
                        if agg_index < n-lag:
                            xs = xs + delta
                            xss = xss + delta_ss
                            sxy = sxy + delta * aggregates[agg_index + lag + 1]
                        lag_acf = (n * sxy - xs * ys) / sqrtl((n * xss - xs * xs) * (n * yss - ys * ys))
                        nb_imp[i] += fabsl(lag_acf - raw_acf[lag])
                        n = n - 1

                    nb_imp[i] /= acf_model.nlags

        free(sum_agg_deltas)
        free(sxy_s)
        free(ys_s)
        free(yss_s)
        free(xss_s)
        free(xs_s)

    for i in range(real_size):
        neighbor_node = neighbors[i]
        neighbor_node.value = nb_imp[i]
        hp_heap.reheap(acf_errors, map_node_to_heap, neighbor_node)

    free(neighbors)
    free(nb_imp)


cpdef np.ndarray[np.uint8_t, ndim=1] simplify_by_fg_agg_sip(double[:] ts, 
                                                            Py_ssize_t hops,
                                                            Py_ssize_t nlags, 
                                                            Py_ssize_t kappa, 
                                                            double acf_threshold,
                                                            Py_ssize_t num_threads):
    cdef: 
        Py_ssize_t start, end, lag, n, num_agg
        long double ace, x_a, c_acf
        long double * raw_acf
        long double * error_values
        long double[:] aggregates
        unordered_map[Py_ssize_t, Py_ssize_t] map_node_to_heap 
        HPNode min_node, left, right
        np.ndarray[np.uint8_t, ndim=1] no_removed_indices = np.ones(ts.shape[0], dtype=bool)
        HPHeap * acf_err_heap = <HPHeap *> malloc(sizeof(HPHeap))
        HPAcfAgg * acf_model = <HPAcfAgg *> malloc(sizeof(HPAcfAgg))

    n = ts.shape[0]
    num_agg = n // kappa

    ace = 0.0
    aggregates = np.empty(num_agg, dtype=np.longdouble)
    raw_acf = <long double *> malloc(nlags * sizeof(long double))
    error_values = <long double *> malloc(n * sizeof(long double))

    hp_acf_agg_model.initialize(acf_model, nlags)  # initialize the aggregates
    hp_acf_agg_model.fit(acf_model, ts, aggregates, kappa)  # extract the aggregates
    hp_acf_agg_model.get_acf(acf_model, raw_acf)  # get raw acf
    hp_math_lib.compute_acf_agg_mean_fall(acf_model, ts, aggregates, raw_acf, error_values, n, kappa)
    hp_heap.initialize(acf_err_heap, map_node_to_heap, error_values, n) # Initialize the heap
    

    while acf_err_heap.values[0].value < INFINITY:
        min_node = hp_heap.pop(acf_err_heap, map_node_to_heap) # TODO: make it a reference
        
        if min_node.value != 0:
            start = min_node.left
            end = min_node.right
            if start + 2 < end:
                hp_acf_agg_model.interpolate_update(acf_model, ts, aggregates, start, end, kappa)
            else:
                x_a = (ts[end]-ts[start]) / (end-start) + ts[start]
                hp_acf_agg_model.update(acf_model, ts, aggregates, x_a, start + 1, kappa)

            ace = 0.0
            n = acf_model.n
            for lag in range(acf_model.nlags):
                n -= 1
                c_acf = (n * acf_model.sxy[lag] - acf_model.xs[lag] * acf_model.ys[lag]) / sqrtl((n * acf_model.xss[lag] - acf_model.xs[lag] * acf_model.xs[lag]) * (n * acf_model.yss[lag] - acf_model.ys[lag] * acf_model.ys[lag]))
                ace += fabsl(raw_acf[lag] - c_acf) 

            ace /= acf_model.nlags

        if ace >= acf_threshold:
            break

        no_removed_indices[min_node.ts] = False
        hp_heap.update_left_right(acf_err_heap, map_node_to_heap, min_node.left, min_node.right)
        if ace != 0:
            parallel_look_ahead_reheap(acf_model, acf_err_heap, map_node_to_heap, ts, aggregates, raw_acf, min_node, hops, kappa, num_threads)

    hp_heap.release_memory(acf_err_heap)
    hp_acf_agg_model.release_memory(acf_model)
    free(error_values)
    free(raw_acf)

    return no_removed_indices