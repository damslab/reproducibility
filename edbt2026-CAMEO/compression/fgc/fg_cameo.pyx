# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
from compression.lpc cimport inc_acf
from compression.lpc cimport math_utils
from compression.lpc cimport heap as heap_lib
from compression.lpc.inc_acf cimport AcfAgg
from compression.lpc.heap cimport Heap, Node
from libcpp.unordered_map cimport unordered_map
from numpy.math cimport INFINITY
from cython.parallel cimport prange, parallel
from libc.stdlib cimport malloc, free
from libc.math cimport sqrt, fabs
import numpy as np
cimport numpy as np

cdef void parallel_look_ahead_reheap(AcfAgg *acf_agg, 
                                    Heap *acf_errors, 
                                    unordered_map[Py_ssize_t, Py_ssize_t] &map_node_to_heap, 
                                    double [:] ts, 
                                    double * raw_acf, 
                                    Node & removed_node, 
                                    Py_ssize_t hops, 
                                    Py_ssize_t num_threads):
    cdef: # Private var
        Py_ssize_t i, ii, index, lag, end, n, num_deltas, num_lags, start
        double delta, delta_ss, x_a, lag_acf, slope
        double sxy, xs, xss, ys, yss
        Node neighbor_node
    cdef:
        Py_ssize_t real_size, max_nd
        Py_ssize_t left_node_index, right_node_index
        Py_ssize_t N = ts.shape[0]
        Node left_node, right_node
        Node * neighbors = <Node *> malloc(2*hops * sizeof(Node))
        double * nb_imp = <double *> malloc(2*hops * sizeof(double))
        double *deltas
        double *sxy_s
        double *sy_s
        double *syy_s
        double *sx_s
        double *sxx_s

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
            if left_node.right - left_node_index > max_nd:
                max_nd = left_node.right - left_node_index
            real_size += 1
        if right_node_index < N - 1:
            right_node = acf_errors.values[map_node_to_heap[right_node_index]]
            neighbors[real_size] = right_node
            right_node_index = right_node.right
            if right_node_index - right_node.left > max_nd:
                max_nd = right_node_index - right_node.left
            real_size += 1

    with nogil, parallel(num_threads=num_threads):

        sxy_s = <double *> malloc(acf_agg.nlags * sizeof(double))
        sy_s = <double *> malloc(acf_agg.nlags * sizeof(double))
        syy_s = <double *> malloc(acf_agg.nlags * sizeof(double))
        sxx_s = <double *> malloc(acf_agg.nlags * sizeof(double))
        sx_s = <double *> malloc(acf_agg.nlags * sizeof(double))
        deltas = <double *> malloc(max_nd * sizeof(double))

        for i in prange(real_size, schedule='guided'):
            neighbor_node = neighbors[i]
            start = neighbor_node.left
            end = neighbor_node.right
            num_deltas = (end - start - 1)

            if start + 2 < end:
                slope = (ts[end] - ts[start]) / (end - start)

                for lag in range(acf_agg.nlags):
                    sy_s[lag] = acf_agg.ys[lag]
                    syy_s[lag] = acf_agg.yss[lag]
                    sxy_s[lag] = acf_agg.sxy[lag]
                    sx_s[lag] = acf_agg.xs[lag]
                    sxx_s[lag] = acf_agg.xss[lag]

                ii = 0
                n = N - 1
                for index in range(start + 1, end):
                    delta = slope * (index - start) + ts[start] - ts[index]
                    deltas[ii] = delta
                    delta_ss = delta * (delta + 2 * ts[index])
                    for lag in range(acf_agg.nlags):
                        if index >= lag + 1:
                            sy_s[lag] += delta
                            syy_s[lag] += delta_ss
                            sxy_s[lag] += delta * ts[index - lag - 1]
                        if index < n - lag:
                            sx_s[lag] += delta
                            sxx_s[lag] += delta_ss
                            sxy_s[lag] += delta * ts[index + lag + 1]

                    ii = ii + 1

                num_lags = num_deltas if num_deltas < acf_agg.nlags else acf_agg.nlags

                n = N - 1
                nb_imp[i] = 0
                for lag in range(acf_agg.nlags):
                    for ii in range(num_deltas - lag - 1):
                        sxy_s[lag] = sxy_s[lag] + deltas[ii] * deltas[ii + lag + 1]
                    lag_acf = (n * sxy_s[lag] - sx_s[lag] * sy_s[lag]) / sqrt(
                        (n * sxx_s[lag] - sx_s[lag] * sx_s[lag]) * (n * syy_s[lag] - sy_s[lag] * sy_s[lag]))
                    nb_imp[i] += fabs(lag_acf - raw_acf[lag])
                    n -= 1

                nb_imp[i] /= acf_agg.nlags
            else:
                x_a = (ts[end] - ts[start]) / (end - start) + ts[start]
                start = start + 1
                delta = x_a - ts[start]
                delta_ss = delta * (2 * ts[start] + delta)
                nb_imp[i] = 0
                n = N - 1
                if delta != 0:
                    for lag in range(acf_agg.nlags):
                        ys = acf_agg.ys[lag]
                        yss = acf_agg.yss[lag]
                        xs = acf_agg.xs[lag]
                        xss = acf_agg.xss[lag]
                        sxy = acf_agg.sxy[lag]
                        if start >= lag + 1:
                            ys = ys + delta
                            yss = yss + delta_ss
                            sxy = sxy + delta * ts[start - lag - 1]
                        if start < n:
                            xs = xs + delta
                            xss = xss + delta_ss
                            sxy = sxy + delta * ts[start + lag + 1]
                        lag_acf = (n * sxy - xs * ys) / sqrt((n * xss - xs * xs) * (n * yss - ys * ys))
                        nb_imp[i] += fabs(lag_acf - raw_acf[lag])
                        n = n-1

                    nb_imp[i] /= acf_agg.nlags

        free(deltas)
        free(sxy_s)
        free(sy_s)
        free(syy_s)
        free(sxx_s)
        free(sx_s)

    for i in range(real_size):
        neighbor_node = neighbors[i]
        neighbor_node.value = nb_imp[i]
        heap_lib.reheap(acf_errors, map_node_to_heap, neighbor_node)

    free(neighbors)
    free(nb_imp)


