from libcpp.vector cimport vector

cdef struct Point:
    int x
    double y

cdef struct Segment:
    vector[Point] points
    vector[double] slopes
    vector[double] intercepts
    int n

cdef struct IrregularTS:
    vector[Segment] segments
    int n


cdef void add_point(Segment & segment, const int & x, const double & y) nogil

cdef void init_segment(Segment & segment) nogil

cdef void init_ts(IrregularTS & ts, const int & n) nogil

cdef void add_segment(IrregularTS & ts) nogil

cdef int last_point(Segment & segment) nogil
