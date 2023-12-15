#!/usr/bin/env python3

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

benchmarks = ["imdb", "ssb", "ssb-skew"]

results = {}

for benchmark in benchmarks:
    # Calculate baseline intermediates
    path = f"{os.getcwd()}/experiment-results/2_1_enumeration_intms/dphyp-equisets/{benchmark}/bfs_min_card"
    files = glob.glob(os.path.join(path, "*.csv"))
    files.sort()
    print(len(files))

    duckdb_pipeline_intms = {}
    optimal_pipeline_intms = {}
    for file in files:
        query = "-".join(file.split("/")[-1].split("-")[:-1])
        df = pd.read_csv(file)
        duckdb_pipeline_intms[query] = df["path_0"].sum()
        optimal_pipeline_intms[query] = df.min(axis=1).sum()

    duckdb_query_intms = {}
    optimal_query_intms = {}
    for file in files:
        query_name = "-".join(file.split("/")[-1].split("-")[:-1])
        df = pd.read_csv(file)
        if query_name in duckdb_query_intms:
            duckdb_query_intms[query_name] += df["path_0"].sum()
            optimal_query_intms[query_name] += df.min(axis=1).sum()
        else:
            duckdb_query_intms[query_name] = df["path_0"].sum()
            optimal_query_intms[query_name] = df.min(axis=1).sum()

    path = f"{os.getcwd()}/experiment-results/3_1_pipeline/{benchmark}/default"
    files = glob.glob(os.path.join(path, "*.csv"))
    files.sort()

    polar_pp_durations = {}
    for csv_file in files:
        query_name = "-".join(csv_file.split("/")[-1].split("-")[0:-1])
        df = pd.read_csv(csv_file, names=["timing"])
        median_timing = float(df["timing"].median())
        if query_name in polar_pp_durations:
            polar_pp_durations[query_name] += median_timing / 1000
        else:
            polar_pp_durations[query_name] = median_timing / 1000

    path = os.getcwd() + f"/experiment-results/3_2_query/{benchmark}/duckdb.csv"

    query_durations = {}
    df = pd.read_csv(path, names=["name", "run", "timing"])
    df = df.groupby("name", as_index=False).median()

    for index, row in df.iterrows():
        query = str(row["name"]).split("/")[-1].split(".")[0]
        query_durations[query] = float(row["timing"])

    impacts = []
    for query in polar_pp_durations:
        non_polar = query_durations[query] - polar_pp_durations[query]
        if polar_pp_durations[query] > query_durations[query]:
            print(f"Warning: join pipeline took longer than query {query}: {query_durations[query]} vs {polar_pp_durations[query]}")
            non_polar = 0.01 * polar_pp_durations[query]
        if optimal_query_intms[query] == 0:
            if duckdb_query_intms[query] == 0:
                impacts.append(1)
                continue
            if non_polar == 0:
                print(f"Warning: join pipeline with originally {duckdb_query_intms[query]} intermediates could be reduced to zero.")
                continue # instead of appending infinity
            impacts.append(query_durations[query] / non_polar)
            continue
        reduction_factor = duckdb_query_intms[query] / optimal_query_intms[query]
        reduced_duration = non_polar + polar_pp_durations[query] / reduction_factor
        impacts.append(query_durations[query] / reduced_duration)
    results[benchmark] = {"default": duckdb_query_intms, "optimal": optimal_query_intms, "impacts": impacts}

print(results)

label_mapping = {"imdb": "JOB", "ssb": "SSB", "ssb-skew": "SSB-skew"}
color_mapping = {"imdb": "#f28522", "ssb": "#009ade", "ssb-skew": "#ff1f5b"}

plt.figure(figsize=(4.25, 1.8), constrained_layout=True)
for result_key in results:
    if len(results[result_key]["impacts"]) == 0:
        continue
    N = len(results[result_key]["impacts"])
    x = np.sort(results[result_key]["impacts"])
    y = np.arange(N) / float(N-1)
    plt.plot(x, y, label=label_mapping[result_key], color=color_mapping[result_key], marker="^", ms=4)

plt.xlabel("Potential improvement")
plt.ylabel("Fraction of queries")
plt.xscale("log")
plt.xticks(ticks=[1, 10], labels=["1x", "10x"])
plt.legend(frameon=False)
plt.savefig("paper/figures/1_3_potential_query_improvements.pdf")
