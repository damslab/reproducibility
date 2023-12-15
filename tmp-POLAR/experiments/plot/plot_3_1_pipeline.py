#!/usr/bin/env python3
import pandas
import pandas as pd
import os
import glob
import sys
import matplotlib.pyplot as plt
import numpy as np

routing_strategies = ["default", "init_once", "opportunistic", "adaptive_reinit", "dynamic", "backpressure"]
benchmarks = ["imdb", "ssb", "ssb-skew"]
exploration_budgets = ["0.001", "0.01"]
sweet_spots = {"adaptive_reinit": {}, "dynamic": {}}
results = {}

for benchmark in benchmarks:
    results[benchmark] = {}
    for strategy in routing_strategies:
        path = f"{os.getcwd()}/experiment-results/3_1_pipeline/{benchmark}/{strategy}"

        if strategy == "adaptive_reinit" or strategy == "dynamic":
            print(benchmark)
            results[benchmark][strategy] = {}
            min_timing_s = sys.maxsize
            budget_sweet_spot = ""

            for budget in exploration_budgets:
                path = f"{os.getcwd()}/experiment-results/3_1_pipeline/{benchmark}/{strategy}/{budget}"

                csv_files = glob.glob(os.path.join(path, "*.csv"))
                csv_files.sort()
                if len(csv_files) == 0:
                    print(f"Warning: no results for {path}")
                    continue

                timings = {}
                for csv_file in csv_files:
                    query_name = "-".join(csv_file.split("/")[-1].split("-")[0:-1])
                    df = pd.read_csv(csv_file, names=["timing"])
                    avg_timing = float(df["timing"].median())
                    if query_name in timings:
                        timings[query_name] += avg_timing
                    else:
                        timings[query_name] = avg_timing

                # For AdaptWindowSize, align with end-to-end benchmark
                if strategy == "adaptive_reinit":
                    path = os.getcwd() + f"/experiment-results/3_2_query/{benchmark}/0.01/polar.csv"
                    df = pd.read_csv(path, names=["name", "run", "timing"])
                    df = df.groupby("name", as_index=False).median()

                    for index, row in df.iterrows():
                        query_name = str(row["name"]).split("/")[-1].split(".")[0]
                        if query_name not in timings:
                            continue
                        query_duration_ms = float(row["timing"]) * 1000
                        if query_duration_ms < timings[query_name]:
                            print(f"Warning: join pipeline took longer than query {query_name}: {query_duration_ms} vs {timings[query_name]}")
                            timings[query_name] = query_duration_ms

                results[benchmark][strategy][budget] = timings.values()
                timing_sum_s = sum(timings.values()) / 1000
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

formatted_results = {}
for benchmark in benchmarks:
    formatted_results[benchmark] = {}
    for strategy in routing_strategies:
        if strategy == "adaptive_reinit" or strategy == "dynamic":
            formatted_results[benchmark][strategy] = "{:10.2f}".format(
                sum(results[benchmark][strategy][sweet_spots[strategy][benchmark]]) / 1000)
        else:
            formatted_results[benchmark][strategy] = "{:10.2f}".format(sum(results[benchmark][strategy]) / 1000)

latex_table = f"""\\begin{{table}}[!t]
  \\centering
  \\caption{{Execution Time -- Pipeline Execution Time of Different Routing Strategies [seconds].}}
  \\vspace{{-0.3cm}}  \\setlength\\tabcolsep{{10.6pt}}
  \\begin{{tabular}}{{lrrr}}
    \\toprule
    \\textbf{{Routing Strategy}} & \\textbf{{JOB}} & \\textbf{{SSB}} & \\textbf{{SSB-skew}}\\\\
    \\midrule
    DuckDB & {formatted_results["imdb"]["default"]} & {formatted_results["ssb"]["default"]} & {formatted_results["ssb-skew"]["default"]}\\\\
    \\midrule
    \\textsc{{InitOnce}} & {formatted_results["imdb"]["init_once"]} & {formatted_results["ssb"]["init_once"]} & {formatted_results["ssb-skew"]["init_once"]}\\\\
    \\textsc{{Opportunistic}} & {formatted_results["imdb"]["opportunistic"]} & {formatted_results["ssb"]["opportunistic"]} & {formatted_results["ssb-skew"]["opportunistic"]}\\\\
    \\textsc{{AdaptTupleCount}} & {formatted_results["imdb"]["dynamic"]} & {formatted_results["ssb"]["dynamic"]} & {formatted_results["ssb-skew"]["dynamic"]}\\\\
    \\textsc{{AdaptWindowSize}} & \\textbf{{{formatted_results["imdb"]["adaptive_reinit"]}}} & \\textbf{{{formatted_results["ssb"]["adaptive_reinit"]}}} & \\textbf{{{formatted_results["ssb-skew"]["adaptive_reinit"]}}}\\\\
    \\textsc{{Backpressure}} & {formatted_results["imdb"]["backpressure"]} & {formatted_results["ssb"]["backpressure"]} & {formatted_results["ssb-skew"]["backpressure"]}\\\\
    \\bottomrule
  \\end{{tabular}}
  \\label{{tab:3_1_pipeline}}
\\end{{table}}
"""

with open("paper/tables/3_1_pipeline.tex", "w") as file:
    file.write(latex_table)
