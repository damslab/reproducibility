# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
cdef struct HPAcfAgg:
    Py_ssize_t nlags, n
    long double *sxy
    long double *xs
    long double *ys
    long double *xss
    long double *yss

ctypedef HPAcfAgg* AcfPtr

cdef void fit(AcfPtr model, double[:] x, long double [:] aggregates, Py_ssize_t kappa)

cdef void initialize(AcfPtr model, Py_ssize_t nlags)


cdef void get_acf(AcfPtr model, long double * result)


cdef void update(AcfPtr model, double[:] x, long double[:] aggregates,
                      long double x_a, Py_ssize_t index, Py_ssize_t kappa)

cdef inline void update_inside_lags(AcfPtr model, 
                                    long double[:] aggregates,
                                    long double delta,
                                    long double delta_ss,
                                    Py_ssize_t index_a)

cdef inline void update_outside_lags(AcfPtr model, 
                                    long double[:] aggregates,
                                    long double delta,
                                    long double delta_ss,
                                    Py_ssize_t index_a)

cdef void interpolate_update(AcfPtr model, double[:] x, long double[:] aggregates, Py_ssize_t start, Py_ssize_t end, Py_ssize_t kappa)

cdef void interpolate_update_outside_lags(AcfPtr model, 
                                            double[:] x, long double[:] aggregates,
                                            Py_ssize_t start, Py_ssize_t end, 
                                            Py_ssize_t start_index_a,
                                            Py_ssize_t end_index_a, Py_ssize_t kappa)

cdef void interpolate_update_inside_lags(AcfPtr model, double[:] x, 
                                            long double[:] aggregates, Py_ssize_t start, Py_ssize_t end, Py_ssize_t start_index_a,
                                            Py_ssize_t end_index_a, Py_ssize_t kappa)

cdef void release_memory(AcfPtr model)