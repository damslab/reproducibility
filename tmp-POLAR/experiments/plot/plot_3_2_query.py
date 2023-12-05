#!/usr/bin/env python3
import pandas
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np

benchmarks = ["imdb", "ssb", "ssb-skew"]
regret_budgets = ["0.0001", "0.001", "0.01", "0.1"]
# Exclude as no containing POLAR pipelines
excluded = {"imdb": ["02a", "02b", "02c", "02d",
                     "04a", "04b", "04c",
                     "06a", "06c", "06e",
                     "07a", "07b", "07c",
                     "08a", "08b",
                     "09b",
                     "11a", "11b",
                     "12a", "12c",
                     "15b",
                     "16a", "16b", "16c", "16d",
                     "17a", "17b", "17c", "17d", "17e", "17f",
                     "19b",
                     "21a", "21b", "21c",
                     "25a", "25b",
                     "27a", "27b", "27c",
                     "28c",
                     "32a", "32b"],
            "ssb": ["q1-1", "q1-2", "q1-3"],
            "ssb-skew": []}

results = {}

for benchmark in benchmarks:
    all_polar_timings = {}
    for budget in regret_budgets:
        path = os.getcwd() + f"/experiment-results/3_2_query/{benchmark}/{budget}/polar.csv"

        polar_timings = []
        df = pd.read_csv(path, names=["name", "run", "timing"])
        df = df.groupby("name", as_index=False).median()

        for index, row in df.iterrows():
            query = row["name"].split("/")[-1].split(".")[0]
            if query in excluded[benchmark]:
                continue

            polar_timings.append(float(row["timing"]))
        all_polar_timings[budget] = polar_timings

    path = os.getcwd() + f"/experiment-results/3_2_query/{benchmark}/duckdb.csv"

    duckdb_timings = []
    df = pd.read_csv(path, names=["name", "run", "timing"])
    df = df.groupby("name", as_index=False).median()

    for index, row in df.iterrows():
        query = row["name"].split("/")[-1].split(".")[0]
        if query in excluded[benchmark]:
            continue

        duckdb_timings.append(float(row["timing"]))

    results[benchmark] = {"polar": all_polar_timings, "duckdb": duckdb_timings}

budget_mapping = {"imdb": "0.001", "ssb": "0.001", "ssb-skew": "0.001"}
titles = {"imdb": "JOB", "ssb": "SSB", "ssb-skew": "SSB-skew"}

loc = plticker.MultipleLocator(base=1.0)

fig = plt.figure(figsize=(12, 4), constrained_layout=True)
subfigs = fig.subfigures(nrows=2, ncols=1)

for row, subfig in enumerate(subfigs):
    title = ""

    if row == 0:
        title = "Tuned"
    else:
        title = "Generic"

    subfig.suptitle(title, fontweight="bold")
    ax = subfig.subplots(nrows=1, ncols=len(benchmarks))

    for i in range(len(benchmarks)):
        benchmark = benchmarks[i]
        polar_timings = []

        if row == 0:
            polar_timings = results[benchmark]["polar"][budget_mapping[benchmark]]
        else:
            polar_timings = results[benchmark]["polar"]["0.001"]
        duckdb_timings = results[benchmark]["duckdb"]

        rel = []
        for j in range(len(polar_timings)):
            pt = polar_timings[j]
            dt = duckdb_timings[j]
            if (pt - dt) / dt < -0.5:
                print(f"{j} | DuckDB: {dt}, POLAR: {pt}, {(dt / pt) - 1}")

            if pt <= dt:
                rel.append((dt / pt) - 1)
            else:
                if (dt - pt) / dt < -0.1:
                    print(f"{j} | DuckDB: {dt}, POLAR: {pt}")
                rel.append((dt - pt) / dt)

        df = pd.DataFrame({"rel": sorted(rel)})
        mask1 = df["rel"] < 0
        mask2 = df["rel"] >= 0

        if row == 0 and i == 2:
            ax[i].bar(df.index[mask2], df["rel"][mask2], color="#00b000", label="Speedup")
            ax[i].bar(df.index[mask1], df["rel"][mask1], color="#e9002d", label="Slowdown")
            handles, labels = ax[i].get_legend_handles_labels()
            leg = fig.legend(handles, labels, loc='outside right center', frameon=False)
            leg.legend_handles[1].set_color('#e9002d')
        else:
            ax[i].bar(df.index[mask2], df["rel"][mask2], color="#00b000")
            ax[i].bar(df.index[mask1], df["rel"][mask1], color="#e9002d")

        if benchmark == "ssb-skew":
            ax[i].set_ylim(bottom=-0.1)
        elif benchmark == "imdb":
            ax[i].yaxis.set_ticks([0,2,4,6,8])
        #elif benchmark == "ssb" and row == 1:
        #    ax[i].set_ylim(bottom=-0.35, top=0.1)

        ax[i].grid(axis="y", alpha=0.5)
        ax[i].set_xticks(np.arange(len(df)), labels=[])
        ax[i].axhline(0, color="black", lw=1)

        if row == 0:
            ax[i].set_title(titles[benchmark])

fig.supxlabel('Queries')
fig.supylabel('Speedup/Slowdown Factor')
plt.savefig("paper/figures/3_2_rel_gains.pdf")

results = {}

