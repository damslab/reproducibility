# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
from compression.hpc.hp_acf_agg_model cimport HPAcfAgg
from compression.hpc.hp_heap cimport HPHeap, HPNode
from libcpp.unordered_map cimport unordered_map
import numpy as np
cimport numpy as np


cdef void look_ahead_reheap_mean(HPAcfAgg *acf_model, HPHeap *acf_errors, 
                                unordered_map[Py_ssize_t, Py_ssize_t] &map_node_to_heap,
                                double [:]y, long double[:] aggregates, long double *raw_acf,
                                const HPNode &removed_node, Py_ssize_t hops, Py_ssize_t kappa)

                                
cpdef np.ndarray[np.uint8_t, ndim=1] simplify_by_agg_sip(double[:] y, Py_ssize_t hops,
                                                    Py_ssize_t nlags, Py_ssize_t kappa, 
                                                    double acf_threshold)