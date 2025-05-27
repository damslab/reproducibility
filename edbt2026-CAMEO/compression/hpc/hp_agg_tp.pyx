# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
from compression.hpc cimport hp_heap
from compression.hpc.hp_heap cimport HPHeap, HPNode
from libcpp.unordered_map cimport unordered_map
from libc.stdlib cimport malloc, free
from libc.math cimport sqrtl, fabsl, fabs
from compression.hpc cimport hp_acf_agg_model
from compression.hpc.hp_acf_agg_model cimport HPAcfAgg
from numpy.math cimport INFINITY
import numpy as np
cimport numpy as np
cimport cython


cdef double compute_importance(double[:] points, HPNode &HPNode):
    cdef:
        double slope, intercept, accum_abs_error
        Py_ssize_t k

    slope = (points[HPNode.right] - points[HPNode.left]) / (HPNode.right - HPNode.left)
    intercept = points[HPNode.left] - slope * HPNode.left

    accum_abs_error = 0.0
    for k in range(HPNode.left, HPNode.right):
        accum_abs_error += fabs(slope * k + intercept - points[k])

    return accum_abs_error / (HPNode.right-HPNode.left)


cdef bint is_line(double[:] points, Py_ssize_t i):
    return points[i-1] == points[i] == points[i + 1]


cdef bint is_concave(double[:] points, Py_ssize_t i):
    return (points[i] >= points[i - 1]) and (points[i] >= points[i + 1])


cdef bint is_convex(double[:] points, Py_ssize_t i):
    return (points[i - 1] >= points[i]) and (points[i + 1] >= points[i])


cdef bint is_downtrend(double[:] points, Py_ssize_t i):
    return points[i] > points[i+1] > points[i+3] and points[i] > points[i+2] > points[i+3] \
        and fabs(points[i+2] - points[i+1]) < fabs(points[i] - points[i+2])+fabs(points[i+1] - points[i+3])


cdef bint is_uptrend(double[:] points, Py_ssize_t i):
    return points[i] < points[i+1] < points[i+3] and points[i] < points[i+2] < points[i+3] \
        and fabs(points[i+1] - points[i+2]) < fabs(points[i] - points[i+2])+fabs(points[i+1] - points[i+3])


cdef bint is_same_trend(double[:] points, Py_ssize_t i):
    return fabs(points[i] - points[i+2]) < 0.001 and fabs(points[i+1] - points[i+3]) < 0.001



cdef Py_ssize_t extract_1st_tps_importance(HPAcfAgg *model, double[:] x, 
                                    long double[:] aggregates, long double * raw_acf,
                                    double acf_error, Py_ssize_t * selected_tp,
                                    double * importance_tp, Py_ssize_t kappa, 
                                    np.ndarray[np.uint8_t, ndim=1] no_removed_indices):
    cdef:
        Py_ssize_t i, k
        Py_ssize_t n = x.shape[0], tp_count = 1
        double slope, intercept, accum_abs_error
        double [:] original_x = np.copy(x)

    selected_tp[0] = 0
    importance_tp[0] = INFINITY
    no_removed_indices[0] = True
    for i in range(1, n - 1):
        if not is_line(x, i) and (is_convex(x, i) or is_concave(x, i)):
            selected_tp[tp_count] = i
            if selected_tp[tp_count-1] + 1 < selected_tp[tp_count]:
                if selected_tp[tp_count-1] + 2 < selected_tp[tp_count]:
                    hp_acf_agg_model.interpolate_update(model, x, aggregates, selected_tp[tp_count-1], selected_tp[tp_count], kappa)
                else:
                    left = x[selected_tp[tp_count-2]]
                    right = x[selected_tp[tp_count-1]]
                    x_a = (right - left) / (selected_tp[tp_count-1] - selected_tp[tp_count-2]) + left
                    hp_acf_agg_model.update(model, x, aggregates, x_a, selected_tp[tp_count-2] + 1, kappa)

                slope = ((x[selected_tp[tp_count]] - x[selected_tp[tp_count - 1]]) /
                         (selected_tp[tp_count] - selected_tp[tp_count - 1]))
                intercept = x[selected_tp[tp_count - 1]] - slope * selected_tp[tp_count - 1]

                accum_abs_error = 0
                for k in range(selected_tp[tp_count - 1], selected_tp[tp_count] + 1):
                    accum_abs_error += fabs(slope * k + intercept - original_x[k])

                importance_tp[tp_count] = accum_abs_error/(selected_tp[tp_count - 1]-selected_tp[tp_count - 2])
            else:
                importance_tp[tp_count] = 0

            no_removed_indices[i] = True
            tp_count += 1

    selected_tp[tp_count] = n-1
    importance_tp[tp_count] = INFINITY
    no_removed_indices[n-1] = True
    tp_count += 1

    return tp_count



