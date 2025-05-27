import numpy as np
cimport numpy as np

cdef double[:] triangle_areas_from_array(long[:] x, double[:] y)

cpdef np.ndarray[np.uint8_t, ndim=1] simplify_by_agg_vw(long [:] x, double[:] y, Py_ssize_t nlags, Py_ssize_t kappa, double acf_threshold)