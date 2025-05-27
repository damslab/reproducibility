import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle as pkl
import irregular_mp as mpf
from sklearn.metrics.pairwise import euclidean_distances


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def slope(self, previous_point):
        return (self.y-previous_point.y)/(self.x-previous_point.x)


class Line:
    def __init__(self, point1, point2):
        self.points = []
        self.points.extend([point1, point2])
        self.slope = point2.slope(point1)
        self.mean = self.slope * (point2.x + self.points[0].x) / 2 + self.points[0].y
        self.std = np.abs(self.slope) * np.sqrt(((point2.x + 1) ** 2 - 1) / 12)
        self.intercept = point1.y - point1.x * self.slope


class Segment:
    def __init__(self):
        self.points = []
        self.mean = 0
        self.std = 0
        self.n = 0

    def add_point(self, point):
        self.points.append(point)
        if self.n == 0:
            # moment_1 = point.y - self.mean
            # self.mean += (point.y-self.mean)/(self.n+1)
            # self.var = (self.n*self.var + moment_1*(point.y - self.mean))/(self.n + 1)
            self.mean = point.y
            self.n += 1
        elif self.n == 1:
            slope = point.slope(self.points[0])
            self.mean = slope*(point.x+self.points[0].x)/2 + self.points[0].y
            self.std = np.abs(slope)*np.sqrt(((point.x+1)**2 - 1) / 12)
            self.n = point.x

    def add_points(self, points):
        self.points.extend(points)

    def rolling_segment(self, next_point):
        first_point = self.points[0]
        new_segment = Segment()
        if first_point.x != self.points[1].x:
            x_a = self.points[1].slope(self.points[0])
            new_segment.add_point(Point(0, x_a))
        new_segment.add_points(self.points[1:])
        new_segment.add_point(next_point)

        return new_segment


def interpolate_point(start, end, x):
    return end.slope(start)*(x-start.x) + start.y


def real_euclidean_distance(x, y, with_sqrt=False):
    if with_sqrt:
        return np.sqrt(np.sum((x-y)**2))

    return np.sum((x-y)**2)


def line_euclidean_distance(slope_1, slope_2, intercept_1, intercept_2, x_start, x_end, with_sqrt=False):
    slope = slope_2 - slope_1
    intercept = intercept_2 - intercept_1
    sum_xi = (x_end * (x_end-1)/2) - (x_start * (x_start-1)/2)
    sum_x2i = (x_end * (x_end - 1) * (2 * x_end - 1)/6) - ((x_start-1) * x_start * (2 * x_start - 1)/6)
    if with_sqrt:
        return np.sqrt((slope**2)*sum_x2i + (2*slope*intercept*sum_xi) + (x_end-x_start)*(intercept**2))

    return (slope**2)*sum_x2i + (2*slope*intercept*sum_xi) + (x_end-x_start)*(intercept**2)


def compute_line_equation(point_1, point_2):
    slope = (point_2.y - point_1.y) / (point_2.x - point_1.x)
    intercept = point_1.y - point_1.x*slope
    return slope, intercept


def print_subseq(subseq_1, subseq_2, do_print):
    interp_x_1 = np.arange(subseq_1[0].x, subseq_1[-1].x+1)
    interp_x_2 = np.arange(subseq_2[0].x, subseq_2[-1].x+1)

    x_axis_1 = [point.x for point in subseq_1]
    y_axis_1 = [point.y for point in subseq_1]
    x_axis_2 = [point.x for point in subseq_2]
    y_axis_2 = [point.y for point in subseq_2]

    interp_y_1 = np.interp(interp_x_1, x_axis_1, y_axis_1)
    interp_y_2 = np.interp(interp_x_2, x_axis_2, y_axis_2)

    if do_print:
        plt.plot(interp_y_1, label='subseq_1')
        plt.plot(interp_y_2, label='subseq_2')
        plt.legend()
        plt.show()

    return interp_y_1, interp_y_2


