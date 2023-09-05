#!/usr/bin/env python3

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

benchmarks = ["imdb", "ssb", "ssb-skew"]

results = {}

for benchmark in benchmarks:
    # Get pipeline names
    pipeline_names = []
    path = f"{os.getcwd()}/experiment-results/1_1_potential_impact/{benchmark}/pipelines"
    files = glob.glob(os.path.join(path, "*.csv"))
    files.sort()

    for file in files:
        pipeline_names.append(file.split("/")[-1].split(".")[0])
    print(pipeline_names)

    # Calculate baseline intermediates
    path = f"{os.getcwd()}/experiment-results/2_1_enumeration_intms/dphyp-equisets/{benchmark}/bfs_min_card"
    files = glob.glob(os.path.join(path, "*.csv"))
    files.sort()
    print(len(files))
    print(len(pipeline_names))
    assert(len(files) == len(pipeline_names))

    duckdb_pipeline_intms = {}
    optimal_pipeline_intms = {}
    for i in range(len(files)):
        file = files[i]
        df = pd.read_csv(file)
        duckdb_pipeline_intms[pipeline_names[i]] = df["path_0"].sum()
        optimal_pipeline_intms[pipeline_names[i]] = df.min(axis=1).sum()

    # Flatten
    duckdb_query_intms = {}
    optimal_query_intms = {}
    for pipeline_name in pipeline_names:
        query_name = "-".join(pipeline_name.split("-")[:-1])
        if query_name in duckdb_query_intms:
            duckdb_query_intms[query_name] += duckdb_pipeline_intms[pipeline_name]
            optimal_query_intms[query_name] += optimal_pipeline_intms[pipeline_name]
        else:
            duckdb_query_intms[query_name] = duckdb_pipeline_intms[pipeline_name]
            optimal_query_intms[query_name] = optimal_pipeline_intms[pipeline_name]

    path = f"{os.getcwd()}/experiment-results/1_1_potential_impact/{benchmark}/pipelines"
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

    path = os.getcwd() + f"/experiment-results/1_1_potential_impact/{benchmark}/queries"
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    query_durations = {}
    df = pd.read_csv(csv_files[0], names=["name", "run", "timing"])
    df = df.groupby("name", as_index=False).median()

    for index, row in df.iterrows():
        query = str(row["name"]).split("/")[-1].split(".")[0]
        query_durations[query] = float(row["timing"])

    impacts = []
    for query in polar_pp_durations:
        non_polar = query_durations[query] - polar_pp_durations[query]
        if polar_pp_durations[query] > query_durations[query]:
            print(f"Warning: join pipeline took longer than query {query}: {query_durations[query]} vs {polar_pp_durations[query]}")
            non_polar = query_durations[query] * 0.1
        if optimal_query_intms[query] == 0:
            impacts.append(query_durations[query] / non_polar)
            continue
        reduction_factor = duckdb_query_intms[query] / optimal_query_intms[query]
        reduced_duration = non_polar + polar_pp_durations[query] / reduction_factor
        impacts.append(query_durations[query] / reduced_duration)
    results[benchmark] = {"default": duckdb_query_intms, "optimal": optimal_query_intms, "impacts": impacts}

print(results)
columns = ["default", "optimal", "best_in_class"]
result_str = "\\begin{table}\n\t\\centering\n\t\\begin{tabular}{l"

for i in range(len(columns)):
    result_str += "r"

result_str += "}\n\t\t"
result_str += "\\textbf{Benchmark}"

for column in columns:
    result_str += " & " + column.replace("_", " ")

result_str += "\\\\\n\t\t"
result_str += "\\hline\n\t\t"

enumerators = list(results[list(results.keys())[0]].keys())

for result_key in results:
    result_str += result_key
    for column in columns:
        sum_intermediates = sum(results[result_key][column].values())
        if column == "optimal" and result_key == "imdb-gr":
            result_str += " & " + "{:10.2f}".format(sum_intermediates / 1000000) + "* M"
        else:
            result_str += " & " + "{:10.2f}".format(sum_intermediates / 1000000) + " M"
    result_str += "\\\\\n\t\t"

result_str += "\\hline\n\t\\end{tabular}\n\t\\caption{"
result_str += "Total number of intermediates for POLAR pipelines with optimal routing strategies"
result_str += "}\n\t\\label{"
result_str += "tab:1_2_potential_savings"
result_str += "}\n\\end{table}\n"

with open("experiment-results/1_2_potential_savings.txt", "w") as file:
    file.write(result_str)

label_mapping = {"imdb-dp": "JOB", "ssb-dp": "SSB", "ssb-skew-dp": "SSB-skew"}
color_mapping = {"imdb-dp": "#f28522", "ssb-dp": "#009ade", "ssb-skew-dp": "#ff1f5b"}

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
plt.xticks(ticks=[1, 10, 100], labels=["1x", "10x", "100x"])
plt.legend(frameon=False)
plt.savefig("experiment-results/1_3_potential_query_improvements.pdf")