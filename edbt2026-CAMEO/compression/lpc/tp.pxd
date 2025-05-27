# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
from compression.lpc.heap cimport Node
from compression.lpc.inc_acf cimport AcfAgg
import numpy as np
cimport numpy as np

cdef double compute_importance(double[:] points, Node &node)

cdef bint is_line(double[:] points, Py_ssize_t i)

cdef bint is_concave(double[:] points, Py_ssize_t i)

cdef bint is_convex(double[:] points, Py_ssize_t i)

cdef bint is_downtrend(double[:] points, Py_ssize_t i)

cdef bint is_uptrend(double[:] points, Py_ssize_t i)

cdef bint is_same_trend(double[:] points, Py_ssize_t i)

cdef Py_ssize_t extract_1st_tps_importance(AcfAgg *model, double[:] x, double * raw_acf,
                                     double acf_error, Py_ssize_t * selected_tp,
                                     double * importance_tp, np.ndarray[np.uint8_t, ndim=1] extract_1st_tps_importance)

cpdef np.ndarray[np.uint8_t, ndim=1] simplify_by_tp(double[:] y, Py_ssize_t nlags, double acf_threshold)