for benchmark in benchmarks:
    all_polar_timings = {}
    for budget in regret_budgets:
        path = os.getcwd() + f"/experiment-results/3_2_query/{benchmark}/{budget}/polar.csv"

        polar_timings = []
        df = pd.read_csv(path, names=["name", "run", "timing"])
        df = df.groupby("name", as_index=False).median()

        for index, row in df.iterrows():
            polar_timings.append(float(row["timing"]))
        all_polar_timings[budget] = polar_timings

    path = os.getcwd() + f"/experiment-results/3_2_query/{benchmark}/duckdb.csv"

    duckdb_timings = []
    df = pd.read_csv(path, names=["name", "run", "timing"])
    df = df.groupby("name", as_index=False).median()

    for index, row in df.iterrows():
        duckdb_timings.append(float(row["timing"]))

    results[benchmark] = {"polar": all_polar_timings, "duckdb": duckdb_timings}

tuned_results = {}
for benchmark in benchmarks:
    tet = sum(results[benchmark]["polar"]["0.0001"])
    maximum = max(results[benchmark]["polar"]["0.0001"])
    for budget in regret_budgets:
        if tet > sum(results[benchmark]["polar"][budget]):
            tet = sum(results[benchmark]["polar"][budget])
            maximum = max(results[benchmark]["polar"][budget])
    tuned_results[benchmark] = {"tet": tet, "max": maximum}

formatted_results = {}
for benchmark in benchmarks:
    formatted_results[benchmark] = {"duckdb": {}, "generic": {}, "tuned": {}, "speedup": {}}
    formatted_results[benchmark]["duckdb"]["tet"] = "{:5.1f}".format(sum(results[benchmark]["duckdb"]))
    formatted_results[benchmark]["duckdb"]["max"] = "{:5.1f}".format(max(results[benchmark]["duckdb"]))
    formatted_results[benchmark]["generic"]["tet"] = "{:5.1f}".format(sum(results[benchmark]["polar"]["0.001"]))
    formatted_results[benchmark]["generic"]["max"] = "{:5.1f}".format(max(results[benchmark]["polar"]["0.001"]))
    formatted_results[benchmark]["tuned"]["tet"] = "{:5.1f}".format(tuned_results[benchmark]["tet"])
    formatted_results[benchmark]["tuned"]["max"] = "{:5.1f}".format(tuned_results[benchmark]["max"])
    formatted_results[benchmark]["speedup"]["tet"] = "{:5.2f}".format(sum(results[benchmark]["duckdb"]) / tuned_results[benchmark]["tet"]) + "x"
    formatted_results[benchmark]["speedup"]["max"] = "{:5.2f}".format(max(results[benchmark]["duckdb"]) / tuned_results[benchmark]["max"]) + "x"

latex_table = f"""\\begin{{table}}
  \\centering
  \\caption{{Overall Performance Impact -- Single-threaded total execution time, and max execution time per query [seconds].}}
  \\vspace{{-0.3cm}} \\setlength\\tabcolsep{{3.7pt}}
  \\begin{{tabular}}{{lcccccc}}
    \\toprule
    & \\multicolumn{{3}}{{c}}{{\\textbf{{Total Execution Time}}}} & \\multicolumn{{3}}{{c}}{{\\textbf{{Max. Query Time}}}}\\\\
    & JOB & SSB & SSB-skew & JOB & SSB & SSB-skew\\\\
    \\midrule
    DuckDB & {formatted_results["imdb"]["duckdb"]["tet"]} & {formatted_results["ssb"]["duckdb"]["tet"]} & {formatted_results["ssb-skew"]["duckdb"]["tet"]} & {formatted_results["imdb"]["duckdb"]["max"]} & {formatted_results["ssb"]["duckdb"]["max"]} & {formatted_results["ssb-skew"]["duckdb"]["max"]}\\\\
    POLAR-G & {formatted_results["imdb"]["generic"]["tet"]} & {formatted_results["ssb"]["generic"]["tet"]} & {formatted_results["ssb-skew"]["generic"]["tet"]} & {formatted_results["imdb"]["generic"]["max"]} & {formatted_results["ssb"]["generic"]["max"]} & {formatted_results["ssb-skew"]["generic"]["max"]}\\\\
    POLAR-T & \\textbf{{{formatted_results["imdb"]["tuned"]["tet"]}}} & \\textbf{{{formatted_results["ssb"]["tuned"]["tet"]}}} & \\textbf{{{formatted_results["ssb-skew"]["tuned"]["tet"]}}} & \\textbf{{{formatted_results["imdb"]["tuned"]["max"]}}} & \\textbf{{{formatted_results["ssb"]["tuned"]["max"]}}} & \\textbf{{{formatted_results["ssb-skew"]["tuned"]["max"]}}}\\\\
    Speedup & {formatted_results["imdb"]["speedup"]["tet"]} & {formatted_results["ssb"]["speedup"]["tet"]} & \\textbf{{\\color{{red}}{formatted_results["ssb-skew"]["speedup"]["tet"]}}} & \\textbf{{\\color{{red}}{formatted_results["imdb"]["speedup"]["max"]}}} & {formatted_results["ssb"]["speedup"]["max"]} & \\textbf{{\\color{{red}}{formatted_results["ssb-skew"]["speedup"]["max"]}}}\\\\
    \\bottomrule
  \\end{{tabular}}
  \\label{{tab:3_4_endtoend}}
\\end{{table}}
"""

with open("paper/tables/3_4_endtoend.tex", "w") as file:
    file.write(latex_table)
