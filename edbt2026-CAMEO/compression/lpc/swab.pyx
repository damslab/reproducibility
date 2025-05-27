# cython: language_level=3, cdivision=True, boundscheck=False, wraparound=False, nonecheck=False, initializedcheck=False, infer_types=True
from libc.math cimport ceil
from libc.stdlib cimport malloc, free
from libc.stdio cimport printf
from libc.math cimport sqrt
import numpy as np
cimport numpy as np
from numpy.math cimport INFINITY
from compression.lpc cimport heap_swab as heap_lib
from compression.lpc.heap_swab cimport Segment
from libcpp.vector cimport vector
from libcpp.utility cimport pair
from libcpp.algorithm cimport sort
cimport cython


cdef double sse_of_segment(Py_ssize_t seg_start, Py_ssize_t seg_end, Py_ssize_t[:] xs, double[:] ys):
    """
    Compute the SSE (sum of squared errors) of fitting a line to
    the points xs[i], ys[i], for i in [seg.start..seg.end].
    """
    cdef Py_ssize_t length, i
    cdef double sum_x, sum_y, sum_x2, sum_xy
    cdef double n, var_x, cov_xy, slope, intercept
    cdef double mean_x, mean_y
    cdef double sse, pred, diff

    length = seg_end - seg_start + 1

    if length <= 1:
        # With 0 or 1 point, SSE is 0 by definition
        return 0.0

    # 1) Gather sums in one pass
    sum_x = 0.0
    sum_y = 0.0
    sum_x2 = 0.0
    sum_xy = 0.0

    for i in range(seg_start, seg_end + 1):
        sum_x  += xs[i]
        sum_y  += ys[i]
        sum_x2 += xs[i] * xs[i]
        sum_xy += xs[i] * ys[i]

    n = <double>length
    # Var(x) = sum_x2 - sum_x^2 / n
    var_x = sum_x2 - (sum_x * sum_x / n)

    if abs(var_x) < 1e-14:
        # All x's are almost identical => best is a horizontal line at mean(y)
        mean_y = sum_y / n
        sse = 0.0
        for i in range(seg_start, seg_end + 1):
            diff = ys[i] - mean_y
            sse += diff * diff
        return sqrt(sse) if sse > 0 else 0
    else:
        # cov_xy = sum_xy - (sum_x * sum_y / n)
        cov_xy = sum_xy - (sum_x * sum_y / n)
        slope = cov_xy / var_x
        mean_x = sum_x / n
        mean_y = sum_y / n
        intercept = mean_y - slope * mean_x

        # 2) Compute SSE in a second pass
        sse = 0.0
        for i in range(seg_start, seg_end + 1):
            pred = slope * xs[i] + intercept
            diff = ys[i] - pred
            sse += diff * diff

        return sqrt(sse) if sse > 0 else 0


cdef double merge_cost(Segment seg_a, Segment seg_b, Py_ssize_t[:] xs, double[:] ys):
    """
    The increment in SSE if segA and segB are merged into one segment,
    """
    # Merged segment covers from min(segA.start, segB.start) .. max(segA.end, segB.end).
    cdef Py_ssize_t merged_start = min(seg_a.seg_start, seg_b.seg_start)
    cdef Py_ssize_t merged_end   = max(seg_a.seg_end, seg_b.seg_end)
    cdef double sse_merged = sse_of_segment(merged_start, merged_end, xs, ys)
    return sse_merged


cdef void build_segments_pairwise(Heap * heap, unordered_map[Py_ssize_t, Py_ssize_t] &map_node_to_heap, Py_ssize_t [:] xs, double [:] ys):
    cdef:
        Py_ssize_t n = xs.shape[0]
        Py_ssize_t i = 0, seg_id = 0
        Py_ssize_t start_seg, end_seg
        Py_ssize_t prev_id = -1
        size_t segments_size = <size_t> (ceil(n / 2.0))

    heap.values = <Segment *>malloc(segments_size * sizeof(Segment))
    while i < n:
        start_seg = xs[i]
        end_seg = min(xs[i + 1], xs[n - 1])  # 2 points if available
        heap.values[seg_id] = Segment(INFINITY, seg_id, start_seg, end_seg, prev_id, -1)

        if prev_id != -1:
            cost = merge_cost(heap.values[prev_id], heap.values[seg_id], xs, ys)
            heap.values[prev_id].right_seg = seg_id
            heap.values[prev_id].merge_cost = cost

        prev_id = seg_id
        seg_id += 1
        i += 2

    heap_lib.initialize(heap, map_node_to_heap, segments_size)


