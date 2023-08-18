#!/usr/bin/env python3

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

optimizer_modes = ["dphyp-equisets"]
benchmarks = ["imdb", "ssb", "ssb-skew"]

results = {}

for benchmark in benchmarks:
    for optimizer_mode in optimizer_modes:
        print(benchmark + "-" + optimizer_mode[:2])
        # Calculate baselines from exhaustive
        path = f"{os.getcwd()}/experiment-results/1_2_potential_savings/{optimizer_mode}/{benchmark}"
        csv_files = glob.glob(os.path.join(path, "*.csv"))
        csv_files.sort()

        default = {}
        exhaustive = {}
        best_in_class = {}
        worst_in_class = {}

        for csv_file in csv_files:
            # TODO: Does not work for ssb
            query_name = "-".join(csv_file.split("/")[-1].split("-")[0:-1])
            df = pd.read_csv(csv_file)
            df.pop(df.columns[-1])

            if query_name in default:
                default[query_name] += (df["path_0"].sum())
                exhaustive[query_name] += (df.min(axis=1).sum())
                best_in_class[query_name] += (df.sum().min())
                worst_in_class[query_name] += (df.sum().max())
            else:
                default[query_name] = (df["path_0"].sum())
                exhaustive[query_name] = (df.min(axis=1).sum())
                best_in_class[query_name] = (df.sum().min())
                worst_in_class[query_name] = (df.sum().max())

        print(exhaustive)

        path = os.getcwd() + f"/experiment-results/1_1_potential_impact/{optimizer_mode}/{benchmark}/pipelines"
        csv_files = glob.glob(os.path.join(path, "*.csv"))
        csv_files.sort()
        if len(csv_files) == 0:
            print(f"Warning: no results for {path}")

        polar_pp_durations = {}
        for csv_file in csv_files:
            # TODO
            query_name = "-".join(csv_file.split("/")[-1].split("-")[0:-1])
            df = pd.read_csv(csv_file, names=["timing"])
            median_timing = float(df["timing"].median())
            if query_name in polar_pp_durations:
                polar_pp_durations[query_name] += median_timing / 1000
            else:
                polar_pp_durations[query_name] = median_timing / 1000

        path = os.getcwd() + f"/experiment-results/1_1_potential_impact/{optimizer_mode}/{benchmark}/queries"
        csv_files = glob.glob(os.path.join(path, "*.csv"))
        if len(csv_files) != 1:
            print(f"Warning: no results for {path}")

        query_durations = {}
        df = pd.read_csv(csv_files[0], names=["name", "run", "timing"])
        df = df.groupby("name", as_index=False).median()

        for index, row in df.iterrows():
            query = str(row["name"]).split("/")[-1].split(".")[0]
            query_durations[query] = float(row["timing"])

        impacts = []
        for query in polar_pp_durations:
            if query not in exhaustive:
                print(f"Warning: query {query} missing.")
                continue
            non_polar = query_durations[query] - polar_pp_durations[query] # TODO: Subtract scan time
            if polar_pp_durations[query] > query_durations[query]:
                print(f"Warning: join pipeline took longer than query {query}: {query_durations[query]} vs {polar_pp_durations[query]}")
                non_polar = query_durations[query] * 0.1
            if exhaustive[query] == 0:
                impacts.append(query_durations[query] / non_polar)
                continue

            reduction_factor = default[query] / exhaustive[query]
            reduced_duration = non_polar + polar_pp_durations[query] / reduction_factor

            impacts.append(query_durations[query] / reduced_duration)

        results[benchmark + "-" + optimizer_mode[:2]] = {"default": default, "optimal": exhaustive,
                                                         "best_in_class": best_in_class,
                                                         "worst_in_class": worst_in_class,
                                                         "impacts": impacts}

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