cpdef np.ndarray[np.uint8_t, ndim=1] simplify_by_fg_sip(double[:] ts, 
                            Py_ssize_t hops, 
                            Py_ssize_t nlags, 
                            double acf_threshold, 
                            Py_ssize_t num_threads):

    cdef:  # Complex var declaration
        AcfAgg * acf_agg = <AcfAgg *> malloc(sizeof(AcfAgg))
        double * raw_acf = <double *> malloc(nlags * sizeof(double))
        double * error_values = <double *> malloc(ts.shape[0] * sizeof(double))
        np.ndarray[np.uint8_t, ndim=1] no_removed_indices = np.ones(ts.shape[0], dtype=bool)
    cdef:
        unordered_map[Py_ssize_t, Py_ssize_t] map_node_to_heap
        Heap * heap = <Heap *> malloc(sizeof(Heap))
        Node min_node
    cdef:
        Py_ssize_t n, N, lag, order
        Py_ssize_t start_point, end_point
        double acf_error, c_acf, x_a

    # Initialize general ACF aggregate and calculate raw ACF
    inc_acf.initialize(acf_agg, nlags)  # initialize the aggregates
    inc_acf.fit(acf_agg, ts)  # extract the aggregates
    inc_acf.get_acf(acf_agg, raw_acf)  # get raw acf
    math_utils.compute_acf_fall(acf_agg, ts, raw_acf, error_values)  # computing the acf for all points
    
    
    n = ts.shape[0]
    N = ts.shape[0]
    heap_lib.initialize_sip(heap, map_node_to_heap, error_values, n)
    order = 1
    while heap.values[0].value < INFINITY:
        min_node = heap_lib.pop(heap, map_node_to_heap)
        acf_error = 0.0
        if min_node.value != 0:
            start_point = min_node.left
            end_point = min_node.right
            if start_point + 2 < end_point:
                inc_acf.interpolate_update(acf_agg, ts, start_point, end_point)
            else:
                x_a = (ts[end_point] - ts[start_point]) / (end_point - start_point) + ts[start_point]
                inc_acf.update(acf_agg, ts, x_a, start_point + 1)

            n = N - 1
            for lag in range(nlags):
                c_acf = (n * acf_agg.sxy[lag] - acf_agg.xs[lag] * acf_agg.ys[lag]) / \
                        sqrt((n * acf_agg.xss[lag] - acf_agg.xs[lag] * acf_agg.xs[lag]) *
                             (n * acf_agg.yss[lag] - acf_agg.ys[lag] * acf_agg.ys[lag]))
                acf_error += fabs(raw_acf[lag] - c_acf)
                n = n - 1

            acf_error = acf_error / nlags

        if acf_error >= acf_threshold:
            break

        no_removed_indices[min_node.ts] = False
        heap_lib.update_left_right(heap, map_node_to_heap, min_node.left, min_node.right)
        if acf_error != 0:
            parallel_look_ahead_reheap(acf_agg, heap, map_node_to_heap, ts, raw_acf, min_node, hops,  num_threads)
    
    free(error_values)
    free(raw_acf)
    heap_lib.release_memory(heap)
    inc_acf.release_memory(acf_agg)
    map_node_to_heap.clear()

    return no_removed_indices


