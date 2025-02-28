"""
Created on Tue Feb 20 17:00:00 2025

@Authors: Kriystian Blagov and Carlos E. Muñiz-Cuza 
@Copyright: Apache 2.0 License
""" 

import os
import sys
import time
from tqdm import tqdm
from collections import defaultdict
import numpy as np
import scipy.stats as st
import math
from statsmodels.tsa.stattools import acf
from scipy.signal import find_peaks
from sklearn.preprocessing import MinMaxScaler


sum_stat_results = defaultdict(int)

def dominant_fourier_freq(ts, min_size=10, max_size=500): #
    fourier = np.fft.fft(ts)
    freq = np.fft.fftfreq(ts.shape[0], 1)

    magnitudes = []
    window_sizes = []

    for coef, freq in zip(fourier, freq):
        if coef and freq > 0:
            window_size = int(1 / freq)
            mag = math.sqrt(coef.real * coef.real + coef.imag * coef.imag)

            if window_size >= min_size and window_size < max_size:
                window_sizes.append(window_size)
                magnitudes.append(mag)

    return window_sizes[np.argmax(magnitudes)]

def movmean(ts, w):
    """
    # faster solution of moving ave
    moving_avg = np.cumsum(ts, dtype=float)
    moving_avg[w:] = moving_avg[w:] - moving_avg[:-w]
    return moving_avg[w-1:] / w
    """
    moving_avg = np.cumsum(ts, dtype=float)
    moving_avg[w:] = moving_avg[w:] - moving_avg[:-w]
    return moving_avg[w - 1:] / w

def mwf(ts, lbound=10, ubound=500):
    """
    finidng appropriate window size using movemean
    """
    all_averages = []
    window_sizes = []

    for w in range(lbound, ubound, 1):
        movingAvg = np.array(movmean(ts, w))
        all_averages.append(movingAvg)
        window_sizes.append(w)

    movingAvgResiduals = []

    for i, w in enumerate(window_sizes):
        moving_avg = all_averages[i][:len(all_averages[-1])]
        movingAvgResidual = np.log(abs(moving_avg - (moving_avg).mean()).sum())
        movingAvgResiduals.append(movingAvgResidual)

    b = (np.diff(np.sign(np.diff(movingAvgResiduals))) > 0).nonzero()[0] + 1  # local min

    if len(b) == 0: return 10
    if len(b) < 3: return window_sizes[b[0]]

    reswin = np.array([window_sizes[b[i]] / (i + 1) for i in range(3)])
    w = np.mean(reswin)

    # w = 0.8 * reswin[0] + 0.15 * reswin[1] + 0.05 * reswin[2]
    # conf = np.std(reswin) / np.sqrt(3)

    return int(w)

def highest_acf(ts, min_size=10, max_size=1000):
    acf_values = acf(ts, fft=True, nlags=int(ts.shape[0] / 2))

    peaks, _ = find_peaks(acf_values)
    peaks = peaks[np.logical_and(peaks >= min_size, peaks < max_size)]
    corrs = acf_values[peaks]

    if len(peaks) == 0:
        peaks, _ = find_peaks(acf_values)
        peaks = peaks[np.logical_and(peaks >= min_size, peaks < 2000)]
        corrs = acf_values[peaks]

    if len(peaks) == 0:
        return -1

    return peaks[np.argmax(corrs)]

def count_direction_changes(subseq):
    count = 0
    direction = "unchanged"

    for i in range(1, len(subseq)):

        if subseq[i] - subseq[i - 1] > 0:
            new_direction = "up"
        elif subseq[i] - subseq[i - 1] < 0:
            new_direction = "down"
        else:
            new_direction = "unchanged"

        if new_direction != direction:
            count += 1

        direction = new_direction

    return count

def point_anomaly(subseq):
    return np.std(subseq)

def compute_largest_deviation(scaled_data, train_test_idx, period_length):
    if np.max(scaled_data[train_test_idx:]) - np.mean(scaled_data) >= np.mean(scaled_data) - np.min(
            scaled_data[train_test_idx:]):
        outlier = np.argmax(scaled_data[train_test_idx:]) + train_test_idx
    else:
        outlier = np.argmin(scaled_data[train_test_idx:]) + train_test_idx

    scaled_outlier = outlier * period_length + period_length / 2

    # sort_scaled = sorted(scaled_data[:train_test_idx])
    scaled_lower_bound = np.min(scaled_data[:train_test_idx]) 
    scaled_upper_bound = np.max(scaled_data[:train_test_idx])


    if scaled_data[outlier] > scaled_upper_bound:
        dev = scaled_data[outlier] - scaled_upper_bound
        outlier_idx = scaled_outlier

    elif scaled_data[outlier] < scaled_lower_bound:
        dev = scaled_lower_bound - scaled_data[outlier]
        outlier_idx = scaled_outlier

    else:
        dev = 0
        outlier_idx = scaled_outlier

    return dev, outlier_idx

def ucr_score(anomaly_idx, begin, end, length):
    return  min(begin-length,begin-100) < anomaly_idx < max(end+length, end+100)

