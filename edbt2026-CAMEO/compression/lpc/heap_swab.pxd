# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
from libcpp.unordered_map cimport unordered_map


cdef struct Segment:
    double merge_cost
    Py_ssize_t id
    Py_ssize_t seg_start
    Py_ssize_t seg_end
    Py_ssize_t left_seg
    Py_ssize_t right_seg

ctypedef Segment* SegmentPtr

cdef struct Heap:
    Py_ssize_t c_size
    SegmentPtr values
    Py_ssize_t m_size 

ctypedef Heap* HeapPtr
ctypedef unordered_map[Py_ssize_t, Py_ssize_t]& MapPtr

cdef void initialize(HeapPtr heap, MapPtr map_node_to_heap, Py_ssize_t n)

cdef inline Py_ssize_t parent(Py_ssize_t n)

cdef Segment pop(HeapPtr heap, MapPtr map_node_to_heap)

cdef void reheap(HeapPtr heap, MapPtr map_node_to_heap, Segment& node)

cdef void update_left_right(HeapPtr heap, MapPtr map_node_to_heap, const Py_ssize_t& left, const Py_ssize_t& right)

cdef void get_update_left_right(HeapPtr heap, MapPtr map_node_to_heap, const Segment& node, Segment& left, Segment& right)

cdef void release_memory(HeapPtr heap)