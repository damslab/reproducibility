# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
from libc.stdlib cimport malloc, free
from numpy.math cimport INFINITY
import cython
cdef Py_ssize_t NODE_TYPE_ROOT = 0
cdef Py_ssize_t NODE_TYPE_INVALID = -1
cdef Node FAKE = Node(INFINITY, -1, -1, -1)


cdef inline Py_ssize_t parent(Py_ssize_t n):
    return (n - 1) >> 1


cdef inline bint less(Node n1, Node n2):
    return n1.value < n2.value


cdef void initialize_vw(HeapPtr heap, MapPtr map_node_to_heap, double[:] x):
    cdef Py_ssize_t i
    heap.c_size = x.shape[0]
    heap.m_size = heap.c_size
    heap.values = <NodePtr> malloc(heap.m_size * sizeof(Node))
    map_node_to_heap.reserve(heap.m_size)

    for i in range(heap.m_size):
        heap.values[i] = Node(x[i], i, i-1, i+1)

    heapify(heap)

    for i in range(heap.m_size):
        map_node_to_heap[heap.values[i].ts] = i


cdef void initialize_sip(HeapPtr heap, MapPtr map_node_to_heap, double *x, Py_ssize_t n):
    cdef Py_ssize_t i
    heap.c_size = n
    heap.m_size = n
    heap.values = <NodePtr> malloc(heap.m_size * sizeof(Node))
    map_node_to_heap.reserve(heap.m_size)

    for i in range(heap.m_size):
        heap.values[i] = Node(x[i], i, i-1, i+1)

    heapify(heap)

    for i in range(heap.m_size):
        map_node_to_heap[heap.values[i].ts] = i


cdef void initialize_tp(HeapPtr heap, MapPtr map_node_to_heap, double *import_tp, Py_ssize_t *selected_tp, Py_ssize_t n):
    cdef Py_ssize_t i
    heap.c_size = n
    heap.m_size = selected_tp[n-1]+1
    heap.values = <NodePtr> malloc(heap.c_size * sizeof(Node))
    map_node_to_heap.reserve(heap.c_size)

    heap.values[0] = Node(import_tp[0], selected_tp[0], -1, selected_tp[1])

    for i in range(1, heap.c_size-1):
        heap.values[i] = Node(import_tp[i], selected_tp[i], selected_tp[i-1], selected_tp[i+1])

    heap.values[n-1] = Node(import_tp[n-1], selected_tp[n-1], selected_tp[n-2], selected_tp[n-1]+1)

    heapify(heap)

    for i in range(heap.c_size):
        map_node_to_heap[heap.values[i].ts] = i


cdef inline Node top(HeapPtr heap):
    return heap.values[0]


cdef Node pop(HeapPtr heap, MapPtr map_node_to_heap):
    cdef Node res
    if heap.c_size != 2:
        res = top(heap)
        heap.c_size -= 1
        clear_heap_index(map_node_to_heap, res.ts)
        heap.values[NODE_TYPE_ROOT] = heap.values[heap.c_size]
        heap.values[heap.c_size] = FAKE
        bubble_down(heap, map_node_to_heap, NODE_TYPE_ROOT)
        return res



cdef void set_heap_index(MapPtr map_node_to_heap, Py_ssize_t v, Py_ssize_t i):
    map_node_to_heap[v] = i



cdef void insert(HeapPtr heap, MapPtr map_node_to_heap, Node node):
    heap.values[heap.c_size] = node
    heap.c_size += 1
    bubble_up(heap, map_node_to_heap, heap.c_size-1)



cdef void shiftup(HeapPtr heap, Py_ssize_t start, Py_ssize_t end):
    cdef Py_ssize_t parent_idx, child
    while end > start:
        child = end
        parent_idx = (child-1)>>1
        if heap.values[child].value < heap.values[parent_idx].value:
            heap.values[child], heap.values[parent_idx] = heap.values[parent_idx], heap.values[child]
            end = parent_idx
        else:
            break



