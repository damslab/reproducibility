# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
from libcpp.unordered_map cimport unordered_map


cdef struct Node:
    double value
    Py_ssize_t ts
    Py_ssize_t left
    Py_ssize_t right

ctypedef Node* NodePtr

cdef struct Heap:
    Py_ssize_t c_size
    NodePtr values
    Py_ssize_t m_size

ctypedef Heap* HeapPtr
ctypedef unordered_map[Py_ssize_t, Py_ssize_t]& MapPtr


cdef void initialize_vw(HeapPtr heap, MapPtr map_node_to_heap, double[:] x)
cdef void initialize_sip(HeapPtr heap, MapPtr map_node_to_heap, double *x, Py_ssize_t n)
cdef void initialize_tp(HeapPtr heap, MapPtr map_node_to_heap, double *import_tp, Py_ssize_t *selected_tp, Py_ssize_t n)

cdef void reheap(HeapPtr heap, MapPtr map_node_to_heap, Node& node)

cdef inline Py_ssize_t parent(Py_ssize_t n)
cdef Node pop(HeapPtr heap, MapPtr map_node_to_heap)

cdef void update_left_right(HeapPtr heap, MapPtr map_node_to_heap, const Py_ssize_t& left, const Py_ssize_t& right)

cdef void get_update_left_right(HeapPtr heap, MapPtr map_node_to_heap, const Node& node, Node& left, Node& right)

cdef void release_memory(HeapPtr heap)