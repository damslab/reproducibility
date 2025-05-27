from libcpp.unordered_map cimport unordered_map


cdef struct HPNode:
    long double value
    Py_ssize_t ts
    Py_ssize_t left
    Py_ssize_t right

ctypedef HPNode* NodePtr

cdef struct HPHeap:
    Py_ssize_t c_size
    Py_ssize_t m_size
    NodePtr values

ctypedef HPHeap* HeapPtr
ctypedef unordered_map[Py_ssize_t, Py_ssize_t]& MapPtr


cdef void initialize(HeapPtr heap, MapPtr map_node_to_heap, long double * errors, Py_ssize_t n)

cdef void initialize_tp(HeapPtr heap, 
                        MapPtr map_node_to_heap, 
                        double *import_tp, 
                        Py_ssize_t *selected_tp, 
                        Py_ssize_t n)

cdef void initialize_vw(HeapPtr heap, MapPtr map_node_to_heap, double[:] aucs)
                        
cdef inline Py_ssize_t parent(Py_ssize_t n)

cdef HPNode pop(HeapPtr heap, MapPtr map_node_to_heap)

cdef void reheap(HeapPtr heap, MapPtr map_node_to_heap, HPNode & node)

cdef void update_left_right(HeapPtr heap, MapPtr map_node_to_heap, Py_ssize_t left, Py_ssize_t right)

cdef void get_update_left_right(HeapPtr heap, MapPtr map_node_to_heap, const HPNode & node, HPNode & left, HPNode & right)

cdef void release_memory(HeapPtr heap)