def subseq_euclidean_distance(subseq_1, subseq_2):
    assert (subseq_1[-1].x - subseq_1[0].x) & (subseq_2[-1].x-subseq_2[0].x)

    n_1 = len(subseq_1)
    n_2 = len(subseq_2)
    pi_1 = 0
    pi_2 = 0
    eud = 0
    real_eud = 0
    interp_y_1, interp_y_2 = print_subseq(subseq_1, subseq_2, do_print=False)
    k = 0
    while k < n_1+n_2-3:
        line_1_point_1, line_1_point_2 = subseq_1[pi_1], subseq_1[pi_1 + 1]
        line_2_point_1, line_2_point_2 = subseq_2[pi_2], subseq_2[pi_2 + 1]
        x_start = max(line_1_point_1.x, line_2_point_1.x)
        slope_1, intercept_1 = compute_line_equation(line_1_point_1, line_1_point_2)
        slope_2, intercept_2 = compute_line_equation(line_2_point_1, line_2_point_2)

        if line_1_point_2.x == line_2_point_2.x:
            x_end = line_1_point_2.x
            pi_1 += 1
            pi_2 += 1
            k += 1
        elif line_1_point_2.x < line_2_point_2.x:
            x_end = line_1_point_2.x
            pi_1 += 1
        else:
            x_end = line_2_point_2.x
            pi_2 += 1

        eud += line_euclidean_distance(slope_1, slope_2, intercept_1, intercept_2, x_start, x_end)
        real_eud += real_euclidean_distance(interp_y_1[x_start:x_end], interp_y_2[x_start:x_end])

        assert np.isclose(eud, real_eud, atol=1.e-6)
        k += 1

    eud += (subseq_1[-1].y - subseq_2[-1].y)**2

    assert np.isclose(np.sqrt(eud), real_euclidean_distance(interp_y_1, interp_y_2, True), atol=1.e-3)

    return np.sqrt(eud)


def real_matrix_profile(x_values, y_values, subseq_len):
    n = y_values.shape[0]
    m = subseq_len
    for i in range(n - m + 1):
        for j in range(n - m + 1):
            D = 0
            for k in range(m):
                D += (y_values[i + k] - y_values[j + k]) ** 2
            D = np.sqrt(D)

    return 0


def matrix_profile_v1(x_values, y_values, subseq_len):
    N = x_values.shape[-1]
    subseq_index = 0
    subseq_start = 0

    while subseq_start + subseq_len < N:

        subseq_position = subseq_start
        subseq_pattern = []

        if x_values[subseq_index] != subseq_start:
            if x_values[subseq_index+1] == subseq_start:
                subseq_index += 1
            else:
                x_a = interpolate_point(Point(x_values[subseq_index], y_values[subseq_index]),
                                        Point(x_values[subseq_index+1], y_values[subseq_index+1]),
                                        subseq_start)
                subseq_pattern.append(Point(0, x_a))

        while x_values[subseq_position] <= x_values[subseq_start] + subseq_len:
            subseq_pattern.append(Point(x_values[subseq_position] - x_values[subseq_start], y_values[subseq_position]))
            subseq_position += 1

        if subseq_pattern[-1].x != subseq_len:
            x_a = interpolate_point(Point(x_values[subseq_position-1], y_values[subseq_position-1]),
                                    Point(x_values[subseq_position], y_values[subseq_position]),
                                    x_values[subseq_start]+subseq_len)

            subseq_pattern.append(Point(subseq_len, x_a))

        ts_index = 0
        ts_start = 0
        while ts_start + subseq_len < N:
            ts_position = ts_start
            ts_pattern = []

            if x_values[ts_index] != ts_start:
                if x_values[ts_index + 1] == ts_start:
                    ts_index += 1
                else:
                    x_a = interpolate_point(Point(x_values[ts_index], y_values[ts_index]),
                                            Point(x_values[ts_index + 1], y_values[ts_index + 1]),
                                            ts_start)
                    ts_pattern.append(Point(0, x_a))

            while x_values[ts_position] <= x_values[ts_start] + subseq_len:
                ts_pattern.append(
                    Point(x_values[ts_position] - x_values[ts_start], y_values[ts_position]))
                ts_position += 1

            if ts_pattern[-1].x != subseq_len:
                x_a = interpolate_point(Point(x_values[ts_position - 1], y_values[ts_position - 1]),
                                        Point(x_values[ts_position], y_values[ts_position]),
                                        x_values[ts_start] + subseq_len)

                ts_pattern.append(Point(subseq_len, x_a))

            ts_start += 1

            subseq_euclidean_distance(subseq_pattern, ts_pattern)

        print('Subseq start', subseq_start)
        subseq_start += 1


