#!/usr/bin/env python3
import pandas
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

routing_strategies = ["default", "init_once", "opportunistic", "adaptive_reinit", "dynamic", "backpressure"]
benchmarks = ["imdb", "ssb", "ssb-skew"]
exploration_budgets = ["0.01"]
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

formatted_results = {}
for benchmark in benchmarks:
    formatted_results[benchmark] = {}
    for strategy in routing_strategies:
        if strategy == "adaptive_reinit" or strategy == "dynamic":
            formatted_results[benchmark][strategy] = "{:10.2f}".format(
                sum(results[benchmark][strategy][sweet_spots[strategy][benchmark]]) / 1000)
        else:
            formatted_results[benchmark][strategy] = "{:10.2f}".format(sum(results[benchmark][strategy]) / 1000)

latex_table = f"""
\\begin{{table}}[!t]
  \\centering
  \\caption{{Execution Time -- Total pipeline execution time per routing strategy [seconds].}}
  \\vspace{{-0.3cm}}  \\setlength\\tabcolsep{{11.4pt}}
  \\begin{{tabular}}{{lrrr}}
    \\toprule
    \\textbf{{Routing strategy}} & \\textbf{{JOB}} & \\textbf{{SSB}} & \\textbf{{SSB-skew}}\\\\
    \\midrule
    DuckDB & {formatted_results["imdb"]["default"]} & {formatted_results["ssb"]["default"]} & {formatted_results["ssb-skew"]["default"]}\\\\
    \\midrule
    \\textsc{{InitOnce}} & {formatted_results["imdb"]["init_once"]} & {formatted_results["ssb"]["init_once"]} & {formatted_results["ssb-skew"]["init_once"]}\\\\
    \\textsc{{Opportunistic}} & {formatted_results["imdb"]["opportunistic"]} & {formatted_results["ssb"]["opportunistic"]} & {formatted_results["ssb-skew"]["opportunistic"]}\\\\
    \\textsc{{AdaptTupleCount}} & {formatted_results["imdb"]["dynamic"]} & {formatted_results["ssb"]["dynamic"]} & {formatted_results["ssb-skew"]["dynamic"]}\\\\
    \\textsc{{AdaptWindowSize}} & {formatted_results["imdb"]["adaptive_reinit"]} & {formatted_results["ssb"]["adaptive_reinit"]} & {formatted_results["ssb-skew"]["adaptive_reinit"]}\\\\
    \\textsc{{Backpressure}} & {formatted_results["imdb"]["backpressure"]} & {formatted_results["ssb"]["backpressure"]} & {formatted_results["ssb-skew"]["backpressure"]}\\\\
    \\bottomrule
  \\end{{tabular}}
  \\label{{tab:3_1_pipeline}}
\\end{{table}}
"""

with open("paper/tables/3_1_pipeline.tex", "w") as file:
    file.write(latex_table)

formatted_results_untuned = {}
for benchmark in benchmarks:
    formatted_results_untuned[benchmark] = {}
    formatted_results_untuned[benchmark]["dynamic"] = "{:10.2f}".format(sum(results[benchmark]["dynamic"]["0.001"]) / 1000)
    formatted_results_untuned[benchmark]["adaptive_reinit"] = "{:10.2f}".format(sum(results[benchmark]["adaptive_reinit"]["0.01"]) / 1000)

latex_table = f"""\\begin{{table}}[!t]
  \\centering
  \\caption{{Parameter Robustness -- Total pipeline execution time with generic vs. tuned exploration budgets [seconds].}}
  \\vspace{{-0.3cm}}  \\setlength\\tabcolsep{{8.7pt}}
  \\begin{{tabular}}{{lrrr}}
    \\toprule
    \\textbf{{Routing strategy}} & \\textbf{{JOB}} & \\textbf{{SSB}} & \\textbf{{SSB-skew}}\\\\
    \\midrule
    DuckDB & {formatted_results["imdb"]["default"]} & {formatted_results["ssb"]["default"]} & {formatted_results["ssb-skew"]["default"]}\\\\
    \\midrule
    \\textsc{{AdaptTupleCount}} (0.1\\,\\%) & {formatted_results_untuned["imdb"]["dynamic"]} & {formatted_results_untuned["ssb"]["dynamic"]} & {formatted_results_untuned["ssb-skew"]["dynamic"]}\\\\
    \\textsc{{AdaptTupleCount}}-tuned & {formatted_results["imdb"]["dynamic"]} & {formatted_results["ssb"]["dynamic"]} & {formatted_results["ssb-skew"]["dynamic"]}\\\\
    \\midrule
    \\textsc{{AdaptWindowSize}} (1\\,\\%) & {formatted_results_untuned["imdb"]["adaptive_reinit"]} & {formatted_results_untuned["ssb"]["adaptive_reinit"]} & {formatted_results_untuned["ssb-skew"]["adaptive_reinit"]}\\\\
    \\textsc{{AdaptWindowSize}}-tuned & {formatted_results["imdb"]["adaptive_reinit"]} & {formatted_results["ssb"]["adaptive_reinit"]} & {formatted_results["ssb-skew"]["adaptive_reinit"]}\\\\
    \\bottomrule
  \\end{{tabular}}
\\label{{tab:3_3_parameter}}
\\end{{table}}
"""

with open("paper/tables/3_3_parameter.tex", "w") as file:
    file.write(latex_table)