cpdef np.ndarray[np.uint8_t, ndim=1] simplify_by_fg_sip_cr(double[:] ts, 
                            Py_ssize_t hops, 
                            Py_ssize_t nlags, 
                            Py_ssize_t target_cr, 
                            Py_ssize_t num_threads):

    cdef:  # Complex var declaration
        AcfAgg * acf_agg = <AcfAgg *> malloc(sizeof(AcfAgg))
        double * raw_acf = <double *> malloc(nlags * sizeof(double))
        double * error_values = <double *> malloc(ts.shape[0] * sizeof(double))
        np.ndarray[np.uint8_t, ndim=1] no_removed_indices = np.ones(ts.shape[0], dtype=bool)
    cdef:
        unordered_map[Py_ssize_t, Py_ssize_t] map_node_to_heap
        Heap * heap = <Heap *> malloc(sizeof(Heap))
        Node min_node
    cdef:
        Py_ssize_t n, N, lag, order = 0
        Py_ssize_t start_point, end_point
        double acf_error, c_acf, x_a

    # Initialize general ACF aggregate and calculate raw ACF
    inc_acf.initialize(acf_agg, nlags)  # initialize the aggregates
    inc_acf.fit(acf_agg, ts)  # extract the aggregates
    inc_acf.get_acf(acf_agg, raw_acf)  # get raw acf
    math_utils.compute_acf_fall(acf_agg, ts, raw_acf, error_values)  # computing the acf for all points
    
    
    n = ts.shape[0]
    N = ts.shape[0]
    heap_lib.initialize_sip(heap, map_node_to_heap, error_values, n)
    while heap.values[0].value < INFINITY:
        min_node = heap_lib.pop(heap, map_node_to_heap)
        acf_error = 0.0
        if min_node.value != 0:
            start_point = min_node.left
            end_point = min_node.right
            if start_point + 2 < end_point:
                inc_acf.interpolate_update(acf_agg, ts, start_point, end_point)
            else:
                x_a = (ts[end_point] - ts[start_point]) / (end_point - start_point) + ts[start_point]
                inc_acf.update(acf_agg, ts, x_a, start_point + 1)

            n = N - 1
            for lag in range(nlags):
                c_acf = (n * acf_agg.sxy[lag] - acf_agg.xs[lag] * acf_agg.ys[lag]) / \
                        sqrt((n * acf_agg.xss[lag] - acf_agg.xs[lag] * acf_agg.xs[lag]) *
                             (n * acf_agg.yss[lag] - acf_agg.ys[lag] * acf_agg.ys[lag]))
                acf_error += fabs(raw_acf[lag] - c_acf)
                n = n - 1

            acf_error = acf_error / nlags

        if N/(N-order) > target_cr:
            break

        order += 1
        no_removed_indices[min_node.ts] = False
        heap_lib.update_left_right(heap, map_node_to_heap, min_node.left, min_node.right)
        if acf_error != 0:
            parallel_look_ahead_reheap(acf_agg, heap, map_node_to_heap, ts, raw_acf, min_node, hops,  num_threads)
    
    free(error_values)
    free(raw_acf)
    heap_lib.release_memory(heap)
    inc_acf.release_memory(acf_agg)
    map_node_to_heap.clear()

    return no_removed_indices