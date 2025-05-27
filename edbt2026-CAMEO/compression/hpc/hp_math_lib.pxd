# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
from compression.hpc.hp_acf_agg_model cimport HPAcfAgg

cdef long double csum(double[:] x, Py_ssize_t n)

cdef long double dot_product(long double[:] x, long double[:] y)

cdef void scan(long double[:] x, long double[:] out1, long double[:] out2) noexcept nogil

cdef void cumsum_cumsum(long double[:] arr, long double[:] cumsum1, long double[:] cumsum2)

cdef double triangle_area(const double &x_p1, const double &y_p1,
                                 const double &x_p2, const double &y_p2,
                                 const double &x_p3, const double &y_p3)

cdef double no_gil_mae(long double *x, long double *y, Py_ssize_t n) noexcept nogil

cdef double mae(long double *x, long double *y, Py_ssize_t n)

cdef void compute_acf_agg_mean_fall(HPAcfAgg *model, double [:]x, long double [:]aggregates,
                               long double *raw_acf, long double *acf_error, Py_ssize_t x_n, Py_ssize_t kappa) noexcept nogil
