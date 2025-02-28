import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import seaborn as sns
import os
from matplotlib.colors import ListedColormap
custom_palette = sns.color_palette("light:#5A9")

custom_cmap = ListedColormap(custom_palette)

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

stan_ucr_results = np.loadtxt(os.path.join("results", "stan_ucr_results.txt"))
merlin_ucr_results = np.loadtxt(os.path.join("results", "merlin_ucr_results.txt"))

anomaly_types_concated = np.concatenate(list(anomaly_types.values()))

if anomaly_types_concated.shape[0] != 250:
    print("Anomaly types are not complete.")
    exit()

if stan_ucr_results.shape[0] != 250:
    print("Stan UCR results are not complete.")
    exit()

if merlin_ucr_results.shape[0] != 250:
    print("Merlin UCR results are not complete.")
    # exit()

stan_aggregates_statistics = defaultdict(int)
merlin_aggregates_statistics = defaultdict(int)

for i in range(stan_ucr_results.shape[0]):
    if stan_ucr_results[i] == 1:
        stan_aggregates_statistics[inverse_anomaly_types[i+1]] += 1
    if i < merlin_ucr_results.shape[0] and merlin_ucr_results[i] == 1:
        merlin_aggregates_statistics[inverse_anomaly_types[i+1]] += 1
    else:
        merlin_aggregates_statistics[inverse_anomaly_types[i+1]] += 0
    
stan_aggregates_statistics = dict(stan_aggregates_statistics)
merlin_aggregates_statistics = dict(merlin_aggregates_statistics)

anomaly_types_keys = list(anomaly_types.keys())
stan_aggregates = [stan_aggregates_statistics[key] for key in anomaly_types_keys]
merlin_aggregates = [merlin_aggregates_statistics[key] for key in anomaly_types_keys]

num_ref_anomalies = [len(anomaly_types[key]) for key in anomaly_types_keys]

df = pd.DataFrame({
    "type": anomaly_types_keys,
    "stan": stan_aggregates,
    "merlin": merlin_aggregates
})

ref_df = pd.DataFrame({
    "type": anomaly_types_keys,
    "stan": num_ref_anomalies,
    "merlin": num_ref_anomalies
})

df.set_index("type", inplace=True)
ref_df.set_index("type", inplace=True)

df = df/ref_df*100
df = df.round(0)
plt.figure(figsize=(4, 7))
hi = sns.heatmap(df, annot=True, fmt='g', cmap=custom_cmap, cbar_kws={"location":"right"})
hi.set_ylabel('Time Series Anomaly Type')
plt.tight_layout()
plt.savefig(os.path.join("results", "figures", "fig_4.png"))
plt.show()


