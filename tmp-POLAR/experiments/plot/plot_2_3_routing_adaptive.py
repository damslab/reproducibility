#!/usr/bin/env python3

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt

benchmarks = ["imdb", "ssb", "ssb-skew"]
adaptive_routing_strategies = ["adaptive_reinit", "dynamic"]
exploration_budgets = ["0.00001", "0.0001", "0.001", "0.01", "0.1", "0.2", "0.4", "0.8", "1.6", "2.4", "3.2"]

results = {}

for benchmark in benchmarks:
    results[benchmark] = {}
    for strategy in adaptive_routing_strategies:
        results[benchmark][strategy] = []
        for budget in exploration_budgets:
            path = f"{os.getcwd()}/experiment-results/2_3_routing/{benchmark}/{strategy}/{budget}"

            intms = []
            txt_files = glob.glob(os.path.join(path, "*.txt"))
            if len(txt_files) == 0:
                print("Warning: " + benchmark + "/" + strategy + "/" + budget + " missing.")
                results[benchmark][strategy].append(0)
                continue
            txt_files.sort()

            for txt_file in txt_files:
                with open(txt_file) as f:
                    line = f.readline()
                    if line == "":
                        print("Warning: " + txt_file + " empty.")
                        continue
                    intms.append(int(line))

            if len(intms) == 0:
                print("Warning: " + benchmark + "/" + strategy + "/" + budget + " has no results.")
                results[benchmark][strategy].append(0)
                continue

            results[benchmark][strategy].append(sum(intms))

    strategy = "alternate"
    path = os.getcwd() + "/experiment-results/2_3_routing/" + benchmark + "/" + strategy
    intms_opt = []
    intms_default = []
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    if len(csv_files) == 0:
        print("Warning: " + benchmark + "/" + strategy + "/" + " missing.")
        results[benchmark]["optimal"] = [0] * len(exploration_budgets)
        results[benchmark]["default"] = [0] * len(exploration_budgets)
        continue
    csv_files.sort()

    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        df.pop(df.columns[-1])
        if "path_0" not in df.columns:
            print("Warning: " + csv_file + " corrupted.")
            continue
        intms_opt.append(df.min(axis=1).sum())
        intms_default.append(df["path_0"].sum())

    if len(intms_opt) == 0 or len(intms_default) == 0:
        print("Warning: " + benchmark + "/" + strategy + "/" + " has no results.")
        results[benchmark]["optimal"] = [0] * len(exploration_budgets)
        results[benchmark]["default"] = [0] * len(exploration_budgets)
        continue

    results[benchmark]["optimal"] = [sum(intms_opt)] * len(exploration_budgets)
    results[benchmark]["default"] = [sum(intms_default)] * len(exploration_budgets)
print(results)

line_colors = {
    "adaptive_reinit": "#00cd6c",
    "dynamic": "#009ade",
    "optimal": "#af58ba",
    "default": "#ffc61e"
}

labels = {"adaptive_reinit": "AdaptWindowSize",
          "dynamic": "AdaptTupleCount",
          "optimal": "Optimal",
          "default": "DuckDB"}

titles = {"imdb": "JOB", "ssb": "SSB", "ssb-skew": "SSB-skew"}

x_values = [float(i) for i in exploration_budgets]

fig, ax = plt.subplots(1, len(benchmarks), figsize=(10, 2), constrained_layout=True, sharex=True)
for i in range(len(benchmarks)):
    benchmark = benchmarks[i]
    for strategy in results[benchmark]:
        ax[i].plot(x_values, results[benchmark][strategy], label=labels[strategy],
                   color=line_colors[strategy], linewidth=1.5)
    ax[i].set_title(titles[benchmark])
    ax[i].set_xscale("log")
    ax[i].set_ylim(bottom=0)

    adre_sweet_spot_idx = 0
    adre_min_intms = results[benchmark]["adaptive_reinit"][0]
    dyn_sweet_spot_idx = 0
    dyn_min_intms = results[benchmark]["dynamic"][0]

    for j in range(len(results[benchmark]["adaptive_reinit"])):
        if results[benchmark]["adaptive_reinit"][j] < adre_min_intms:
            adre_min_intms = results[benchmark]["adaptive_reinit"][j]
            adre_sweet_spot_idx = j
        if results[benchmark]["dynamic"][j] < dyn_min_intms:
            dyn_min_intms = results[benchmark]["dynamic"][j]
            dyn_sweet_spot_idx = j

    ax[i].axvline(x=x_values[adre_sweet_spot_idx], color=line_colors["adaptive_reinit"], linestyle='dotted')
    ax[i].axvline(x=x_values[dyn_sweet_spot_idx], color=line_colors["dynamic"], linestyle='dotted')
    if i == 2:
        handles, labels = ax[i].get_legend_handles_labels()
        fig.legend(handles, labels, loc='outside right center', frameon=False)

fig.supxlabel('Exploration budget')
fig.supylabel('Intermediates')
plt.savefig("paper/figures/2_3_routing_adaptive.pdf")
