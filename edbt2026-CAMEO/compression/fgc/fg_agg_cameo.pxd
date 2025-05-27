# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
from compression.hpc.hp_acf_agg_model cimport HPAcfAgg
from compression.hpc.hp_heap cimport HPHeap, HPNode
from libcpp.unordered_map cimport unordered_map
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
                                        Py_ssize_t num_threads)


cpdef np.ndarray[np.uint8_t, ndim=1] simplify_by_fg_agg_sip(double[:] ts, 
                                                            Py_ssize_t hops,
                                                            Py_ssize_t nlags, 
                                                            Py_ssize_t kappa, 
                                                            double acf_threshold,
                                                            Py_ssize_t num_threads)