cpdef np.ndarray[np.uint8_t, ndim=1] bottom_up(Py_ssize_t [:]xs, double [:]ys, double max_error):
    cdef:
        size_t n = xs.shape[0]
        Py_ssize_t left_idx, right_idx
        double new_cost
        Heap * heap = <Heap *> malloc(sizeof(Heap))
        unordered_map[Py_ssize_t, Py_ssize_t] map_node_to_heap
        size_t segments_size = <size_t> (ceil(n / 2.0))
        Segment left_seg, new_segment
        Segment min_merge
        np.ndarray[np.uint8_t, ndim = 1] no_removed_indices = np.zeros(n, dtype=bool)

    build_segments_pairwise(heap, map_node_to_heap, xs, ys)

    current_segments = segments_size

    while heap.c_size > 0 and heap.values[0].merge_cost < max_error:
        min_merge = heap_lib.pop(heap, map_node_to_heap)
        left_idx = min_merge.left_seg
        right_idx = min_merge.right_seg

        if left_idx != -1:
            left_seg = heap.values[map_node_to_heap[left_idx]]
        else:
            left_seg = min_merge
            left_seg.id = -1

        if right_idx != -1:
            new_segment = heap.values[map_node_to_heap[right_idx]]
        else:
            # Something went wrong! Stop running!
            printf("Most right segment should always have inf cost: %f\n", min_merge.merge_cost)
            break

        new_segment.seg_start = min_merge.seg_start
        new_segment.left_seg = left_seg.id
        left_seg.right_seg = new_segment.id

        if new_segment.left_seg != -1:
            new_cost = merge_cost(left_seg, new_segment, xs, ys)
            left_seg.merge_cost = new_cost
            heap_lib.reheap(heap, map_node_to_heap, left_seg)

        if new_segment.right_seg != -1:
            new_cost = merge_cost(new_segment, heap.values[map_node_to_heap[new_segment.right_seg]], xs, ys)
        else:
            new_cost = INFINITY
        new_segment.merge_cost = new_cost
        heap_lib.reheap(heap, map_node_to_heap, new_segment)

    for i in range(heap.c_size):
        no_removed_indices[heap.values[i].seg_start] = 1
        no_removed_indices[heap.values[i].seg_end] = 1

    heap_lib.release_memory(heap)
    return no_removed_indices



cdef void build_segments_pairwise_aux(Heap * heap, unordered_map[Py_ssize_t, Py_ssize_t] &map_node_to_heap, Py_ssize_t [:] xs, double [:] ys,
                                      Py_ssize_t start_idx, Py_ssize_t end_idx):
    cdef:
        Py_ssize_t n = end_idx - start_idx
        Py_ssize_t i = start_idx, seg_id = 0
        Py_ssize_t start_seg, end_seg
        Py_ssize_t prev_id = -1
        size_t segments_size = <size_t> (ceil(n / 2.0))

    heap.values = <Segment *>malloc(segments_size * sizeof(Segment))
    while i < end_idx:
        start_seg = xs[i]
        end_seg = min(xs[i + 1], xs[end_idx])  # 2 points if available
        heap.values[seg_id] = Segment(INFINITY, seg_id, start_seg, end_seg, prev_id, -1)

        if prev_id != -1:
            cost = merge_cost(heap.values[prev_id], heap.values[seg_id], xs, ys)
            heap.values[prev_id].right_seg = seg_id
            heap.values[prev_id].merge_cost = cost

        prev_id = seg_id
        seg_id += 1
        i += 2

    heap_lib.initialize(heap, map_node_to_heap, segments_size)



