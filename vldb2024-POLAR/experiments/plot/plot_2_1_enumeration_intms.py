#!/usr/bin/env python3

import pandas as pd
import os
import glob

optimizer_modes = ["dphyp-equisets", "greedy-equisets-ldt"]
benchmarks = ["imdb", "ssb", "ssb-skew"]
enumerators = ["each_last_once", "each_first_once", "bfs_min_card", "bfs_random", "sample"]

results = {}
for benchmark in benchmarks:
    for optimizer_mode in optimizer_modes:
        # Calculate baselines from exhaustive
        path = ""
        if optimizer_mode == "dphyp-equisets":
            path = f"{os.getcwd()}/experiment-results/2_1_enumeration_intms/{optimizer_mode}/{benchmark}/optimal"
        elif benchmark == "imdb":
            path = f"{os.getcwd()}/experiment-results/2_1_enumeration_intms/{optimizer_mode}/{benchmark}/bfs_min_card"
        else:
            continue

        csv_files = glob.glob(os.path.join(path, "*.csv"))
        csv_files.sort()

        exhaustive = []
        default = []
        static = []

        for csv_file in csv_files:
            df = pd.read_csv(csv_file)
            df.pop(df.columns[-1])
            exhaustive.append(df.min(axis=1).sum())
            default.append(df["path_0"].sum())
            static.append(df.sum().min())

        results[benchmark + "-" + optimizer_mode[:2]] = {"default": default, "optimal": exhaustive, "static": static}

        for enumerator in enumerators:
            path = f"{os.getcwd()}/experiment-results/2_1_enumeration_intms/{optimizer_mode}/{benchmark}/{enumerator}"
            csv_files = glob.glob(os.path.join(path, "*.csv"))
            csv_files.sort()

            intermediates = []

            for csv_file in csv_files:
                df = pd.read_csv(csv_file)
                if "path_0" in df:
                    df.pop(df.columns[-1])
                    intermediates.append(df.min(axis=1).sum())
                else:
                    if "intermediates" not in df:
                        print(f"Warning: {csv_file} ?")
                    intermediates.append(df["intermediates"].sum())

            results[benchmark + "-" + optimizer_mode[:2]][enumerator] = intermediates

        print("### " + benchmark + "-" + optimizer_mode + " ###")
        for mode in results[benchmark + "-" + optimizer_mode[:2]]:
            sum_intermediates = sum(results[benchmark + "-" + optimizer_mode[:2]][mode])
            print(mode + ": " + str(sum_intermediates / 1000000) + "M intermediates")

formatted_results = {}
for result_key in results:
    formatted_results[result_key] = {}
    for enumerator in results[result_key]:
        formatted_results[result_key][enumerator] = "{:10.2f}".format(sum(results[result_key][enumerator]) / 1000000) + "\\,M"

