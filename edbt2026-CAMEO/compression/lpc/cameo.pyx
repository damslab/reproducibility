# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
from compression.lpc cimport heap, math_utils
from compression.lpc.heap cimport Heap, Node
from libcpp.unordered_map cimport unordered_map
from cython.parallel cimport prange, parallel
from libc.stdlib cimport malloc, free
from libc.math cimport sqrt, fabs
from compression.lpc cimport inc_acf
from compression.lpc.inc_acf cimport AcfAgg
from numpy.math cimport INFINITY
import numpy as np
cimport numpy as np
cimport cython


cdef void look_ahead_reheap(AcfAgg *acf_agg, Heap *acf_errors, unordered_map[Py_ssize_t, Py_ssize_t] &map_node_to_heap, double [:]y, double *raw_acf, const Node &removed_node, Py_ssize_t &hops):
    cdef:
        Py_ssize_t i, ii, left_node_index, right_node_index, start, end, \
            real_size, n, lag, num_deltas, index, num_lags, max_nd
        double x_a, delta, delta_ss, ys, yss, xs, xss, sxy, lag_acf, slope
        Node neighbor_node, left_node, right_node
        Node * neighbors = <Node *> malloc(2 * hops * sizeof(Node))
        double *nb_imp, *deltas, *sxy_s, *ys_s, *yss_s, *xs_s, *xss_s

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
        if right_node_index < acf_agg.n - 1:
            right_node = acf_errors.values[map_node_to_heap[right_node_index]]
            neighbors[real_size] = right_node
            right_node_index = right_node.right
            if right_node_index - right_node.left > max_nd:
                max_nd = right_node_index - right_node.left
            real_size += 1

    nb_imp = <double *> malloc(real_size * sizeof(double))
    sxy_s = <double *> malloc(acf_agg.nlags * sizeof(double))
    ys_s = <double *> malloc(acf_agg.nlags * sizeof(double))
    yss_s = <double *> malloc(acf_agg.nlags * sizeof(double))
    xss_s = <double *> malloc(acf_agg.nlags * sizeof(double))
    xs_s = <double *> malloc(acf_agg.nlags * sizeof(double))
    deltas = <double *> malloc(max_nd * sizeof(double))

    for i in range(real_size):
        neighbor_node = neighbors[i]
        start = neighbor_node.left
        end = neighbor_node.right
        num_deltas = (end - start - 1)

        if start + 2 < end:
            slope = (y[end] - y[start]) / (end - start)

            for lag in range(acf_agg.nlags):
                ys_s[lag] = acf_agg.ys[lag]
                yss_s[lag] = acf_agg.yss[lag]
                sxy_s[lag] = acf_agg.sxy[lag]
                xs_s[lag] = acf_agg.xs[lag]
                xss_s[lag] = acf_agg.xss[lag]

            ii = 0
            n = acf_agg.n - 1
            for index in range(start + 1, end):
                delta = slope * (index - start) + y[start] - y[index]
                deltas[ii] = delta
                delta_ss = delta * (delta + 2 * y[index])
                for lag in range(acf_agg.nlags):
                    if index >= lag + 1:
                        ys_s[lag] += delta
                        yss_s[lag] += delta_ss
                        sxy_s[lag] += delta * y[index - lag - 1]
                    if index < n - lag:
                        xs_s[lag] += delta
                        xss_s[lag] += delta_ss
                        sxy_s[lag] += delta * y[index + lag + 1]

                ii = ii + 1

            num_lags = num_deltas if num_deltas < acf_agg.nlags else acf_agg.nlags

            n = acf_agg.n - 1
            nb_imp[i] = 0
            for lag in range(acf_agg.nlags):
                for ii in range(num_deltas - lag - 1):
                    sxy_s[lag] = sxy_s[lag] + deltas[ii] * deltas[ii + lag + 1]
                lag_acf = (n * sxy_s[lag] - xs_s[lag] * ys_s[lag]) / sqrt(
                    (n * xss_s[lag] - xs_s[lag] * xs_s[lag]) * (n * yss_s[lag] - ys_s[lag] * ys_s[lag]))
                nb_imp[i] += fabs(lag_acf - raw_acf[lag])
                n -= 1

            nb_imp[i] /= acf_agg.nlags
        else:
            x_a = (y[end] - y[start]) / (end - start) + y[start]
            start = start + 1
            delta = x_a - y[start]
            delta_ss = delta * (2 * y[start] + delta)
            nb_imp[i] = 0
            n = acf_agg.n - 1
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
                        sxy = sxy + delta * y[start - lag - 1]
                    if start < n:
                        xs = xs + delta
                        xss = xss + delta_ss
                        sxy = sxy + delta * y[start + lag + 1]
                    lag_acf = (n * sxy - xs * ys) / sqrt((n * xss - xs * xs) * (n * yss - ys * ys))
                    nb_imp[i] += fabs(lag_acf - raw_acf[lag])
                    n = n - 1

                nb_imp[i] /= acf_agg.nlags

    for i in range(real_size):
        neighbor_node = neighbors[i]
        neighbor_node.value = nb_imp[i]
        heap.reheap(acf_errors, map_node_to_heap, neighbor_node)

    free(neighbors)
    free(nb_imp)
    free(deltas)
    free(sxy_s)
    free(ys_s)
    free(yss_s)
    free(xss_s)
    free(xs_s)