cdef vector[pair[Py_ssize_t, Py_ssize_t]] bottom_up_aux(Py_ssize_t [:]xs, double [:]ys, Py_ssize_t start_idx, Py_ssize_t end_idx, double max_error):
    cdef:
        size_t n = end_idx - start_idx
        Py_ssize_t left_idx, right_idx, j
        double new_cost
        Heap * heap = <Heap *> malloc(sizeof(Heap))
        unordered_map[Py_ssize_t, Py_ssize_t] map_node_to_heap
        size_t segments_size = <size_t> (ceil(n / 2.0))
        Segment left_seg, new_segment
        Segment min_merge
        vector[pair[Py_ssize_t, Py_ssize_t]] segments

    build_segments_pairwise_aux(heap, map_node_to_heap, xs, ys, start_idx, end_idx)

    current_segments = segments_size

    while heap.c_size > 0 and heap.values[0].merge_cost < max_error:
        min_merge = heap_lib.pop(heap, map_node_to_heap)

        left_idx = min_merge.left_seg
        right_idx = min_merge.right_seg

        if left_idx != -1:
            left_seg = heap.values[map_node_to_heap[left_idx]]
        else:
            left_seg = min_merge
            left_seg.id = -1

        if right_idx != -1:
            new_segment = heap.values[map_node_to_heap[right_idx]]
        else:
            # Something went wrong! Stop running!
            printf("Most right segment should always have inf cost: %f\n", min_merge.merge_cost)
            break

        new_segment.seg_start = min_merge.seg_start
        new_segment.left_seg = left_seg.id
        left_seg.right_seg = new_segment.id

        if new_segment.left_seg != -1:
            new_cost = merge_cost(left_seg, new_segment, xs, ys)
            left_seg.merge_cost = new_cost
            heap_lib.reheap(heap, map_node_to_heap, left_seg)

        if new_segment.right_seg != -1:
            new_cost = merge_cost(new_segment, heap.values[map_node_to_heap[new_segment.right_seg]], xs, ys)
        else:
            new_cost = INFINITY

        new_segment.merge_cost = new_cost
        heap_lib.reheap(heap, map_node_to_heap, new_segment)

    for i in range(heap.c_size):
        segments.push_back(pair[Py_ssize_t, Py_ssize_t](heap.values[i].seg_start, heap.values[i].seg_end))

    sort(segments.begin(), segments.end())

    heap_lib.release_memory(heap)
    return segments


cdef Py_ssize_t best_line(Py_ssize_t [:] xs, double [:] ys, Py_ssize_t seg_start, double max_error):
    cdef Py_ssize_t seg_end = seg_start + 1
    cdef Py_ssize_t n = xs.shape[0]
    cdef double cost = 0

    while seg_end < n-1 and cost < max_error:
        cost = sse_of_segment(seg_start, seg_end, xs, ys)
        seg_end += 1

    # seg_end -= 1

    return seg_end


cpdef np.ndarray[np.uint8_t, ndim=1] swab(Py_ssize_t [:] xs, double [:]ys, double max_error, double window_size_fraction):
    cdef:
        Py_ssize_t i, idx, window_size, lower_bound, upper_bound, end_buffer, seg_len
        Py_ssize_t first, second
        Py_ssize_t n = xs.shape[0]
        np.ndarray[np.uint8_t, ndim = 1] no_removed_indices = np.zeros(n, dtype=bool)
        vector[pair[Py_ssize_t, Py_ssize_t]] bottom_up_results
        Py_ssize_t [:] buf_xs
        double [:] buf_ys

    window_size = int(n * window_size_fraction)
    lower_bound = window_size // 2
    upper_bound = 2 * window_size
    end_buffer = window_size
    i = 0
    while i < n:
        bottom_up_results = bottom_up_aux(xs, ys, i, end_buffer, max_error)

        first = bottom_up_results[0].first
        second = bottom_up_results[0].second

        no_removed_indices[first] = True
        no_removed_indices[second] = True

        seg_len = second - first + 1

        if end_buffer < n - 1:
            end_buffer = best_line(xs, ys, end_buffer, max_error)
        else:
            for idx in range(2, bottom_up_results.size()):
                first = bottom_up_results[idx].first
                second = bottom_up_results[idx].second
                no_removed_indices[first] = True
                no_removed_indices[second] = True
            break

        i += seg_len
        window_size = end_buffer - i
        if window_size <= lower_bound:
            end_buffer = min(end_buffer + lower_bound - 1, n)

        if window_size - i >= upper_bound:
            end_buffer -= (window_size - upper_bound - 1)

    return no_removed_indices


