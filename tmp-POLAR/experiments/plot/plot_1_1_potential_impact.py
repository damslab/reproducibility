#!/usr/bin/env python3

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

benchmarks = ["imdb", "ssb", "ssb-skew"]
results = {}

for benchmark in benchmarks:
    results[benchmark] = {}
    path = os.getcwd() + f"/experiment-results/1_1_potential_impact/{benchmark}/pipelines"
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

    results[benchmark]["pipelines"] = timings
    path = os.getcwd() + f"/experiment-results/1_1_potential_impact/{benchmark}/queries"
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    if len(csv_files) != 1:
        print(f"Warning: no results for {path}")
        results[benchmark]["queries"] = 0
        continue

    df = pd.read_csv(csv_files[0], names=["name", "run", "timing"])
    total_time = float(df.groupby("name").median()["timing"].sum())
    results[benchmark]["queries"] = total_time

print(results)

polar_times = []
for benchmark in results:
    if results[benchmark]["queries"] == 0:
        polar_times.append(0)
        continue
    polar_times.append(max(1, sum(results[benchmark]["pipelines"]) / results[benchmark]["queries"]))
print(polar_times)

# TODO Get intermediates
