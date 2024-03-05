#!/usr/bin/env python3

import pandas as pd
import os
import glob

benchmarks = ["imdb", "ssb", "ssb-skew"]
routing_strategies = ["default_path", "alternate", "init_once", "opportunistic",
                      "adaptive_reinit", "dynamic", "backpressure"]

sweet_spots = {"adaptive_reinit": {"imdb": "0.01", "ssb": "0.01", "ssb-skew": "0.01"},
               "dynamic": {"imdb": "0.001", "ssb": "0.001", "ssb-skew": "0.001"}}

results = {}

for benchmark in benchmarks:
    num_files = -1
    alternate_files = []
    results[benchmark] = {}
    for strategy in routing_strategies:
        path = f"{os.getcwd()}/experiment-results/2_3_routing/{benchmark}/{strategy}"
        if strategy == "adaptive_reinit" or strategy == "dynamic":
            path += f"/{sweet_spots[strategy][benchmark]}"

        intms = []
        if strategy == "alternate":
            alternate_files = glob.glob(os.path.join(path, "*.csv"))
            alternate_files.sort()

            if num_files == -1:
                num_files = len(alternate_files)
            elif num_files != len(alternate_files):
                print("Warning: " + strategy + " has " + str(len(alternate_files)) + " instead of "
                      + str(num_files))

            for csv_file in alternate_files:
                df = pd.read_csv(csv_file)
                df.pop(df.columns[-1])
                if "path_0" not in df.columns:
                    print("Warning: " + csv_file)
                    txt_path = csv_file.split(".")[-2] + "-intms.txt"
                    print(f"  -> {txt_path}")
                    with open(txt_path) as f:
                        line = f.readline()
                        intms.append(int(line))
                    continue
                else:
                    intms.append(df.min(axis=1).sum())
        else:
            txt_files = glob.glob(os.path.join(path, "*.txt"))
            txt_files.sort()

            csv_files = glob.glob(os.path.join(path, "*.csv"))
            csv_files.sort()

            if len(txt_files) != len(csv_files):
                print("Warning: " + strategy + " has " + str(len(txt_files)) + " txts and " + str(len(csv_files))
                      + " csvs")

            if num_files == -1:
                num_files = len(txt_files)
            elif num_files != len(txt_files):
                print("Warning: " + strategy + " has " + str(len(txt_files)) + " instead of " + str(num_files))

            for i in range(len(csv_files)):
                csv_file = csv_files[i]
                txt_file = txt_files[i]

                if txt_file.split("/")[-1].split("-")[0] != csv_file.split("/")[-1].split(".")[0]:
                    print("Warning: " + txt_file.split("/")[-1] + " != " + csv_file.split("/")[-1])

                intermediates = 0
                with open(txt_file) as f:
                    line = f.readline()
                    if line == "":
                        print("Warning: " + txt_file)
                        continue
                    intermediates = int(line)

                df = pd.read_csv(csv_file)
                intermediates_2 = df["intermediates"].sum()

                if intermediates != intermediates_2:
                    print("### Warning ###")
                    print(txt_file + ": " + str(intermediates))
                    print(csv_file + ": " + str(intermediates_2))

                intms.append(int(intermediates))
        results[benchmark][strategy] = intms
        if strategy == "adaptive_reinit" or strategy == "dynamic":
            print(
                f"{benchmark} | {strategy}({sweet_spots[strategy][benchmark]}): {sum(intms) / 1000000}M intermediates")

formatted_results = {}
for benchmark in benchmarks:
    formatted_results[benchmark] = {}
    for strategy in routing_strategies:
        formatted_results[benchmark][strategy] = "{:10.2f}".format(sum(results[benchmark][strategy]) / 1000000) + "\\,M"

latex_table = f"""\\begin{{table}}[!t]
  \\centering
  \\caption{{Intermediate Results -- Number of Intermediates of Different Routing Strategies (Tuned Exploration Budgets).}}
  \\vspace{{-0.3cm}} \\setlength\\tabcolsep{{7.5pt}}
  \\begin{{tabular}}{{lrrr}}
    \\toprule
    \\textbf{{Routing Strategy}} & \\textbf{{JOB}} & \\textbf{{SSB}} & \\textbf{{SSB-skew}}\\\\
    \\midrule
    DuckDB & {formatted_results["imdb"]["default_path"]} & {formatted_results["ssb"]["default_path"]} & {formatted_results["ssb-skew"]["default_path"]}\\\\
    Optimal & {formatted_results["imdb"]["alternate"]} & {formatted_results["ssb"]["alternate"]} & {formatted_results["ssb-skew"]["alternate"]}\\\\
    \\midrule
    \\textsc{{InitOnce}} & {formatted_results["imdb"]["init_once"]} & {formatted_results["ssb"]["init_once"]} & {formatted_results["ssb-skew"]["init_once"]}\\\\
    \\textsc{{Opportunistic}} & {formatted_results["imdb"]["opportunistic"]} & \\textbf{{{formatted_results["ssb"]["opportunistic"]}}} & {formatted_results["ssb-skew"]["opportunistic"]}\\\\
    \\textsc{{AdaptTupleCount}} & \\textbf{{{formatted_results["imdb"]["dynamic"]}}} & {formatted_results["ssb"]["dynamic"]} & {formatted_results["ssb-skew"]["dynamic"]}\\\\
    \\textsc{{AdaptWindowSize}} & {formatted_results["imdb"]["adaptive_reinit"]} & {formatted_results["ssb"]["adaptive_reinit"]} & \\textbf{{{formatted_results["ssb-skew"]["adaptive_reinit"]}}}\\\\
    \\textsc{{Backpressure}} & {formatted_results["imdb"]["backpressure"]} & {formatted_results["ssb"]["backpressure"]} & {formatted_results["ssb-skew"]["backpressure"]}\\\\
    \\bottomrule
    \\end{{tabular}}
  \\label{{tab:2_4_routing_all}}
  \\vspace{{-0.2cm}}
\\end{{table}}
"""

with open("paper/tables/2_4_routing_all.tex", "w") as file:
    file.write(latex_table)
