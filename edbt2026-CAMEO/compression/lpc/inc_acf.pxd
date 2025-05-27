# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
cdef struct AcfAgg:
    Py_ssize_t nlags, n
    double *sxy
    double *xs
    double *ys
    double *xss
    double *yss

ctypedef AcfAgg* AcfPtr
cdef void initialize(AcfPtr model, Py_ssize_t nlags)

cdef void fit(AcfPtr model, double[:] x)

cdef void get_acf(AcfPtr model, double* result)

cdef void update(AcfPtr model, double[:] x, double x_a, Py_ssize_t index)

cdef double look_ahead_impact(AcfPtr model, double[:] x, double *raw_acf, double x_a, Py_ssize_t index) nogil

cdef inline void update_inside_lags(AcfPtr model, double[:] x,
                                     double delta,
                                     double delta_ss,
                                     Py_ssize_t index)

cdef inline void update_outside_lags(AcfPtr model, double[:] x,
                                     double delta,
                                     double delta_ss,
                                     Py_ssize_t index)

cdef void interpolate_update(AcfPtr model, double[:] x, Py_ssize_t start, Py_ssize_t end)

cdef double look_ahead_interpolated_impact(AcfPtr model, double[:] x, double *raw_acf, Py_ssize_t start, Py_ssize_t end) nogil

cdef void interpolate_update_outside_lags(AcfPtr model, double[:] x, Py_ssize_t start, Py_ssize_t end)

cdef void interpolate_update_inside_lags(AcfPtr model, double[:] x, Py_ssize_t start, Py_ssize_t end)

cdef void release_memory(AcfPtr model)