#!/usr/bin/env python3

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42

threads = ["1", "8"]
benchmarks = ["imdb", "ssb", "ssb-skew"]
system_names = {"polar": "POLAR", "lip": "LIP", "duckdb": "DuckDB", "skinnermt": "SkinnerMT", "skinnerdb": "SkinnerDB",
                "postgres": "Postgres"}

results = []
for benchmark in benchmarks:
    benchmark_results = {}
    for system in ["polar", "lip", "duckdb"]:
        benchmark_results[system_names[system]] = []
        for nthreads in threads:
            path = os.getcwd() + f"/experiment-results/4_1_endtoend/{benchmark}/{system}/{system}-{nthreads}.csv"
            df = pd.read_csv(path, names=["name", "run", "timing"])
            df = df.groupby("name", as_index=False).median()
            timings = []
            for index, row in df.iterrows():
                query = str(row["name"]).split("/")[-1].split(".")[0]
                timings.append(float(row["timing"]))
            benchmark_results[system_names[system]].append(sum(timings))

    for system in ["postgres"]:
        benchmark_results[system_names[system]] = []
        for nthreads in threads:
            path = os.getcwd() + f"/experiment-results/4_1_endtoend/{benchmark}/{system}/{system}-{nthreads}.csv"
            df = pd.read_csv(path)
            df = df.groupby("query", as_index=False).median()
            timings = []
            for index, row in df.iterrows():
                timings.append(float(row["duration"]))
            benchmark_results[system_names[system]].append(sum(timings))

    for system in ["skinnerdb", "skinnermt"]:
        if benchmark != "imdb":
            break
        benchmark_results[system_names[system]] = []
        for nthreads in threads:
            path = os.getcwd() + f"/experiment-results/4_1_endtoend/{benchmark}/{system}/{system}-{nthreads}.csv"
            df = pd.read_csv(path)
            timings = []
            for index, row in df.iterrows():
                timings.append(float(row["Millis"]) / 1000)
            benchmark_results[system_names[system]].append(sum(timings))

    results.append(benchmark_results)

fig, ax = plt.subplots(1, len(benchmarks), figsize=(13, 2.5), constrained_layout=True)
bar_colors = {
    "POLAR": "#ff1f5b",
    "LIP": "#00cd6c",
    "DuckDB": "#ffc61e",
    "SkinnerMT": "#af58ba",
    "SkinnerDB": "#009ade",
    "Postgres": "#f28522"
}

titles = {"imdb": "JOB", "ssb": "SSB", "ssb-skew": "SSB-skew"}

for i in range(len(benchmarks)):
    threads = [1, 8]
    x = np.arange(len(threads))
    width = 0.14
    multiplier = 0

    timings = results[i]
    for attribute, measurement in timings.items():
        offset = width * multiplier
        print(attribute + " " + str(measurement) + " " + str(offset))
        rects = ax[i].bar(x + offset, measurement, width, label=attribute, color=bar_colors[attribute])
        ax[i].bar_label(rects, padding=0, fmt="{:3.0f}", fontsize=7)
        multiplier += 1

    if benchmarks[i] == "imdb":
        ax[i].set_xticks(x + 2 * width, threads)
    else:
        ax[i].set_xticks(x + 1.5 * width, threads)
    ax[i].set_title(titles[benchmarks[i]])

    max_postgres = max(list(results[i]["Postgres"]))
    max_skinner = 0
    if benchmarks[i] == "imdb":
        max_skinner = max(list(results[i]["SkinnerDB"]))
    max_duckdb = max(list(results[i]["DuckDB"]))
    max_polar = max(list(results[i]["POLAR"]))
    ylimt = max(max_skinner, max_postgres, max_duckdb) * 1.1
    ax[i].set_ylim(bottom=0, top=ylimt)

    if i == 0:
        handles, labels = ax[i].get_legend_handles_labels()
        fig.legend(handles, labels, loc='outside right center', frameon=False)

fig.supxlabel('Number of Threads')
fig.supylabel('Total Execution Time (s)')

plt.savefig("paper/figures/4_1_total.pdf")
plt.clf()
