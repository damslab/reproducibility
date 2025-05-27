from compression.hpc.hp_heap cimport HPNode
from compression.hpc.hp_acf_agg_model cimport HPAcfAgg
import numpy as np
cimport numpy as np

cdef double compute_importance(double[:] points, HPNode &node)

cdef bint is_line(double[:] points, Py_ssize_t i)

cdef bint is_concave(double[:] points, Py_ssize_t i)

cdef bint is_convex(double[:] points, Py_ssize_t i)

cdef bint is_downtrend(double[:] points, Py_ssize_t i)

cdef bint is_uptrend(double[:] points, Py_ssize_t i)

cdef bint is_same_trend(double[:] points, Py_ssize_t i)

cdef Py_ssize_t extract_1st_tps_importance(HPAcfAgg *model, double[:] x, 
                                    long double[:] aggregates, long double * raw_acf,
                                    double acf_error, Py_ssize_t * selected_tp,
                                    double * importance_tp, Py_ssize_t kappa, 
                                    np.ndarray[np.uint8_t, ndim=1] no_removed_indices)

cpdef np.ndarray[np.uint8_t, ndim=1] simplify_by_agg_tp(double[:] y, Py_ssize_t nlags, Py_ssize_t kappa, double acf_threshold)