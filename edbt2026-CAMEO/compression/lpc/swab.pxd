# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
from compression.lpc.heap_swab cimport Heap, Segment
from libcpp.unordered_map cimport unordered_map
from libcpp.vector cimport vector
from libcpp.utility cimport pair
cimport numpy as np


cdef double sse_of_segment(Py_ssize_t seg_start, Py_ssize_t seg_end, Py_ssize_t[:] xs, double[:] ys)

cdef double merge_cost(Segment seg_a, Segment seg_b, Py_ssize_t[:] xs, double[:] ys)

cdef void build_segments_pairwise(Heap * heap, unordered_map[Py_ssize_t, Py_ssize_t] &map_node_to_heap, Py_ssize_t [:] xs, double [:] ys)

cdef vector[pair[Py_ssize_t, Py_ssize_t]] bottom_up_aux(Py_ssize_t [:]xs, double [:]ys, Py_ssize_t start_idx, Py_ssize_t end_idx, double max_error)

cpdef np.ndarray[np.uint8_t, ndim=1] bottom_up(Py_ssize_t [:]xs, double [:]ys, double max_error)

cdef void build_segments_pairwise_aux(Heap * heap, unordered_map[Py_ssize_t, Py_ssize_t] &map_node_to_heap, Py_ssize_t [:] xs, double [:] ys,
                                      Py_ssize_t start_idx, Py_ssize_t end_idx)