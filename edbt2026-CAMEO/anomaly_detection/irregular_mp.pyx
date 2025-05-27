# cython: profile=True
cimport cython
from libc.math cimport sqrt
from libc.time cimport clock, CLOCKS_PER_SEC, clock_t
from libc.stdio cimport printf
from irregular_ts cimport Point, Segment, IrregularTS
from irregular_ts cimport init_ts, add_segment, add_point, last_point
from cython.parallel cimport prange
from libcpp.vector cimport vector
from numpy.math cimport INFINITY
import numpy as np
cimport numpy as np


@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef double line_euclidean_distance(const double & slope_1, const double & slope_2,
                                    const double & intercept_1, const double & intercept_2,
                                    const int & x_start, const int & x_end)  nogil:
    cdef:
        double slope, intercept, sum_xi, sum_x2i

    slope = slope_2 - slope_1
    intercept = intercept_2 - intercept_1
    sum_xi = (x_end * (x_end-1)/2) - (x_start * (x_start-1)/2)
    sum_x2i = (x_end * (x_end - 1) * (2 * x_end - 1)/6) - ((x_start-1) * x_start * (2 * x_start - 1)/6)
    # if with_sqrt:
    #     return sqrt((slope**2)*sum_x2i + (2*slope*intercept*sum_xi) + (x_end-x_start)*(intercept**2))

    return slope*slope*sum_x2i + 2*slope*intercept*sum_xi + (x_end-x_start)*intercept*intercept

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline double slope(Point & start, Point & end)  nogil:
    return (end.y - start.y) / (end.x - start.x)

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef double interpolate_point(const Point & start, const Point & end, const int & x)  nogil:
    return ((end.y - start.y) / (end.x - start.x))*(x-start.x) + start.y

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef void compute_line_equation(const Point & point_1, const Point & point_2,
                                double & slope, double & intercept)  nogil:
    slope = (point_2.y - point_1.y) / (point_2.x - point_1.x)
    intercept = point_1.y - point_1.x*slope


@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef double subseq_euclidean_distance(const vector[Point] & subseq_1,
                                      const vector[Point] & subseq_2)   nogil:
    cdef:
        size_t n_1, n_2
        int pi_1, pi_2, x_start, x_end
        double eud, slope_1, slope_2, intercept_1, intercept_2
        Point line_1_point_1, line_1_point_2, line_2_point_1, line_2_point_2

    pi_1 = 0
    pi_2 = 0
    eud = 0
    n_1 = subseq_1.size()
    n_2 = subseq_2.size()
    while (pi_1 + 1 < n_1) and (pi_2 + 1 < n_2):
        line_1_point_1, line_1_point_2 = subseq_1[pi_1], subseq_1[pi_1 + 1]
        line_2_point_1, line_2_point_2 = subseq_2[pi_2], subseq_2[pi_2 + 1]
        x_start = max(line_1_point_1.x, line_2_point_1.x)
        compute_line_equation(line_1_point_1, line_1_point_2, slope_1, intercept_1)
        compute_line_equation(line_2_point_1, line_2_point_2, slope_2, intercept_2)

        if line_1_point_2.x < line_2_point_2.x:
            x_end = line_1_point_2.x
            pi_1 += 1
        else:
            x_end = line_2_point_2.x
            pi_2 += 1

        eud += line_euclidean_distance(slope_1, slope_2, intercept_1, intercept_2, x_start, x_end)

    eud += (subseq_1[n_1-1].y - subseq_2[n_2-1].y)**2

    return sqrt(eud)