cpdef np.ndarray[np.uint8_t, ndim=1] simplify_by_sip(double[:] y, Py_ssize_t hops, Py_ssize_t nlags, double acf_threshold):
    cdef:
        Py_ssize_t start, end, lag, n = y.shape[0]
        double ace = 0.0, x_a, right_area, left_area, c_acf, inf = INFINITY
        double * raw_acf = <double *> malloc(nlags * sizeof(double))
        double * error_values = <double *> malloc(n * sizeof(double))
        # double * c_acf = <double *> malloc(nlags * sizeof(double))
        Heap * acf_errors = <Heap *> malloc(sizeof(Heap))
        AcfAgg * acf_agg = <AcfAgg *> malloc(sizeof(AcfAgg))
        unordered_map[Py_ssize_t, Py_ssize_t] map_node_to_heap
        Node min_node, left, right
        np.ndarray[np.uint8_t, ndim=1] no_removed_indices = np.ones(n, dtype=bool)

    inc_acf.initialize(acf_agg, nlags)  # initialize the aggregates
    inc_acf.fit(acf_agg, y)  # extract the aggregates
    inc_acf.get_acf(acf_agg, raw_acf)  # get raw acf
    math_utils.compute_acf_fall(acf_agg, y, raw_acf, error_values) # computing the areas for all triangles
    heap.initialize_sip(acf_errors, map_node_to_heap, error_values, n) # Initialize the heap
    
    while acf_errors.values[0].value < inf:
        min_node = heap.pop(acf_errors, map_node_to_heap) # TODO: make it a reference
        
        if min_node.value != 0:
            start = min_node.left
            end = min_node.right
            if start + 2 < end:
                inc_acf.interpolate_update(acf_agg, y, start, end)
            else:
                x_a = (y[end]-y[start]) / (end-start) + y[start]
                inc_acf.update(acf_agg, y, x_a, start + 1)

            ace = 0.0
            n = y.shape[0]
            for lag in range(acf_agg.nlags):
                n -= 1
                c_acf = (n * acf_agg.sxy[lag] - acf_agg.xs[lag] * acf_agg.ys[lag]) / \
                              sqrt((n * acf_agg.xss[lag] - acf_agg.xs[lag] * acf_agg.xs[lag]) *
                                   (n * acf_agg.yss[lag] - acf_agg.ys[lag] * acf_agg.ys[lag]))
                ace += fabs(raw_acf[lag] - c_acf)

            ace /= acf_agg.nlags

        if ace >= acf_threshold:
            break

        no_removed_indices[min_node.ts] = False
        heap.update_left_right(acf_errors, map_node_to_heap, min_node.left, min_node.right)
        look_ahead_reheap(acf_agg, acf_errors, map_node_to_heap, y, raw_acf, min_node, hops)

    heap.release_memory(acf_errors)
    inc_acf.release_memory(acf_agg)
    free(raw_acf)
    free(error_values)

    return no_removed_indices


