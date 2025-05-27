from libcpp.vector cimport vector
from irregular_ts cimport Point, Segment, IrregularTS

cdef double line_euclidean_distance(const double & slope_1, const double & slope_2,
                                    const double & intercept_1, const double & intercept_2,
                                    const int & x_start, const int & x_end)  nogil

cdef inline double slope(Point & start, Point & end) nogil 

cdef double interpolate_point(const Point & start, const Point & end, const int & x)  nogil

cdef void compute_line_equation(const Point & point_1, const Point & point_2,
                                double & slope, double & intercept)  nogil

cdef double subseq_euclidean_distance(const vector[Point] & subseq_1,
                                      const vector[Point] & subseq_2)  nogil

cdef double segment_euclidean_distance(const Segment & subseq_1, const Segment & subseq_2)  nogil

cdef void create_all_subseq_points(long [:] x, double [:] y,
                                   vector[vector[Point]] & all_subseq,
                                   const int & m)  nogil

cdef void create_all_segments(long [:] x, double [:] y, IrregularTS & ts, const int & m)  nogil

cdef void matrix_profile(long [:] x, double [:] y, int m,
                         long [:] mp_index, double [:] mp_distance)

cdef void real_matrix_profile(double [:] y, int m, long [:] mp_index, double [:] mp_distance)