@cython.cdivision(True)
@cython.boundscheck(True)
@cython.wraparound(False)
cdef double segment_euclidean_distance(const Segment & segment_1,
                                      const Segment & segment_2) nogil:
    cdef:
        size_t n_1, n_2
        int pi_1, pi_2, x_start, x_end
        double distance, slope_1, slope_2, slope3, intercept_1, intercept_2, intercept_3
        double sum_xi, sum_x2i
        Point line_1_point_1, line_1_point_2, line_2_point_1, line_2_point_2

    pi_1 = 0
    pi_2 = 0
    distance = 0
    n_1 = segment_1.points.size()
    n_2 = segment_2.points.size()
    for k in range(n_1 + n_2 - 3):
        x_start = max(segment_1.points[pi_1].x, segment_2.points[pi_2].x)

        slope_1 = segment_1.slopes[pi_1]
        intercept_1 = segment_1.intercepts[pi_1]
        slope_2 = segment_2.slopes[pi_2]
        intercept_2 = segment_2.intercepts[pi_2]

        if segment_1.points[pi_1 + 1].x < segment_2.points[pi_2 + 1].x:
            x_end = segment_1.points[pi_1 + 1].x
            pi_1 = pi_1 + 1
        else:
            x_end = segment_2.points[pi_2 + 1].x
            pi_2 = pi_2 + 1

        slope_3 = slope_2 - slope_1
        intercept_3 = intercept_2 - intercept_1
        sum_xi = (x_end * (x_end - 1) / 2) - (x_start * (x_start - 1) / 2)
        sum_x2i = (x_end * (x_end - 1) * (2 * x_end - 1) / 6) - ((x_start - 1) * x_start * (2 * x_start - 1) / 6)
        distance = distance + slope_3 * slope_3 * sum_x2i + 2 * slope_3 * intercept_3 * sum_xi + (
                    x_end - x_start) * intercept_3 * intercept_3

    distance = distance + (segment_1.points[n_1 - 1].y - segment_2.points[n_2 - 1].y) * \
               (segment_1.points[n_1 - 1].y - segment_2.points[n_2 - 1].y)

    return sqrt(distance)

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef void create_all_subseq_points(long [:] x, double [:] y, vector[vector[Point]] & all_subseq, const int & m)  nogil:
    cdef:
        int n, subseq_index, subseq_position, subseq_start
        double x_a
        Point point_1, point_2, point_3
        vector[Point] subseq_pattern

    n = x[x.shape[0]-1]
    subseq_index = 0

    for subseq_start in range(n - m):
        subseq_position = subseq_index

        if x[subseq_index] != subseq_start:
            if x[subseq_index+1] == subseq_start:
                subseq_index += 1
            else:
                point_1 = Point(x[subseq_index], y[subseq_index])
                point_2 = Point(x[subseq_index+1], y[subseq_index+1])
                x_a = interpolate_point(point_1, point_2, subseq_start)
                point_3 = Point(0, x_a)
                subseq_pattern.push_back(point_3)

            subseq_position += 1

        while x[subseq_position] <= subseq_start + m:
            point_3 = Point(x[subseq_position] - subseq_start, y[subseq_position])
            subseq_pattern.push_back(point_3)
            subseq_position += 1

        if subseq_pattern[subseq_pattern.size()-1].x != m:
            point_1 = Point(x[subseq_position-1], y[subseq_position-1])
            point_2 = Point(x[subseq_position], y[subseq_position])
            x_a = interpolate_point(point_1, point_2, subseq_start+m)
            point_3 = Point(m, x_a)
            subseq_pattern.push_back(point_3)

        all_subseq.push_back(subseq_pattern)
        subseq_pattern.clear()


@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef void create_all_segments(long [:] x, double [:] y, IrregularTS & ts, const int & m) nogil:
    cdef:
        int n, subseq_index, subseq_position, subseq_start
        double x_a
        Point point_1
        Point point_2

    n = x[x.shape[0]-1] + 1
    subseq_index = 0

    for subseq_start in range(n - m):
        subseq_position = subseq_index
        add_segment(ts)
        if x[subseq_index] != subseq_start:
            if x[subseq_index+1] == subseq_start:
                subseq_index += 1
            else:
                point_1 = Point(x[subseq_index], y[subseq_index])
                point_2 = Point(x[subseq_index+1], y[subseq_index+1])
                x_a = interpolate_point(point_1, point_2, subseq_start)
                add_point(ts.segments[subseq_start], 0, x_a)

            subseq_position += 1

        while x[subseq_position] <= subseq_start + m:
            add_point(ts.segments[subseq_start], x[subseq_position] - subseq_start, y[subseq_position])
            subseq_position += 1

        if last_point(ts.segments[subseq_start]) != m:
            point_1 = Point(x[subseq_position-1], y[subseq_position-1])
            point_2 = Point(x[subseq_position], y[subseq_position])
            x_a = interpolate_point(point_1, point_2, subseq_start+m)
            add_point(ts.segments[subseq_start], m, x_a)



