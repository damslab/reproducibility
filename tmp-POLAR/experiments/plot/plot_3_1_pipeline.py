#!/usr/bin/env python3
import pandas
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

routing_strategies = ["default", "init_once", "opportunistic", "adaptive_reinit", "dynamic", "backpressure"]
benchmarks = ["imdb", "ssb", "ssb-skew"]
exploration_budgets = ["0.00001", "0.0001", "0.001", "0.01", "0.1", "0.2", "0.4", "0.8", "1.6", "2.4", "3.2"]
sweet_spots = {"adaptive_reinit": {}, "dynamic": {}}
results = {}

for benchmark in benchmarks:
    results[benchmark] = {}
    for strategy in routing_strategies:
        path = f"{os.getcwd()}/experiment-results/3_1_pipeline/{benchmark}/{strategy}"

        if strategy == "adaptive_reinit" or strategy == "dynamic":
            print(benchmark)
            results[benchmark][strategy] = {}
            min_timing_s = 10000000
            budget_sweet_spot = ""

            for budget in exploration_budgets:
                path = f"{os.getcwd()}/experiment-results/3_1_pipeline/{benchmark}/{strategy}/{budget}"

                csv_files = glob.glob(os.path.join(path, "*.csv"))
                csv_files.sort()
                if len(csv_files) == 0:
                    print(f"Warning: no results for {path}")
                    continue

                timings = []
                for csv_file in csv_files:
                    df = pd.read_csv(csv_file, names=["timing"])
                    avg_timing = float(df["timing"].median())
                    timings.append(avg_timing)

                results[benchmark][strategy][budget] = timings
                timing_sum_s = sum(timings) / 1000
                print(f"{strategy}({budget}): {timing_sum_s} s")
                if timing_sum_s < min_timing_s:
                    min_timing_s = timing_sum_s
                    budget_sweet_spot = budget
            sweet_spots[strategy][benchmark] = budget_sweet_spot
        else:
            csv_files = glob.glob(os.path.join(path, "*.csv"))
            csv_files.sort()
            if len(csv_files) == 0:
                print(f"Warning: no results for {path}")
                continue

            timings = []
            for csv_file in csv_files:
                df = pd.read_csv(csv_file, names=["timing"])
                avg_timing = float(df["timing"].median())
                timings.append(avg_timing)

            results[benchmark][strategy] = timings

print(sweet_spots)

for key in results:
    df = pandas.DataFrame()
    for strategy in results[key]:
        df[strategy] = results[key][strategy]

    for strategy in results[key]:
        df[f"{strategy}-rel"] = 1 + ((df["default"] - df[strategy]) / df[strategy])
    df.to_csv(f"experiment-results/3_1_pipeline_{key}.csv", sep="\t")

    print(key)
    print(df[df["adaptive_reinit-rel"] < 1].sort_values(by=["default"]))

result_str = "\\begin{table}\n\t\\centering\n\t\\begin{tabular}{l"

for i in range(len(results)):
    result_str += "r"

result_str += "}\n\t\t"
result_str += "\\textbf{Routing strategy}"

for result_key in results:
    if "default" in results[result_key]:
        result_str += " & " + result_key

result_str += "\\\\\n\t\t"
result_str += "\\hline\n\t\t"

for routing_strategy in routing_strategies:
    result_str += routing_strategy.replace("_", " ")

    if routing_strategy == "adaptive_reinit" or routing_strategy == "dynamic":
        for result_key in results:
            if "default" in results[result_key] and len(results[result_key]["default"]) > 0:
                total_pipeline_duration = sum(results[result_key][routing_strategy][sweet_spots[routing_strategy][result_key]])
                result_str += " & " + "{:10.2f}".format(total_pipeline_duration / 1000) + " s"
        result_str += "\\\\\n\t\t"
    else:
        for result_key in results:
            if "default" in results[result_key] and len(results[result_key]["default"]) > 0:
                total_pipeline_duration = sum(results[result_key][routing_strategy])
                result_str += " & " + "{:10.2f}".format(total_pipeline_duration / 1000) + " s"
        result_str += "\\\\\n\t\t"

result_str += "\\hline\n\t\\end{tabular}\n\t\\caption{"
result_str += "Total duration for POLAR-applicable pipelines"
result_str += "}\n\t\\label{"
result_str += "tab:3_1_pipeline"
result_str += "}\n\\end{table}\n"

with open("experiment-results/3_1_pipeline.txt", "w") as file:
    file.write(result_str)

#for result_key in results:
#    fig = plt.figure()
#    ax = fig.add_axes([0, 0, 1, 1])
#    i = 0
#    for strategy in results[result_key]:
#        X = np.arange(len(results[result_key][strategy]))
#        ax.bar(X + i, results[result_key][strategy], width=0.18)
#        i = i + 0.18
#    fig.legend(routing_strategies)
#    plt.savefig(f"experiment-results/3_1_pipeline_per_query_{result_key}.pdf")
#    plt.clf()