def create_all_subseq_points(x, y, subseq_len):
    N = x[-1]
    subseq_index = 0
    all_subseq = []

    for subseq_start in range(N - subseq_len):
        subseq_pattern = []
        subseq_position = subseq_index

        if x[subseq_index] != subseq_start:
            if x[subseq_index+1] == subseq_start:
                subseq_index += 1
            else:
                x_a = interpolate_point(Point(x[subseq_index], y[subseq_index]),
                                        Point(x[subseq_index+1], y[subseq_index+1]),
                                        subseq_start)
                # subseq_pattern.append(Point(subseq_start, x_a))
                subseq_pattern.append(Point(0, x_a))

            subseq_position += 1

        while x[subseq_position] <= subseq_start + subseq_len:
            # subseq_pattern.append(Point(x[subseq_position], y[subseq_position]))
            subseq_pattern.append(Point(x[subseq_position] - subseq_start, y[subseq_position]))
            subseq_position += 1

        if subseq_pattern[-1].x != subseq_len:
            x_a = interpolate_point(Point(x[subseq_position-1], y[subseq_position-1]),
                                    Point(x[subseq_position], y[subseq_position]),
                                    subseq_start+subseq_len)

            subseq_pattern.append(Point(subseq_len, x_a))

        all_subseq.append(subseq_pattern)

    return all_subseq


def matrix_profile_v2(x, y, subseq_len):
    n = x[-1]
    all_subseq = create_all_subseq_points(x, y, subseq_len)
    mp_distance = np.empty((n-subseq_len, ), dtype=float)
    mp_index = np.empty((n-subseq_len, ), dtype=int)
    for i in range(n-subseq_len):
        print('Subsequence pattern', i)
        distance = np.empty((n-subseq_len, ), dtype=float)
        trivial_lb = max(i-subseq_len/4, 0)
        trivial_ub = min(i+subseq_len/4 + 1, n-subseq_len)
        for j in range(n-subseq_len):
            if trivial_lb <= j <= trivial_ub:
                distance[j] = np.inf
            else:
                distance[j] = subseq_euclidean_distance(all_subseq[i], all_subseq[j])

        mp_index[i] = int(np.argmin(distance))
        mp_distance[i] = distance[mp_index[i]]

    return mp_index, mp_distance


def test_matrix_profile():
    N = 10000
    np.random.seed(42)
    for i in range(1000):
        print('Iteration', i)
        subseq_len = np.random.randint(50, 200)
        sampling = int(N * 0.25)
        x = np.arange(N)
        y = np.round(np.random.rand(N), 2)
        r = np.empty((sampling + 2,), dtype=int)
        r[0] = x[0]
        r[-1] = x[-1]
        r[1:-1] = np.sort(np.random.choice(x[1:-1], sampling, replace=False))
        x = x[r]
        y = y[r]
        # create_all_subseq_points(x, y, subseq_len)
        matrix_profile_v2(x, y, subseq_len)
        # real_matrix_profile(x, y, subseq_len)