cpdef np.ndarray[np.uint8_t, ndim=1] simplify_by_sip_cr(double[:] y, Py_ssize_t hops, Py_ssize_t nlags, Py_ssize_t target_cr):
    cdef:
        Py_ssize_t start, end, lag, n = y.shape[0], order = 0, N = y.shape[0]
        double ace = 0.0, x_a, right_area, left_area, c_acf, inf = INFINITY
        double * raw_acf = <double *> malloc(nlags * sizeof(double))
        double * error_values = <double *> malloc(n * sizeof(double))
        # double * c_acf = <double *> malloc(nlags * sizeof(double))
        Heap * acf_errors = <Heap *> malloc(sizeof(Heap))
        AcfAgg * acf_agg = <AcfAgg *> malloc(sizeof(AcfAgg))
        unordered_map[Py_ssize_t, Py_ssize_t] map_node_to_heap
        Node min_node, left, right
        np.ndarray[np.uint8_t, ndim=1] no_removed_indices = np.ones(n, dtype=bool)

    inc_acf.initialize(acf_agg, nlags)  # initialize the aggregates
    inc_acf.fit(acf_agg, y)  # extract the aggregates
    inc_acf.get_acf(acf_agg, raw_acf)  # get raw acf
    math_utils.compute_acf_fall(acf_agg, y, raw_acf, error_values) # computing the areas for all triangles
    heap.initialize_sip(acf_errors, map_node_to_heap, error_values, n) # Initialize the heap
    
    while acf_errors.values[0].value < inf:
        min_node = heap.pop(acf_errors, map_node_to_heap) # TODO: make it a reference
        
        if min_node.value != 0:
            start = min_node.left
            end = min_node.right
            if start + 2 < end:
                inc_acf.interpolate_update(acf_agg, y, start, end)
            else:
                x_a = (y[end]-y[start]) / (end-start) + y[start]
                inc_acf.update(acf_agg, y, x_a, start + 1)

            ace = 0.0
            n = N
            for lag in range(acf_agg.nlags):
                n -= 1
                c_acf = (n * acf_agg.sxy[lag] - acf_agg.xs[lag] * acf_agg.ys[lag]) / \
                              sqrt((n * acf_agg.xss[lag] - acf_agg.xs[lag] * acf_agg.xs[lag]) *
                                   (n * acf_agg.yss[lag] - acf_agg.ys[lag] * acf_agg.ys[lag]))
                ace += fabs(raw_acf[lag] - c_acf)

            ace /= acf_agg.nlags
        
        
        if N/(N-order) > target_cr:
            break
        order += 1
        no_removed_indices[min_node.ts] = False
        heap.update_left_right(acf_errors, map_node_to_heap, min_node.left, min_node.right)
        
        if ace != 0:
            look_ahead_reheap(acf_agg, acf_errors, map_node_to_heap, y, raw_acf, min_node, hops)

    heap.release_memory(acf_errors)
    inc_acf.release_memory(acf_agg)
    free(raw_acf)
    free(error_values)

    return no_removed_indices


cpdef np.ndarray[np.float, ndim=1] get_initial_distribution(double[:] y, Py_ssize_t nlags):
    cdef:
        Py_ssize_t n = y.shape[0], i
        double * error_values = <double *> malloc(n * sizeof(double))
        double * raw_acf = <double *> malloc(nlags * sizeof(double))
        AcfAgg * acf_agg = <AcfAgg *> malloc(sizeof(AcfAgg))
        Node min_node, left, right

    initial_distribution = np.ones(y.shape[0], dtype=np.float)
    inc_acf.initialize(acf_agg, nlags)  # initialize the aggregates
    inc_acf.fit(acf_agg, y)  # extract the aggregates
    inc_acf.get_acf(acf_agg, raw_acf)  # get raw acf
    math_utils.compute_acf_fall(acf_agg, y, raw_acf, error_values)  # computing the acf for all

    for i in range(n):
        initial_distribution[i] = error_values[i]

    inc_acf.release_memory(acf_agg)

    free(raw_acf)
    free(error_values)

    return initial_distribution
