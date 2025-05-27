# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
ctypedef HPPIPNode* HPNodePtr
ctypedef HPPIPNode** HPNodeDbPtr
ctypedef HPPIPHeap* HPHeapPtr

cdef struct HPPIPNode:
    HPNodePtr left
    HPNodePtr right
    HPHeapPtr parent
    Py_ssize_t ts
    Py_ssize_t index
    Py_ssize_t order
    double value
    double cache

cdef struct HPPIPHeap:
    HPNodePtr head
    HPNodePtr tail
    HPNodeDbPtr values
    Py_ssize_t size
    Py_ssize_t m_size
    Py_ssize_t global_order

cdef double vertical_distance(HPNodePtr left, HPNodePtr node, HPNodePtr right)

cdef void init_node(HPNodePtr node, HPHeapPtr heap, Py_ssize_t i)

cdef void update_cache(HPNodePtr node)

cdef HPNodePtr put_after(HPNodePtr node, HPNodePtr tail)

cdef HPPIPNode recycle(HPNodePtr node)

cdef HPPIPNode clear(HPNodePtr node)

cdef void init_heap(HPHeapPtr heap, Py_ssize_t size)

cdef HPNodePtr acquire_item(HPHeapPtr heap, Py_ssize_t ts, double value)

cdef void add(HPHeapPtr heap, Py_ssize_t ts, double value)

cdef  Py_ssize_t notify_change(HPHeapPtr heap, Py_ssize_t index)

cdef  Py_ssize_t min(HPHeapPtr heap, Py_ssize_t i, Py_ssize_t j, Py_ssize_t k)

cdef HPPIPNode remove_at(HPHeapPtr heap,  Py_ssize_t index)

cdef  Py_ssize_t bubble_up(HPHeapPtr heap,  Py_ssize_t n)

cdef  Py_ssize_t bubble_down(HPHeapPtr heap,  Py_ssize_t n)

cdef  Py_ssize_t swap(HPHeapPtr heap,  Py_ssize_t i,  Py_ssize_t j)

cdef bint less(HPHeapPtr heap,  Py_ssize_t i,  Py_ssize_t j)

cdef bint i_smaller_than_j(HPHeapPtr heap,  Py_ssize_t i,  Py_ssize_t j)

cdef void iterate(HPHeapPtr heap)

cdef void deinit_heap(HPHeapPtr heap)