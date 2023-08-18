#!/usr/bin/env python3

import pandas as pd
import os
import glob

optimizer_modes = ["dphyp-equisets", "greedy-equisets-ldt", "nostats"]
benchmarks = ["imdb", "ssb", "ssb-skew"]
enumerators = ["each_last_once", "each_first_once", "bfs_random-4", "bfs_min_card-4", "bfs_uncertain-8",
               "bfs_random-16", "bfs_min_card-16", "bfs_uncertain-16", "bfs_random-4", "bfs_min_card-4",
               "bfs_uncertain-4"]

results = {}

for benchmark in benchmarks:
    for optimizer_mode in optimizer_modes:
        # Calculate baselines from exhaustive
        path = f"{os.getcwd()}/experiment-results/2_1_enumeration_intms/{optimizer_mode}/{benchmark}/bfs_min_card-24"
        csv_files = glob.glob(os.path.join(path, "*.csv"))
        csv_files.sort()

        exhaustive = []
        default = []

        for csv_file in csv_files:
            df = pd.read_csv(csv_file)
            df.pop(df.columns[-1])

            exhaustive.append(df.min(axis=1).sum())
            default.append(df["path_0"].sum())

        results[benchmark + "-" + optimizer_mode[:2]] = {"default": default, "optimal": exhaustive}

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

print("each_last_once | exhaustive")
for i in range(len(results["imdb-dp"]["bfs_min_card-4"])):
    print(f"P{i+1}: {results['imdb-dp']['each_first_once'][i]}\t{results['imdb-dp']['bfs_min_card-4'][i]}")

result_keys = ["imdb-dp", "ssb-dp", "ssb-skew-dp", "imdb-gr"]

result_str = "\\begin{table}\n\t\\centering\n\t\\begin{tabular}{l"

for i in range(len(results)):
    result_str += "r"

result_str += "}\n\t\t"
result_str += "\\textbf{Join order selection}"

for result_key in result_keys:
    result_str += " & " + result_key

result_str += "\\\\\n\t\t"
result_str += "\\hline\n\t\t"

enumerators = list(results[list(results.keys())[0]].keys())
print(enumerators)

for enumerator in enumerators:
    result_str += enumerator.replace("_", " ")
    for result_key in result_keys:
        sum_intermediates = sum(results[result_key][enumerator])
        if enumerator == "optimal" and result_key == "imdb-gr":
            result_str += " & ---"  # No exhaustive enumeration in that config -> no optimum retrievable
        else:
            result_str += " & " + "{:10.2f}".format(sum_intermediates / 1000000) + " M"

    result_str += "\\\\\n\t\t"
    if enumerator == "optimal":
        result_str += "\\hline\n\t\t"

result_str += "\\hline\n\t\\end{tabular}\n\t\\caption{"
result_str += "Total number of intermediates for POLAR pipelines with optimal routing strategies"
result_str += "}\n\t\\label{"
result_str += "tab:1_1_sel_intms"
result_str += "}\n\\end{table}\n"

with open("experiment-results/2_1_enumeration_intms.txt", "w") as file:
    file.write(result_str)