cdef void shiftdown(HeapPtr heap, Py_ssize_t start):
    cdef Py_ssize_t iend, istart, ichild, iright
    iend = heap.c_size
    istart = start
    ichild = 2 * istart + 1
    while ichild < iend:
        iright = ichild + 1
        if iright < iend and heap.values[ichild].value > heap.values[iright].value:
            ichild = iright
        heap.values[ichild], heap.values[istart] = heap.values[istart], heap.values[ichild]
        istart = ichild
        ichild = 2 * istart + 1

    shiftup(heap, start, istart)


cdef Py_ssize_t bubble_down(HeapPtr heap, MapPtr map_node_to_heap, Py_ssize_t n):
    cdef  Py_ssize_t left, right, smallest
    while True:
        left = 2 * n + 1
        right = 1 + left
        smallest = n
        if left < heap.c_size and heap.values[left].value < heap.values[smallest].value:
                smallest = left
        if right < heap.c_size and heap.values[right].value < heap.values[smallest].value:
                smallest = right
        if smallest != n:
            heap.values[smallest], heap.values[n] = heap.values[n], heap.values[smallest]
            map_node_to_heap[heap.values[n].ts] = n
            n = smallest
        else:
            map_node_to_heap[heap.values[n].ts] = n
            return n


cdef Py_ssize_t bubble_down_exp(HeapPtr heap, MapPtr map_node_to_heap, Py_ssize_t n):
    cdef  Py_ssize_t left, right, end
    end = heap.c_size
    left = 2 * n + 1
    while left < end:
        right = left + 1
        if right < end and heap.values[right].value < heap.values[left].value:
            left = right

        heap.values[left], heap.values[n] = heap.values[n], heap.values[left]
        map_node_to_heap[heap.values[n].ts] = n
        n = left
        left = 2 * n + 1


@cython.cdivision(True)
cdef void heapify(HeapPtr heap):
    cdef Py_ssize_t i = heap.m_size//2
    while i >= 0:
        shiftdown(heap, i)
        i -= 1



cdef Py_ssize_t bubble_up(HeapPtr heap, MapPtr map_node_to_heap, Py_ssize_t n):
    cdef  Py_ssize_t parent_idx = (n - 1) >> 1
    while n != NODE_TYPE_ROOT and heap.values[n].value < heap.values[parent_idx].value:
        heap.values[n], heap.values[parent_idx] = heap.values[parent_idx], heap.values[n]
        map_node_to_heap[heap.values[n].ts] = n
        n = parent_idx
        parent_idx = (n - 1) >> 1

    map_node_to_heap[heap.values[n].ts] = n
    return n



cdef inline void clear_heap_index(MapPtr map_node_to_heap, Py_ssize_t node):
    map_node_to_heap.erase(node)



cdef void get_update_left_right(HeapPtr heap, MapPtr map_node_to_heap, const Node& node, Node& left, Node& right):
    cdef Py_ssize_t i

    if node.left > 0:
        i = map_node_to_heap[node.left]
        heap.values[i].right = node.right
        left = heap.values[i]
    else:
        left.ts = -1
    if node.right < heap.m_size-1:
        i = map_node_to_heap[node.right]
        heap.values[i].left = node.left
        right = heap.values[i]
    else:
        right.ts = -1



cdef void update_left_right(HeapPtr heap, MapPtr map_node_to_heap, const Py_ssize_t& left, const Py_ssize_t& right):
    cdef Py_ssize_t i

    if left >= 0:
        i = map_node_to_heap[left]
        heap.values[i].right = right
    if right < heap.m_size:
        i = map_node_to_heap[right]
        heap.values[i].left = left



cdef void reheap(HeapPtr heap, MapPtr map_node_to_heap, Node& node):
    cdef Py_ssize_t heap_idx = map_node_to_heap[node.ts]
    if heap.values[heap_idx].value != node.value:
        heap.values[heap_idx] = node
        bubble_down(heap, map_node_to_heap, bubble_up(heap, map_node_to_heap, heap_idx))



cdef bint empty(HeapPtr heap):
    return heap.c_size == 2


cdef void release_memory(HeapPtr heap):
    free(heap.values)
    free(heap)