def test_subseq_euclidean_distance():
    np.random.seed(42)
    N = 100000

    subseq_pattern = [Point(0, np.random.rand()), Point(10, np.random.rand())]
    subseq_ts = [Point(0, np.random.rand()), Point(10, np.random.rand())]
    subseq_euclidean_distance(subseq_pattern, subseq_ts)

    subseq_pattern = [Point(0, np.random.rand()), Point(10, np.random.rand()), Point(20, np.random.rand())]
    subseq_ts = [Point(0, np.random.rand()), Point(10, np.random.rand()), Point(20, np.random.rand())]
    subseq_euclidean_distance(subseq_pattern, subseq_ts)

    subseq_pattern = [Point(0, np.random.rand()),
                      Point(10, np.random.rand()),
                      Point(20, np.random.rand()),
                      Point(30, np.random.rand())]
    subseq_ts = [Point(0, np.random.rand()),
                 Point(10, np.random.rand()),
                 Point(15, np.random.rand()),
                 Point(20, np.random.rand()),
                 Point(25, np.random.rand()),
                 Point(30, np.random.rand())]
    subseq_euclidean_distance(subseq_pattern, subseq_ts)

    for i in range(100):
        print('Iteration', i)
        sampling = int(N*np.random.uniform(0.2, 0.7))
        x = np.arange(N)
        y = np.round(np.random.rand(N), 2)
        r = np.empty((sampling+2,), dtype=int)
        r[0] = x[0]
        r[-1] = x[-1]
        r[1:-1] = np.sort(np.random.choice(x[1:-1], sampling, replace=False))
        x = x[r]
        y = y[r]
        start = np.random.randint(20, x.shape[0]//2)
        subseq_len = np.random.randint(50, 200)
        position = start

        subseq_pattern = []

        while x[position] <= x[start]+subseq_len:
            subseq_pattern.append(Point(x[position]-x[start], y[position]))
            position += 1

        if subseq_pattern[-1].x != subseq_len:
            x_a = interpolate_point(Point(x[position-1], y[position-1]), Point(x[position], y[position]), x[start]+subseq_len)
            assert np.isclose(x_a, np.interp(np.arange(N), x, y)[x[start]+subseq_len], atol=1.e-6)
            subseq_pattern.append(Point(subseq_len, x_a))

        start += np.random.randint(20, x.shape[0]//2)
        position = start

        subseq_ts = []

        while x[position] <= x[start] + subseq_len:
            subseq_ts.append(Point(x[position]-x[start], y[position]))
            position += 1

        if subseq_ts[-1].x != subseq_len:
            x_a = interpolate_point(Point(x[position - 1], y[position - 1]), Point(x[position], y[position]),
                                    x[start] + subseq_len)
            assert np.isclose(x_a, np.interp(np.arange(N), x, y)[x[start] + subseq_len], atol=1.e-6)
            subseq_ts.append(Point(subseq_len, x_a))

        subseq_euclidean_distance(subseq_pattern, subseq_ts)

def test_line_euclidean_distance():
    np.random.seed(42)
    acc_ied = 0
    acc_ed = 0
    for i in range(10000):
        x_start = np.random.randint(1, 100)
        x_end = x_start + np.random.randint(2, 1000)
        x = np.arange(x_start, x_end)
        m1 = np.random.rand()
        m2 = np.random.rand()
        n1 = np.random.rand()
        n2 = np.random.rand()
        y1 = m1*x + n1
        y2 = m2*x + n2
        start_time = time.time()
        iec = line_euclidean_distance(m1, m2, n1, n2, x_start, x_end-1, with_sqrt=True)
        acc_ied += time.time()-start_time
        start_time = time.time()
        ed = euclidean_distances(y1[np.newaxis, :-1], y2[np.newaxis, :-1])
        acc_ed += time.time() - start_time
        if np.abs(iec-ed) > 0.0001:
            raise Exception(f'The difference is {np.abs(iec-ed[0][0])}')

    print('Irregular Euclidean Distance took', round(acc_ied, 2))
    print('Rregular Euclidean Distance took', round(acc_ed, 2))

    print('Test passed')


def test_matrix_profile_cython():
    np.random.seed(42)
    results = {'p': [], 'n': [], 'm': [], 'cr': [], 'time': [], 'it': []}
    # for p in [13]:
    for p in [15, 17, 20]:
        n = 2**p
        x = np.arange(n, dtype=int)
        y = np.round(np.random.rand(n), 2)
        # for m in [75]:
        for m in [75, 100, 125, 150]:
            for cr in [1, 0.2, 0.1, 0.05, 0.04, 0.03, 0.02, 0.01]:
            # for cr in [0.2]:
                for it in range(1):
                    if cr == 1:
                        sampled_x = x.copy()
                        sampled_y = y.copy()
                        start = time.time()
                        mpf.real_matrix_profile_caller(sampled_x, sampled_y, m)
                        end = time.time()
                    else:
                        sampling = int(n * cr)
                        r = np.empty((sampling + 2,), dtype=int)
                        r[0] = x[0]
                        r[-1] = x[-1]
                        r[1:-1] = np.sort(np.random.choice(x[1:-1], sampling, replace=False))
                        sampled_x = x[r]
                        sampled_y = y[r]
                        start = time.time()
                        mpf.matrix_profile_caller(sampled_x, sampled_y, m)
                        end = time.time()

                    results['cr'].append(round(1/cr, 2))
                    results['p'].append(p)
                    results['n'].append(n)
                    results['time'].append(round(end-start, 2))
                    results['m'].append(m)
                    results['it'].append(it)

                    print('It took', round(end-start, 2), 'seconds, for cr =', round(1/cr, 2), ', n =', n, ', m =', m, ', p =', p, 'it=', it)

            try:
                df = pd.DataFrame(results)
                df.to_csv('results/matrix_profile/running_time.csv')
            except Exception as e:
                print('There was an error writing down the dataframe, writing as a pickle.', e)
                with open('running_time.pkl', 'wb') as f:
                    pkl.dump(results, f)
            else:
                print('All good the file was stored :)')


if __name__ == "__main__":
    test_subseq_euclidean_distance()