cpdef np.ndarray[np.uint8_t, ndim=1] simplify_by_agg_tp(double[:] y, Py_ssize_t nlags, Py_ssize_t kappa, double acf_threshold):
    cdef:
        Py_ssize_t i, tp_count, lag, n = y.shape[0] 
        Py_ssize_t left_node_index, right_node_index, start, end
        double ace, x_a, c_acf, inf = INFINITY, node_importance
        long double * raw_acf = <long double *> malloc(nlags * sizeof(long double))
        Py_ssize_t * selected_tp = <Py_ssize_t *> malloc(n * sizeof(Py_ssize_t))
        double * importance_tp = <double *> malloc(n * sizeof(double))
        HPHeap * tp_importance_heap = <HPHeap *> malloc(sizeof(HPHeap))
        HPAcfAgg * acf_agg = <HPAcfAgg *> malloc(sizeof(HPAcfAgg))
        unordered_map[Py_ssize_t, Py_ssize_t] map_node_to_heap
        HPNode min_node, left_node, right_node
        long double[:] aggregates = np.empty(n // kappa, dtype=np.longdouble)
        np.ndarray[np.uint8_t, ndim=1] no_removed_indices = np.zeros(y.shape[0], dtype=bool)

    hp_acf_agg_model.initialize(acf_agg, nlags)  # initialize the aggregates
    hp_acf_agg_model.fit(acf_agg, y, aggregates, kappa)  # extract the aggregates
    hp_acf_agg_model.get_acf(acf_agg, raw_acf)  # get raw acf

    tp_count = extract_1st_tps_importance(acf_agg,
                                          y,
                                          aggregates,
                                          raw_acf,
                                          acf_threshold,
                                          selected_tp,
                                          importance_tp,
                                          kappa,
                                          no_removed_indices)

    ace = 0.0
    n = y.shape[0]
    for lag in range(acf_agg.nlags):
        n -= 1
        c_acf = (n * acf_agg.sxy[lag] - acf_agg.xs[lag] * acf_agg.ys[lag]) / \
                sqrtl((n * acf_agg.xss[lag] - acf_agg.xs[lag] * acf_agg.xs[lag]) *
                        (n * acf_agg.yss[lag] - acf_agg.ys[lag] * acf_agg.ys[lag]))
        ace += fabsl(raw_acf[lag] - c_acf)

    ace /= acf_agg.nlags

    if ace >= acf_threshold:
        hp_heap.release_memory(tp_importance_heap)
        hp_acf_agg_model.release_memory(acf_agg)
        free(raw_acf)
        free(selected_tp)
        free(importance_tp)
        return np.ones(y.shape[0], dtype=bool)

    hp_heap.initialize_tp(tp_importance_heap, map_node_to_heap, importance_tp, selected_tp, tp_count)  # Initialize the heap

    while tp_importance_heap.values[0].value < inf:
        min_node = hp_heap.pop(tp_importance_heap, map_node_to_heap)

        start = min_node.left
        end = min_node.right
        if start + 2 < end:
            hp_acf_agg_model.interpolate_update(acf_agg, y, aggregates, start, end, kappa)
        else:
            x_a = (y[end]-y[start]) / (end-start) + y[start]
            hp_acf_agg_model.update(acf_agg, y, aggregates, x_a, start + 1, kappa)

        ace = 0.0
        n = y.shape[0]
        for lag in range(acf_agg.nlags):
            n -= 1
            c_acf = (n * acf_agg.sxy[lag] - acf_agg.xs[lag] * acf_agg.ys[lag]) / \
                    sqrtl((n * acf_agg.xss[lag] - acf_agg.xs[lag] * acf_agg.xs[lag]) *
                         (n * acf_agg.yss[lag] - acf_agg.ys[lag] * acf_agg.ys[lag]))
            ace += fabsl(raw_acf[lag] - c_acf)

        ace /= acf_agg.nlags

        if ace >= acf_threshold:
            break

        hp_heap.update_left_right(tp_importance_heap, map_node_to_heap, min_node.left, min_node.right)

        if min_node.left > 0:
            left_node_index = map_node_to_heap[min_node.left]
            node_importance = compute_importance(y, tp_importance_heap.values[left_node_index])
            if node_importance > tp_importance_heap.values[left_node_index].value:
                tp_importance_heap.values[left_node_index].value = node_importance
                hp_heap.reheap(tp_importance_heap, map_node_to_heap, tp_importance_heap.values[left_node_index])

        if min_node.right < tp_importance_heap.m_size-1:
            right_node_index = map_node_to_heap[min_node.right]
            node_importance = compute_importance(y, tp_importance_heap.values[right_node_index])
            if node_importance > tp_importance_heap.values[right_node_index].value:
                tp_importance_heap.values[right_node_index].value = node_importance
                hp_heap.reheap(tp_importance_heap, map_node_to_heap, tp_importance_heap.values[right_node_index])

        no_removed_indices[min_node.ts] = False

    hp_heap.release_memory(tp_importance_heap)
    hp_acf_agg_model.release_memory(acf_agg)
    free(raw_acf)
    free(selected_tp)
    free(importance_tp)

    return no_removed_indices


