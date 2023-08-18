#!/usr/bin/env python3

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

optimizer_modes = ["dphyp-equisets"]
benchmarks = ["imdb", "ssb", "ssb-skew"]
raw_results = {}

for benchmark in benchmarks:
    for mode in optimizer_modes:
        raw_results[f"{benchmark}-{mode[:2]}"] = {}
        path = os.getcwd() + f"/experiment-results/1_1_potential_impact/{mode}/{benchmark}/pipelines"
        csv_files = glob.glob(os.path.join(path, "*.csv"))
        if len(csv_files) == 0:
            print(f"Warning: no results for {path}")

        timings = []
        for csv_file in csv_files:
            df = pd.read_csv(csv_file, names=["timing"])
            median_timing = float(df["timing"].median())
            timings.append(median_timing / 1000)

        if len(timings) == 0:
            timings.append(0)
        raw_results[f"{benchmark}-{mode[:2]}"]["pipelines"] = timings

        path = os.getcwd() + f"/experiment-results/1_1_potential_impact/{mode}/{benchmark}/queries"
        csv_files = glob.glob(os.path.join(path, "*.csv"))
        if len(csv_files) != 1:
            print(f"Warning: no results for {path}")
            raw_results[f"{benchmark}-{mode[:2]}"]["queries"] = 0
            continue

        df = pd.read_csv(csv_files[0], names=["name", "run", "timing"])
        total_time = float(df.groupby("name").median()["timing"].sum())
        raw_results[f"{benchmark}-{mode[:2]}"]["queries"] = total_time

print(raw_results)

total_times = []
polar_times = []
for result_key in raw_results:
    if raw_results[result_key]["queries"] == 0:
        total_times.append(0)
        polar_times.append(0)
        continue
    print(f"({raw_results[result_key]['queries']} - {sum(raw_results[result_key]['pipelines'])}) / {raw_results[result_key]['queries']}")
    total_time = max((raw_results[result_key]["queries"] - sum(raw_results[result_key]["pipelines"])) / raw_results[result_key]["queries"], 0)
    total_times.append(total_time)
    polar_times.append(1 - total_time)

print(total_times)
print(polar_times)


plt.bar(benchmarks, polar_times, color="#009ade")

# fig, ax = plt.subplots()
# bottom = np.zeros(len(raw_results.keys()))
# ax.bar(list(raw_results.keys()), total_times, 0.5, label="not applicable", bottom=bottom)
# bottom += total_times
# ax.bar(list(raw_results.keys()), polar_times, 0.5, label="POLAR-applicable", bottom=bottom)
# ax.set_ylabel("% of execution time spent in pipeline")
# for tick in ax.get_xticklabels():
#     tick.set_rotation(90)
# ax.legend(loc="upper right")

plt.tight_layout()
plt.savefig("experiment-results/1_1_potential_impact.pdf")

