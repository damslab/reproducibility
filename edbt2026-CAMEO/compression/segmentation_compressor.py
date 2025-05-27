import os
import numpy as np
import heapq
from numpy.linalg import lstsq


def merge_cost(segA, segB, xs, ys):
    merged_start = min(segA.start, segB.start)
    merged_end = max(segA.end, segB.end)
    merged_xs = xs[merged_start: merged_end + 1]
    merged_ys = ys[merged_start: merged_end + 1]
    A = np.ones((merged_xs.shape[0], 2), float)

    A[:, 0] = merged_xs
    coefficients, residuals, rank, s = lstsq(A, merged_ys, rcond=None)
    try:
        error = residuals[0]
    except IndexError:
        error = 0.0

    return error


class Segment:
    __slots__ = ('id', 'start', 'end', 'left', 'right', 'alive')

    def __init__(self, seg_id, start, end, left, right):
        self.id = seg_id
        self.start = start
        self.end = end
        self.left = left
        self.right = right
        self.alive = True


def build_segments_pairwise(xs, ys):
    n = len(xs)
    segments = []
    heap = []

    seg_id = 0
    prev_id = None
    i = 0
    while i < n:
        start_idx = i
        end_idx = min(i + 1, n - 1)  # 2 points if available
        seg = Segment(seg_id, start_idx, end_idx, left=prev_id, right=None)
        segments.append(seg)

        # Link to previous
        if prev_id is not None:
            segments[prev_id].right = seg_id
            # compute cost
            cost_val = merge_cost(segments[prev_id], seg, xs, ys)
            heap.append((cost_val, prev_id, seg_id))

        prev_id = seg_id
        seg_id += 1
        i += 2

    heapq.heapify(heap)
    return segments, heap

def bottom_up(xs, ys, max_error):
    xs = np.array(xs)
    ys = np.array(ys)

    n = len(xs)
    if n == 0:
        return []

    segments, heap = build_segments_pairwise(xs, ys)
    current_segments = len(segments)

    while heap and heap[0][0] < max_error:
        cost_val, leftID, rightID = heapq.heappop(heap)

        left_seg = segments[leftID]
        right_seg = segments[rightID]

        if not (left_seg.alive and right_seg.alive):
            # one or both are already merged away
            continue
        if left_seg.right != rightID or right_seg.left != leftID:
            # no longer neighbors
            continue

        left_seg.end = right_seg.end
        right_seg.alive = False

        left_seg.right = right_seg.right
        if right_seg.right is not None:
            segments[right_seg.right].left = leftID

        current_segments -= 1


        new_right_id = left_seg.right
        if new_right_id is not None:
            new_right_seg = segments[new_right_id]
            new_cost = merge_cost(left_seg, new_right_seg, xs, ys)
            heapq.heappush(heap, (new_cost, leftID, new_right_id))


    final_segs = []
    for seg in segments:
        if seg.alive:
            final_segs.append((seg.start, seg.end))
    final_segs.sort(key=lambda x: x[0])
    return final_segs

def best_line(xs, ys, start_idx, max_error):
    seg_start = start_idx
    seg_end = start_idx + 1
    n = len(xs)
    err = 0
    while seg_end < n-1 and err < max_error:
        curr_xs = xs[seg_start: seg_end + 1]
        curr_ys = ys[seg_start: seg_end + 1]
        A = np.ones((curr_xs.shape[0], 2), float)

        A[:, 0] = curr_xs
        _, residuals, _, _ = lstsq(A, curr_ys, rcond=None)
        try:
            err = residuals[0]
        except IndexError:
            err = 0.0

        seg_end += 1

    if seg_end < n-1:
        seg_end -= 1

    seg_end -= 1

    return seg_start, seg_end


def swab(xs, ys, max_error):
    xs = np.array(xs)
    ys = np.array(ys)
    n = len(xs)

    if n == 0:
        return []

    final_segments = []
    i = 0
    window_size = int(n*0.15)
    lower_bound = window_size // 2
    upper_bound = 2 * window_size
    end_buffer = min(i + window_size, n)
    while i < n:
        buf_xs = xs[i:end_buffer]
        buf_ys = ys[i:end_buffer]

        local_segs = bottom_up(buf_xs, buf_ys, max_error)

        if not local_segs:
            break

        leftmost_seg_local = local_segs[0]  # e.g., (0, something)
        final_segments.append((leftmost_seg_local[0]+i, leftmost_seg_local[1]+i))

        seg_len = (leftmost_seg_local[1] - leftmost_seg_local[0] + 1)

        if end_buffer < n:
            _, end_buffer = best_line(xs, ys, end_buffer, max_error)
        else:
            for local_seg in local_segs[1:]:
                global_seg = (local_seg[0] + i, local_seg[1] + i)
                final_segments.append(global_seg)

        i += seg_len
        window_size = end_buffer - i
        if window_size <= lower_bound:
            end_buffer = min(end_buffer + lower_bound - 1, n)

        if window_size - i >= upper_bound:
            end_buffer -= (window_size - upper_bound - 1)


    return final_segments


class SWAB(object):
    uncompressed = None

    def __init__(self):
        pass

    def compress(self, uncompressed, error_bound, _=None, __=None):
        self.uncompressed = np.array(uncompressed)
        return np.asarray(bottom_up(np.arange(len(uncompressed)), uncompressed, error_bound))
        
    def decompress(self, compressed):
        concatenated_compressed = np.concatenate(compressed)
        return np.interp(np.arange(len(self.uncompressed)), concatenated_compressed, self.uncompressed[concatenated_compressed])