latex_table = f"""\\begin{{table}}[!t]
  \\centering
  \\caption{{Join Order Selection -- Total Number of Intermediates for POLAR Pipelines with Different Selection Strategies.}}
  \\vspace{{-0.3cm}}
  \\begin{{tabular}}{{lrrrr}}
    \\toprule
    \\textbf{{Enumeration}} & \\textbf{{JOB}} & \\textbf{{SSB}} & \\textbf{{SSB-skew}} & \\textbf{{JOB-ldt}}\\\\
    \\midrule
    DuckDB* & {formatted_results["imdb-dp"]["default"]} & {formatted_results["ssb-dp"]["default"]} & {formatted_results["ssb-skew-dp"]["default"]} & {formatted_results["imdb-gr"]["default"]} \\\\
    Optimal & {formatted_results["imdb-dp"]["optimal"]} & {formatted_results["ssb-dp"]["optimal"]} & {formatted_results["ssb-skew-dp"]["optimal"]} & ---\\\\
    \\midrule
    \\textsc{{SelSampling}} & {formatted_results["imdb-dp"]["sample"]} & {formatted_results["ssb-dp"]["sample"]} & {formatted_results["ssb-skew-dp"]["sample"]} & {formatted_results["imdb-gr"]["sample"]}\\\\
    \\textsc{{GetMinCard}} & {formatted_results["imdb-dp"]["bfs_min_card"]} & {formatted_results["ssb-dp"]["bfs_min_card"]} & {formatted_results["ssb-skew-dp"]["bfs_min_card"]} & {formatted_results["imdb-gr"]["bfs_min_card"]}\\\\
    \\textsc{{GetRandom}} & {formatted_results["imdb-dp"]["bfs_random"]} & {formatted_results["ssb-dp"]["bfs_random"]} & {formatted_results["ssb-skew-dp"]["bfs_random"]} & {formatted_results["imdb-gr"]["bfs_random"]}\\\\
    \\textsc{{PushDown}} & {formatted_results["imdb-dp"]["each_first_once"]} & {formatted_results["ssb-dp"]["each_first_once"]} & {formatted_results["ssb-skew-dp"]["each_first_once"]} & {formatted_results["imdb-gr"]["each_first_once"]}\\\\
    \\textsc{{PullUp}} & {formatted_results["imdb-dp"]["each_last_once"]} & {formatted_results["ssb-dp"]["each_last_once"]} & {formatted_results["ssb-skew-dp"]["each_last_once"]} & {formatted_results["imdb-gr"]["each_last_once"]}\\\\
    \\bottomrule
  \\end{{tabular}}
  \\label{{tab:1_1_sel_intms}}
  \\vspace{{-0.4cm}}
\\end{{table}}
"""

with open("paper/tables/1_1_sel_intms.tex", "w") as file:
    file.write(latex_table)

results = {}
for benchmark in benchmarks:
    results[benchmark] = {}
    path = os.getcwd() + f"/experiment-results/3_1_pipeline/{benchmark}/default"
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    if len(csv_files) == 0:
        print(f"Warning: no results for {path}")

    timings = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, names=["timing"])
        median_timing = float(df["timing"].median())
        timings.append(median_timing / 1000)

    if len(timings) == 0:
        timings.append(0)

    results[benchmark]["pipelines"] = timings
    path = os.getcwd() + f"/experiment-results/3_2_query/{benchmark}/duckdb.csv"

    df = pd.read_csv(path, names=["name", "run", "timing"])
    total_time = float(df.groupby("name").median()["timing"].sum())
    results[benchmark]["queries"] = total_time

formatted_coverage = {}
for benchmark in benchmarks:
    formatted_coverage[benchmark] = "{:10.0f}".format(min(1, sum(results[benchmark]["pipelines"]) / results[benchmark]["queries"]) * 100)

latex_table = f"""\\begin{{table}}[!t]
  \\centering 
  \\caption{{Total Number of Intermediates and Fraction of Total Execution Time Spent in Amenable Pipelines (Coverage).}}
  \\vspace{{-0.3cm}} \\setlength\\tabcolsep{{5.2pt}}
  \\begin{{tabular}}{{lrrrr}}
    \\toprule
    \\textbf{{Benchmark}} & \\textbf{{DuckDB}} & \\textbf{{Routing}} & \\textbf{{Static}} & \\textbf{{Coverage}}\\\\
    \\midrule
    JOB & {formatted_results["imdb-dp"]["default"]} & {formatted_results["imdb-dp"]["optimal"]} & {formatted_results["imdb-dp"]["static"]} & {formatted_coverage["imdb"]} \\%\\\\
    SSB & {formatted_results["ssb-dp"]["default"]} & {formatted_results["ssb-dp"]["optimal"]} & {formatted_results["ssb-dp"]["static"]} & {formatted_coverage["ssb"]} \\%\\\\
    SSB-skew & {formatted_results["ssb-skew-dp"]["default"]} & {formatted_results["ssb-skew-dp"]["optimal"]} & {formatted_results["ssb-skew-dp"]["static"]} & {formatted_coverage["ssb-skew"]} \\%\\\\
    \\bottomrule
  \\end{{tabular}}
\\label{{tab:1_2_potential_savings}}
\\vspace{{-0.2cm}}
\\end{{table}}
"""

with open("paper/tables/1_2_potential_savings.tex", "w") as file:
    file.write(latex_table)
