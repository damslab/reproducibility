# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
import numpy as np
cimport numpy as np

cpdef np.ndarray[np.uint8_t, ndim=1] simplify_by_vw(long [:] x, double[:] y, Py_ssize_t nlags, double acf_threshold)

cdef double[:] triangle_areas_from_array(long[:] x, double[:] y)

