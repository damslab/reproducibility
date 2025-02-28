import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import seaborn as sns
import os
from matplotlib.colors import ListedColormap
custom_palette = sns.color_palette("light:#5A9")

custom_cmap = ListedColormap(custom_palette)

statistics: list[str] = ['min', 'max', 'mean', 'std', 'skew', 'kurtosis', 'count_direction_changes', 'point_anomaly']

anomaly_types: dict[str, list[int]] = {
    "amplitude_change": [13, 14, 37, 42, 44, 53, 57, 66, 91, 100, 104, 121, 122, 145, 150, 152, 161, 165, 174, 199, 205, 206, 207, 215, 217],
    "flat": [45, 78, 110, 153, 186, 236],
    "freq_change": [23, 26, 32, 33, 34, 40, 48, 99, 101, 131, 134, 140, 141, 142, 148, 156, 202, 222, 223, 224, 227, 228, 229, 244, 245, 246, 247],
    "local_drop": [5, 43, 54, 63, 77, 86, 92, 102, 106, 113, 151, 162, 171, 185, 194, 200, 232, 233, 237, 238],
    "local_peak": [7, 21, 24, 25, 30, 49, 62, 64, 85, 89, 97, 115, 129, 132, 133, 138, 157, 170, 172, 193, 197, 234, 235, 239, 243],
    "missing_drop": [2, 72, 180],
    "missing_peak": [4, 19, 35, 36, 59, 60, 94, 112, 127, 143, 144, 167, 168, 248],
    "noise": [3, 8, 27, 28, 29, 39, 56, 67, 68, 83, 95, 98, 107, 111, 116, 135, 136, 137, 147, 164, 175, 176, 191],
    "outlier_datasets": [11, 12, 15, 18, 70, 71, 84, 119, 120, 123, 126, 178, 179, 192, 213, 216, 220, 226],
    "reverse": [20, 22, 38, 52, 55, 65, 90, 103, 128, 130, 146, 160, 163, 173, 198, 201, 203, 209, 212, 225, 230, 242, 249],
    "reverse_horizontal": [16, 17, 58, 96, 124, 125, 166, 231],
    "sampling_rate": [50, 61, 105, 158, 169],
    "signal_shift": [204],
    "smoothed_increase": [241],
    "steep_increase": [51, 159],
    "time_shift": [69, 74, 75, 79, 80, 81, 82, 87, 88, 108, 177, 182, 183, 187, 188, 189, 190, 195, 196, 208],
    "time_warping": [31, 76, 139, 184],
    "unusual_pattern": [1, 6, 9, 10, 41, 46, 47, 73, 93, 109, 114, 117, 118, 149, 154, 155, 181, 210, 211, 214, 218, 219, 221, 240, 250]
}

inverse_anomaly_types = {v: k for k, values in anomaly_types.items() for v in values}

anomaly_types_concated = np.concatenate(list(anomaly_types.values()))

anomaly_types_keys = list(anomaly_types.keys())

num_ref_anomalies = [len(anomaly_types[key]) for key in anomaly_types_keys]

ref_df = pd.DataFrame({
    "type": anomaly_types_keys,
    "total": num_ref_anomalies,
})
ref_df.set_index("type", inplace=True)


def collect_statistic_results(statistic):
    try:
        statistic_results = np.loadtxt(os.path.join("results", f"stan_ucr_results_{statistic}.txt"))
    except:
        print(f"UCR results for {statistic} are not complete.")
        print("Run stan.py aggregates to generate the ucr results.")
        exit()
    statistics_map = defaultdict(int)
    for i in range(statistic_results.shape[0]):
        statistics_map[inverse_anomaly_types[i+1]] += statistic_results[i]
    statistics_map = dict(statistics_map)

    anomaly_types_keys = list(anomaly_types.keys())
    statistics_aggregates = [statistics_map[key] for key in anomaly_types_keys]

    return {statistic: statistics_aggregates}


if __name__ == '__main__':
    all_results = pd.DataFrame({"type": anomaly_types_keys})

    for statistic in statistics:
        statistics_map = collect_statistic_results(statistic)
        all_results = pd.concat([all_results, pd.DataFrame(statistics_map)], axis=1)
        

    all_results.set_index("type", inplace=True)
    all_results = all_results/ref_df.values*100
    all_results = all_results.round(0)
    plt.figure(figsize=(4, 7))
    hi = sns.heatmap(all_results, annot=True, fmt='g', cmap=custom_cmap, cbar_kws={"location":"right"})
    hi.set_ylabel('Time Series Anomaly Type')
    plt.tight_layout()
    plt.savefig(os.path.join("results", "figures", "fig_5.png"))
    plt.show()