def run_stan(ts, start_training, begin, end, anom_length, windows_func=highest_acf, statistics=None):
    deviations = []
    outlier_idx = []
    period_length = windows_func(ts)
    org_period_length = period_length
    data_original = ts
    data = np.diff(ts)
    if point_anomaly in statistics:
        E = [[] for _ in range(len(statistics) - 1)]
    else:
        E = [[] for _ in range(len(statistics))]

    for j in range(0, len(data), period_length):
        if j + period_length < len(data):
            counter = 0
            for statistic in statistics:
                if statistic.__name__ == "point_anomaly":
                    continue
                if statistic.__name__ == "count_direction_changes":
                    E[counter].append(statistic(data_original[j:j + period_length]))
                    counter += 1
                else:
                    E[counter].append(statistic(data[j:j + period_length]))
                    counter += 1

    p_anomaly_list = []
    for j in range(len(data)):
        if j % 3 == 0 and (j + 3) <= len(data):
            p_anomaly_list.append(np.std(data[j:j + 3]))

    counter = 0
    for statistic in statistics:
        if statistic.__name__ == "point_anomaly":
            period_length = 3
            data_to_scale = [[x] for x in p_anomaly_list]
        else:
            period_length = org_period_length
            data_to_scale = [[x] for x in E[counter]]
            counter += 1

        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(data_to_scale)
        scaled_data = scaled_data.flatten()

        # Index separating train and test data
        train_test_idx = math.floor(start_training / period_length)

        deviation, outlier_id = compute_largest_deviation(scaled_data, train_test_idx, period_length)
        deviations.append(deviation)
        outlier_idx.append(outlier_id)
        sum_stat_results[statistic.__name__] += ucr_score(outlier_id, begin, end, anom_length)

    # Return the anomaly index with the largest factor
    max_deviation = np.argmax(deviations)
    ult_outlier = outlier_idx[max_deviation]

    return int(ult_outlier), np.max(max_deviation)

def run_experiments_ucr(window_func=highest_acf, statistics=None):
    ucraa_root = os.path.join(os.getcwd(), "data", "ucraa")
    files = sorted([f for f in os.listdir(ucraa_root) if os.path.isfile(os.path.join(ucraa_root, f))])
    name_time_series_list = []
    time_series_list = []
    print("Loading data...")
    for file in tqdm(files):
        if file.endswith(".txt"):
            ts = np.fromfile(os.path.join(ucraa_root, file), sep="\n")
            if ts.shape[0] < 100:
                ts = np.fromfile(os.path.join(ucraa_root, file), sep=" ")
            time_series_list.append(ts)
            name_time_series_list.append(file)
    
    ucr_results = []
    start_time = time.time()
    idx = 0
    print("Detecting anomalies...")
    for ts in tqdm(time_series_list):
        ts_name = name_time_series_list[idx]
        parts = list(ts_name.split("_"))
        begin = int(parts[-2])
        end = int(parts[-1][:-4])
        start_training = int(parts[-3])
        anom_length = end-begin+1
        anomaly_idx, max_dev  = run_stan(ts, start_training, begin, end, anom_length, window_func, statistics)
        ucr_results.append(ucr_score(anomaly_idx, begin, end, anom_length))
        idx += 1
        
    end_time = time.time()
    runtime = end_time - start_time
    print("UCR-Score:", np.round(np.mean(ucr_results)*100, 2), f"% ({np.sum(ucr_results)}/250 correctly detected anomalies)")
    print("Total Runtime:", np.round(runtime, 2), "seconds")
    print("Runtime per Dataset:", np.round(runtime/250, 2), "seconds")
    print("Correctly detected anomalies per summary statistic:")
    print(sum_stat_results)

    if window_func.__name__ == "highest_acf":
        if len(statistics) == 8:
            np.savetxt(os.path.join(os.getcwd(), "results", "stan_ucr_results.txt"), ucr_results, fmt='%d')
            np.savetxt(os.path.join(os.getcwd(), "results", "stan_exec_time.txt"), np.array([np.round(runtime, 2), np.round(runtime/250, 2)]))
            with open(os.path.join(os.getcwd(), "results", "stan_aggregates_results.txt"), 'w') as f:
                for key, value in sum_stat_results.items():
                    f.write(f"{key}: {value}\n")
        elif len(statistics) > 1:
            np.savetxt(os.path.join(os.getcwd(), "results", f"stan_ucr_results_{'_'.join([stat.__name__ for stat in statistics])}.txt"), ucr_results, fmt='%d')
        else:
            np.savetxt(os.path.join(os.getcwd(), "results", f"stan_ucr_results_{statistics[0].__name__}.txt"), ucr_results, fmt='%d')
    else:
        np.savetxt(os.path.join(os.getcwd(), "results", f"stan_ucr_results_{window_func.__name__}.txt"), ucr_results, fmt='%d')
            
if __name__ == '__main__':
    arguments = sys.argv
    statistics = [np.std, np.min, np.max, st.kurtosis, st.skew, point_anomaly, count_direction_changes, np.mean]
    
    if len(arguments) == 1:
        run_experiments_ucr(window_func=highest_acf, statistics=statistics)
    else:
        if arguments[1] == "alternative":
            print("Running alternative window functions...")
            print("Running dominan_fourier_freq...")
            run_experiments_ucr(window_func=dominant_fourier_freq, statistics=statistics)
            print("Running mwf...")
            run_experiments_ucr(window_func=mwf, statistics=statistics)
        elif arguments[1] == 'aggregates':
            print("Running stan with aggregates individually...")
            for statistic in statistics:
                print(f"Running {statistic.__name__}...")
                run_experiments_ucr(window_func=highest_acf, statistics=[statistic])
        elif arguments[1] == 'incremental':
            print("Running stan with incremental added statistics...")
            for i in range(7, len(statistics)):
                print(f"Running with {' and '.join([stat.__name__ for stat in statistics[:i]])} statistics...")
                run_experiments_ucr(window_func=highest_acf, statistics=statistics[:i])
        else:
            print("Invalid argument. Please use 'alternative' or 'aggregates'")
            