@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef void matrix_profile(long [:] x, double [:] y, int m,
                         long [:] mp_index, double [:] mp_distance):
    cdef int n, i, j, trivial_lb, trivial_ub, min_index, k
    cdef int pi_1, pi_2, eud, n_1, n_2, x_start, x_end
    cdef double min_distance, distance
    cdef double sum_xi, sum_x2i
    cdef double slope_1, slope_2, slope_3
    cdef double intercept_1, intercept_2, intercept_3
    cdef clock_t start_time, end_time
    cdef double cpu_time_used
    cdef IrregularTS ts

    n = x[x.shape[0]-1] + 1

    init_ts(ts, n-m)

    create_all_segments(x, y, ts, m)

    for i in range(n-m):
    # for i in prange(n-m, nogil=True, schedule='static', num_threads=8):
        trivial_lb = max(i-m/4, 0)
        trivial_ub = min(i+m/4 + 1, n-m)
        min_distance = INFINITY
        for j in range(n-m):
            if trivial_lb <= j <= trivial_ub:
                continue
            else:
                pi_1 = 0
                pi_2 = 0
                distance = 0
                n_1 = ts.segments[i].points.size()
                n_2 = ts.segments[j].points.size()
                for k in range(n_1+n_2-3):
                    x_start = max(ts.segments[i].points[pi_1].x, ts.segments[j].points[pi_2].x)

                    slope_1 = ts.segments[i].slopes[pi_1]
                    intercept_1 = ts.segments[i].intercepts[pi_1]
                    slope_2 = ts.segments[j].slopes[pi_2]
                    intercept_2 = ts.segments[j].intercepts[pi_2]

                    if ts.segments[i].points[pi_1 + 1].x < ts.segments[j].points[pi_2 + 1].x:
                        x_end = ts.segments[i].points[pi_1 + 1].x
                        pi_1 = pi_1 + 1
                    else:
                        x_end = ts.segments[j].points[pi_2 + 1].x
                        pi_2 = pi_2 + 1

                    slope_3 = slope_2 - slope_1
                    intercept_3 = intercept_2 - intercept_1
                    sum_xi = (x_end * (x_end-1)/2) - (x_start * (x_start-1)/2)
                    sum_x2i = (x_end * (x_end - 1) * (2 * x_end - 1)/6) - ((x_start-1) * x_start * (2 * x_start - 1)/6)
                    distance = distance + slope_3*slope_3*sum_x2i + 2*slope_3*intercept_3*sum_xi + (x_end-x_start)*intercept_3*intercept_3

                distance = distance + (ts.segments[i].points[n_1 - 1].y - ts.segments[j].points[n_2 - 1].y) * \
                            (ts.segments[i].points[n_1 - 1].y - ts.segments[j].points[n_2 - 1].y)
                # distance = segment_euclidean_distance(ts.segments[i], ts.segments[j])

                if distance < min_distance:
                    min_distance = distance
                    min_index = j

        mp_index[i] = min_index
        mp_distance[i] = min_distance



@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef void real_matrix_profile(double [:] y, int m, long [:] mp_index, double [:] mp_distance):
    cdef int n, k, i, j, trivial_lb, trivial_ub, min_index
    cdef double min_distance, distance


    n = y.shape[0]
    # for i in prange(n-m, nogil=True, schedule='static', num_threads=8):
    for i in prange(n-m, nogil=True, schedule='static', num_threads=8):
        trivial_lb = max(i - m / 4, 0)
        trivial_ub = min(i + m / 4 + 1, n - m)
        min_distance = INFINITY
        for j in range(n - m):
            if trivial_lb <= j <= trivial_ub:
                continue
            else:
                distance = 0.
                for k in range(m):
                    distance += (y[i + k] - y[j + k]) * (y[i + k] - y[j + k])
                distance = sqrt(distance)
                if distance < min_distance:
                    min_distance = distance
                    min_index = j

        mp_index[i] = min_index
        mp_distance[i] = min_distance



cpdef matrix_profile_caller(long [:] x, double [:] y, int m):
    cdef int n = x[-1] + 1
    cdef double [:] mp_distance = np.empty((n - m, ), dtype=float)
    cdef long [:] mp_index = np.empty((n - m,), dtype=int)

    matrix_profile(x, y, m, mp_index, mp_distance)

    return mp_index, mp_distance


cpdef real_matrix_profile_caller(long [:] x, double [:] y, int m):
    cdef int n = x[-1] + 1
    cdef double [:] mp_distance = np.empty((n - m, ), dtype=float)
    cdef long [:] mp_index = np.empty((n - m,), dtype=int)

    real_matrix_profile(y, m, mp_index, mp_distance)

    return mp_index, mp_distance
