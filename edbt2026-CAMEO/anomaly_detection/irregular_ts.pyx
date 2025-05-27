cimport cython
from libcpp.vector cimport vector

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef void init_segment(Segment & segment) nogil:
    segment.n = 0
    segment.points = vector[Point]()
    segment.slopes = vector[double] ()
    segment.intercepts = vector[double] ()


@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef void add_point(Segment & segment, const int & x, const double & y) nogil:
    cdef Point p
    cdef int n = segment.n
    p.x = x
    p.y = y
    segment.points.push_back(p)
    if n > 0:
        segment.slopes.push_back((segment.points[n].y - segment.points[n-1].y) / (segment.points[n].x - segment.points[n-1].x))
        segment.intercepts.push_back(segment.points[n].y - segment.points[n].x * segment.slopes[n])
    segment.n += 1


@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef void init_ts(IrregularTS & ts, const int & n) nogil:
    ts.segments.reserve(n)
    ts.n = 0


@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef void add_segment(IrregularTS & ts) nogil:
    cdef Segment s
    s.n = 0
    s.points = vector[Point]()
    s.slopes = vector[double]()
    s.intercepts = vector[double]()
    ts.segments.push_back(s)
    ts.n += 1

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef int last_point(Segment & segment) nogil:
    # cdef int n = segment.points.size()
    return segment.points[segment.n-1].x