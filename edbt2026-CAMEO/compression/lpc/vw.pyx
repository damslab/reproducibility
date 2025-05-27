# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
from compression.lpc cimport heap, math_utils
from compression.lpc.heap cimport Heap, Node
from libcpp.unordered_map cimport unordered_map
from libc.stdlib cimport malloc, free
cimport cython
from compression.lpc cimport inc_acf
from compression.lpc.inc_acf cimport AcfAgg
from numpy.math cimport INFINITY
import numpy as np
cimport numpy as np


cdef double[:] triangle_areas_from_array(long[:] x, double[:] y):
    cdef:
        long n = x.shape[0], i
        np.ndarray[double, ndim=1] result = np.empty((n,), np.float64)
        long[:] x_p1 = x[:n-2]
        double[:] y_p1 = y[:n-2]
        long[:] x_p2 = x[1:n-1]
        double[:] y_p2 = y[1:n-1]
        long[:] x_p3 = x[2:]
        double[:] y_p3 = y[2:]

        np.ndarray[double, ndim=1] accr = np.empty((n-2,), np.float64)  # Accumulate directly into result
        np.ndarray[double, ndim=1] acc1 = np.empty_like(accr)

    np.subtract(y_p2, y_p3, out=accr)
    np.multiply(x_p1, accr, out=accr)
    np.subtract(y_p3, y_p1, out=acc1)
    np.multiply(x_p2, acc1, out=acc1)
    np.add(acc1, accr, out=accr)
    np.subtract(y_p1, y_p2, out=acc1)
    np.multiply(x_p3, acc1, out=acc1)
    np.add(acc1, accr, out=accr)
    np.abs(accr, out=accr)
    accr = np.multiply(accr, 0.5)
    result[1:n-1] = accr
    result[0] = result[n-1] = np.inf
    return result


cpdef np.ndarray[np.uint8_t, ndim=1] simplify_by_vw(long [:] x, double[:] y, Py_ssize_t nlags, double acf_threshold):
    cdef:
        Py_ssize_t start, end
        double ace = 0.0, x_a, right_area, left_area, inf = INFINITY
        double[:] real_areas
        double * raw_acf = <double *> malloc(nlags * sizeof(double))
        double * c_acf = <double *> malloc(nlags * sizeof(double))
        Heap * area_heap = <Heap *> malloc(sizeof(Heap))
        AcfAgg * acf_model = <AcfAgg *> malloc(sizeof(AcfAgg))
        unordered_map[Py_ssize_t, Py_ssize_t] map_node_to_heap
        Node min_node, left, right
        np.ndarray[np.uint8_t, ndim=1] no_removed_indices = np.ones(x.shape[0], dtype=bool)

    real_areas = triangle_areas_from_array(x, y) # computing the areas for all triangles
    heap.initialize_vw(area_heap, map_node_to_heap, real_areas) # Initialize the heap
    inc_acf.initialize(acf_model, nlags) # initialize the aggregates
    inc_acf.fit(acf_model, y) # extract the aggregates
    inc_acf.get_acf(acf_model, raw_acf) # get raw acf

    while area_heap.values[0].value < inf:
        min_node = heap.pop(area_heap, map_node_to_heap) # TODO: make it a reference

        if min_node.value != 0:
            start = min_node.left
            end = min_node.right
            if start + 2 < end:
                inc_acf.interpolate_update(acf_model, y, start, end)
            else:
                x_a = (y[end]-y[start]) / (end-start) + y[start]
                inc_acf.update(acf_model, y, x_a, start + 1)

            inc_acf.get_acf(acf_model, c_acf)
            ace = math_utils.mae(raw_acf, c_acf, nlags)

        if ace >= acf_threshold:
            break

        no_removed_indices[min_node.ts] = False

        heap.get_update_left_right(area_heap, map_node_to_heap, min_node, left, right)

        if right.ts != -1:
            right_area = math_utils.triangle_area(x[right.ts], y[right.ts],
                                       x[right.left], y[right.left],
                                       x[right.right], y[right.right])

            if right_area <= min_node.value:
                right_area = min_node.value

            right.value = right_area
            heap.reheap(area_heap, map_node_to_heap, right)
        if left.ts != -1:
            left_area = math_utils.triangle_area(x[left.ts], y[left.ts],
                                      x[left.left], y[left.left],
                                      x[left.right], y[left.right])

            if left_area <= min_node.value:
                left_area = min_node.value

            left.value = left_area
            heap.reheap(area_heap, map_node_to_heap, left)

    heap.release_memory(area_heap)
    inc_acf.release_memory(acf_model)
    free(raw_acf)
    free(c_acf)

    return no_removed_indices