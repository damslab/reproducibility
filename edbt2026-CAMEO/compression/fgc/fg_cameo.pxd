# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
from compression.lpc.inc_acf cimport AcfAgg
from compression.lpc.heap cimport Heap, Node
from libcpp.unordered_map cimport unordered_map
import numpy as np
cimport numpy as np


cdef void parallel_look_ahead_reheap(AcfAgg *acf_agg, 
                                    Heap *acf_errors, 
                                    unordered_map[Py_ssize_t, Py_ssize_t] &map_node_to_heap, 
                                    double [:] y, 
                                    double * raw_acf, 
                                    Node & removed_node, 
                                    Py_ssize_t hops, 
                                    Py_ssize_t num_threads)

cpdef np.ndarray[np.uint8_t, ndim=1] simplify_by_fg_sip(double[:] ts, 
                                                        Py_ssize_t hops, 
                                                        Py_ssize_t nlags, 
                                                        double acf_threshold, 
                                                        Py_ssize_t num_threads)