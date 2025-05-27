# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
from compression.lpc.heap cimport Heap, Node
from libcpp.unordered_map cimport unordered_map
from compression.lpc.inc_acf cimport AcfAgg
import numpy as np
cimport numpy as np


cdef void look_ahead_reheap(AcfAgg *acf_agg, Heap *acf_errors, unordered_map[Py_ssize_t, Py_ssize_t] &map_node_to_heap, double [:]y, double *raw_acf, const Node &removed_node, Py_ssize_t &hops)

cpdef np.ndarray[np.uint8_t, ndim=1] simplify_by_sip(double[:] y, Py_ssize_t hops, Py_ssize_t nlags, double acf_threshold)


cpdef np.ndarray[np.float, ndim=1] get_initial_distribution(double[:] y, Py_ssize_t nlags)