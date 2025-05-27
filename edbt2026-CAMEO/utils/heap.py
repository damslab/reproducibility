import heapq
import numpy as np


NODE_TYPE_ROOT = 0
NODE_TYPE_INVALID = -1


def parent(n):
    if n != NODE_TYPE_ROOT:
        return (n - 1) // 2
    else:
        return NODE_TYPE_INVALID


def left_child(n):
    return 2*n + 1


def comp(lhs, rhs):
    return lhs[0] < rhs[0]


class Heap:
    def __init__(self, x):
        self.m_size = len(x)
        indices = np.arange(self.m_size)
        self.heap = list(zip(x, indices, indices - 1, indices + 1))
        heapq.heapify(self.heap)
        self.map_node_to_heap = dict(((node[1], i) for i, node in enumerate(self.heap)))

    def insert(self, node):
        insert_idx = self.m_size
        self.m_size += 1
        self.heap[insert_idx] = node
        self.bubble_up(insert_idx)

    def top(self):
        return self.heap[0]

    def pop(self):
        if not self.empty():
            res = self.top()
            self.m_size -= 1
            self.clear_heap_index(res)
            self.heap[NODE_TYPE_ROOT] = self.heap[self.m_size]
            self.heap[self.m_size] = (np.inf, -1, -1, -1)
            self.bubble_down(NODE_TYPE_ROOT)
            return res

    def set_heap_index(self, v, i):
        self.map_node_to_heap[v[1]] = i

    def bubble_up(self, n):
        parent_idx = parent(n)
        while n != NODE_TYPE_ROOT and parent_idx != NODE_TYPE_INVALID and comp(self.heap[n], self.heap[parent_idx]):
            self.heap[n], self.heap[parent_idx] = self.heap[parent_idx], self.heap[n]

            self.set_heap_index(self.heap[n], n)

            n = parent_idx
            parent_idx = parent(n)

        self.set_heap_index(self.heap[n], n)

        return n

    def small_elem(self, n, left, right):
        smallest = n

        if left < self.m_size and comp(self.heap[left], self.heap[smallest]):
            smallest = left

        if right < self.m_size and comp(self.heap[right], self.heap[smallest]):
            smallest = right

        return smallest

    def bubble_down(self, n):
        while True:
            left = left_child(n)
            right = 1 + left
            smallest = self.small_elem(n, left, right)
            if smallest != n:
                self.heap[smallest], self.heap[n] = self.heap[n], self.heap[smallest]
                self.set_heap_index(self.heap[n], n)
                n = smallest
            else:
                self.set_heap_index(self.heap[n], n)
                return n

    def clear_heap_index(self, node):
        self.map_node_to_heap.pop(node[1])

    def get_left_right(self, node):
        left = None
        right = None

        if node[2] > 0:
            left = self.heap[self.map_node_to_heap[node[2]]]
            left = left[:-1] + (node[3],)

        if node[3] < len(self.heap)-1:
            right = self.heap[self.map_node_to_heap[node[3]]]
            right = right[:2] + (node[2], ) + (right[3], )

        return left, right

    def update_left_right(self, node: tuple):
        if node[2] > 0:
            i: int = self.map_node_to_heap[node[2]]
            left: tuple = self.heap[i]
            left = left[:-1] + (node[3],)
            self.heap[i] = left

        if node[3] < len(self.heap)-1:
            i: int = self.map_node_to_heap[node[3]]
            right: tuple = self.heap[i]
            right = right[:2] + (node[2], ) + (right[3], )
            self.heap[i] = right

    def reheap(self, node):
        heap_idx = self.map_node_to_heap[node[1]]
        self.heap[heap_idx] = node
        self.bubble_down(self.bubble_up(heap_idx))

    def partial_reheap(self, node):
        heap_idx = self.map_node_to_heap[node[1]]
        self.heap[heap_idx] = node

    def full_reheap(self):
        heapq.heapify(self.heap)
        self.map_node_to_heap = dict(((node[1], i) for i, node in enumerate(self.heap)))

    def empty(self):
        return self.m_size == 0

    def update_node(self, node):
        heap_idx = self.map_node_to_heap[node[1]]
        self.heap[heap_idx] = node
