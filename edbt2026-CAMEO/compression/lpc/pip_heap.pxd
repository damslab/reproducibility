# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
ctypedef PIPNode* NodePtr
ctypedef PIPNode** NodeDbPtr
ctypedef PIPHeap* HeapPtr

cdef struct PIPNode:
    NodePtr left
    NodePtr right
    HeapPtr parent
    Py_ssize_t ts
    Py_ssize_t index
    Py_ssize_t order
    double value
    double cache

cdef struct PIPHeap:
    NodePtr head
    NodePtr tail
    NodeDbPtr values
    Py_ssize_t size
    Py_ssize_t m_size
    Py_ssize_t global_order

cdef double vertical_distance(NodePtr left, NodePtr node, NodePtr right)

cdef void init_node(NodePtr node, HeapPtr heap, Py_ssize_t i)

cdef void update_cache(NodePtr node)

cdef NodePtr put_after(NodePtr node, NodePtr tail)

cdef PIPNode recycle(NodePtr node)

cdef PIPNode clear(NodePtr node)

cdef void init_heap(HeapPtr heap, Py_ssize_t size)

cdef NodePtr acquire_item(HeapPtr heap, Py_ssize_t ts, double value)

cdef void add(HeapPtr heap, Py_ssize_t ts, double value)

cdef  Py_ssize_t notify_change(HeapPtr heap, Py_ssize_t index)

cdef  Py_ssize_t min(HeapPtr heap, Py_ssize_t i, Py_ssize_t j, Py_ssize_t k)

cdef PIPNode remove_at(HeapPtr heap,  Py_ssize_t index)

cdef  Py_ssize_t bubble_up(HeapPtr heap,  Py_ssize_t n)

cdef  Py_ssize_t bubble_down(HeapPtr heap,  Py_ssize_t n)

cdef  Py_ssize_t swap(HeapPtr heap,  Py_ssize_t i,  Py_ssize_t j)

cdef bint less(HeapPtr heap,  Py_ssize_t i,  Py_ssize_t j)

cdef bint i_smaller_than_j(HeapPtr heap,  Py_ssize_t i,  Py_ssize_t j)

cdef void iterate(HeapPtr heap)

cdef void deinit_heap(HeapPtr heap)