#!/usr/bin/env python3

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

benchmarks = ["imdb", "ssb", "ssb-skew"]

results = []
for benchmark in benchmarks:
    # POLAR
    path = os.getcwd() + f"/experiment-results/4_1_endtoend/{benchmark}/polar/polar-generic-1.csv"
    df = pd.read_csv(path, names=["name", "run", "timing"])
    df = df.groupby("name", as_index=False).median()
    polar_timings = []
    for index, row in df.iterrows():
        query = str(row["name"]).split("/")[-1].split(".")[0]
        polar_timings.append(float(row["timing"]))

    # POLAR-8
    path = os.getcwd() + f"/experiment-results/4_1_endtoend/{benchmark}/polar/polar-generic-8.csv"
    df = pd.read_csv(path, names=["name", "run", "timing"])
    df = df.groupby("name", as_index=False).median()
    polar8_timings = []
    for index, row in df.iterrows():
        query = str(row["name"]).split("/")[-1].split(".")[0]
        polar8_timings.append(float(row["timing"]))

    # LIP
    path = os.getcwd() + f"/experiment-results/4_1_endtoend/{benchmark}/lip/lip-1.csv"
    df = pd.read_csv(path, names=["name", "run", "timing"])
    df = df.groupby("name", as_index=False).median()
    polar_untuned_timings = []
    for index, row in df.iterrows():
        query = str(row["name"]).split("/")[-1].split(".")[0]
        polar_untuned_timings.append(float(row["timing"]))

    # LIP
    path = os.getcwd() + f"/experiment-results/4_1_endtoend/{benchmark}/lip/lip-8.csv"
    df = pd.read_csv(path, names=["name", "run", "timing"])
    df = df.groupby("name", as_index=False).median()
    polar8_untuned_timings = []
    for index, row in df.iterrows():
        query = str(row["name"]).split("/")[-1].split(".")[0]
        polar8_untuned_timings.append(float(row["timing"]))

    # DuckDB
    path = os.getcwd() + f"/experiment-results/4_1_endtoend/{benchmark}/duckdb/duckdb-1.csv"
    df = pd.read_csv(path, names=["name", "run", "timing"])
    df = df.groupby("name", as_index=False).median()
    duckdb_timings = []
    for index, row in df.iterrows():
        query = str(row["name"]).split("/")[-1].split(".")[0]
        duckdb_timings.append(float(row["timing"]))

    # DuckDB-8
    path = os.getcwd() + f"/experiment-results/4_1_endtoend/{benchmark}/duckdb/duckdb-8.csv"
    df = pd.read_csv(path, names=["name", "run", "timing"])
    df = df.groupby("name", as_index=False).median()
    duckdb8_timings = []
    for index, row in df.iterrows():
        query = str(row["name"]).split("/")[-1].split(".")[0]
        duckdb8_timings.append(float(row["timing"]))

    if benchmark == "imdb":
        # SkinnerDB
        path = os.getcwd() + f"/experiment-results/4_1_endtoend/{benchmark}/skinnerdb/skinnerdb-1.csv"
        df = pd.read_csv(path)
        skinnerdb_timings = []
        for index, row in df.iterrows():
            skinnerdb_timings.append(float(row["Millis"]) / 1000)

        # SkinnerDB 8
        path = os.getcwd() + f"/experiment-results/4_1_endtoend/{benchmark}/skinnerdb/skinnerdb-8.csv"
        df = pd.read_csv(path)
        skinnerdb8_timings = []
        for index, row in df.iterrows():
            skinnerdb8_timings.append(float(row["Millis"]) / 1000)

        # SkinnerMT
        skinnermt_timings = []
        path = os.getcwd() + f"/experiment-results/4_1_endtoend/{benchmark}/skinnermt/skinnermt-1.csv"
        df = pd.read_csv(path)
        df = df.groupby("Query", as_index=False).median()
        for index, row in df.iterrows():
            skinnermt_timings.append(float(row["Millis"]) / 1000)

        # SkinnerMT 8
        skinnermt8_timings = []
        path = os.getcwd() + f"/experiment-results/4_1_endtoend/{benchmark}/skinnermt/skinnermt-8.csv"
        df = pd.read_csv(path)
        df = df.groupby("Query", as_index=False).median()
        for index, row in df.iterrows():
            skinnermt8_timings.append(float(row["Millis"]) / 1000)

    # Postgres
    path = os.getcwd() + f"/experiment-results/4_1_endtoend/{benchmark}/postgres/postgres-1.csv"
    df = pd.read_csv(path)
    df = df.groupby("query", as_index=False).median()
    postgres_timings = []
    for index, row in df.iterrows():
        postgres_timings.append(float(row["duration"]))

    # Postgres 8
    path = os.getcwd() + f"/experiment-results/4_1_endtoend/{benchmark}/postgres/postgres-8.csv"
    df = pd.read_csv(path)
    df = df.groupby("query", as_index=False).median()
    postgres8_timings = []
    for index, row in df.iterrows():
        postgres8_timings.append(float(row["duration"]))

    print(f"###{benchmark}###")
    print(f"POLAR-1: {sum(polar_timings)}")
    print(f"POLAR-8: {sum(polar8_timings)}")
    print(f"LIP-1: {sum(polar_untuned_timings)}")
    print(f"LIP-8: {sum(polar8_untuned_timings)}")
    print(f"DuckDB-1: {sum(duckdb_timings)}")
    print(f"DuckDB-8: {sum(duckdb8_timings)}")
    print(f"SkinnerDB-1: {sum(skinnerdb_timings)}")
    print(f"SkinnerDB-8: {sum(skinnerdb8_timings)}")
    print(f"SkinnerMT-1: {sum(skinnermt_timings)}")
    print(f"SkinnerMT-8: {sum(skinnermt8_timings)}")
    print(f"Postgres-1: {sum(postgres_timings)}")
    print(f"Postgres-8: {sum(postgres8_timings)}")

    if benchmark == "imdb":
        timings = {
            'POLAR': [sum(polar_timings), sum(polar8_timings)],
            'LIP': [sum(polar_untuned_timings), sum(polar8_untuned_timings)],
            'DuckDB': [sum(duckdb_timings), sum(duckdb8_timings)],
            'SkinnerMT': [sum(skinnermt_timings), sum(skinnermt8_timings)],
            'SkinnerDB': [sum(skinnerdb_timings), sum(skinnerdb8_timings)],
            'Postgres': [sum(postgres_timings), sum(postgres8_timings)]
        }
    else:
        timings = {
            'POLAR': [sum(polar_timings), sum(polar8_timings)],
            'LIP': [sum(polar_untuned_timings), sum(polar8_untuned_timings)],
            'DuckDB': [sum(duckdb_timings), sum(duckdb8_timings)],
            'Postgres': [sum(postgres_timings), sum(postgres8_timings)]
        }
    results.append(timings)

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
    x = np.arange(len(threads))  # the label locations
    width = 0.14  # the width of the bars
    multiplier = 0

    timings = results[i]
    for attribute, measurement in timings.items():
        offset = width * multiplier
        print(attribute + " " + str(measurement) + " " + str(offset))
        rects = ax[i].bar(x + offset, measurement, width, label=attribute, color=bar_colors[attribute])
        if measurement[0] >= 100:
            ax[i].bar_label(rects, padding=0, fmt="{:3.0f}", fontsize=7)
        else:
            ax[i].bar_label(rects, padding=0, fmt="{:3.1f}", fontsize=7)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    if benchmarks[i] == "imdb":
        ax[i].set_xticks(x + 2 * width, threads)
    else:
        ax[i].set_xticks(x + 1.5 * width, threads)
    ax[i].set_title(titles[benchmarks[i]])
    # max_skinner = max(list(results[i]["SkinnerMT"]))
    max_postgres = max(list(results[i]["Postgres"]))
    ylimt = max(0, max_postgres) * 1.1
    ax[i].set_ylim(bottom=0, top=ylimt)

    if i == 0:
        handles, labels = ax[i].get_legend_handles_labels()
        fig.legend(handles, labels, loc='outside right center', frameon=False)

fig.supxlabel('Threads')
fig.supylabel('Total execution time (s)')

plt.savefig("paper/figures/4_1_total.pdf")
plt.clf()
