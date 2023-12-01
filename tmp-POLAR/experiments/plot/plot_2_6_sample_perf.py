#!/usr/bin/env python3
import pandas
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

routing_strategies = ["adaptive_reinit", "dynamic", "adaptive_reinit-exhaustive", "dynamic-exhaustive"]
benchmarks = ["ssb-skew"]
exploration_budgets = ["0.001", "0.01", "0.1"]
results = {}

for benchmark in benchmarks:
    results[benchmark] = {}
    for strategy in routing_strategies:
        path = f"{os.getcwd()}/experiment-results/3_1_pipeline/{benchmark}/{strategy}"
        results[benchmark][strategy] = []

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

            results[benchmark][strategy].append(sum(timings) / 1000)

print(results)

normalized_results = {}
for routing_strategy in ["adaptive_reinit", "dynamic"]:
    normalized_results[routing_strategy] = []
    for i in range(len(results["ssb-skew"][routing_strategy])):
        normalized_results[routing_strategy].append(((results["ssb-skew"][f"{routing_strategy}-exhaustive"][i] / results["ssb-skew"][routing_strategy][i]) - 1) * 100)

line_colors = {
    "adaptive_reinit": "#00cd6c",
    "dynamic": "#009ade",
    "adaptive_reinit-exhaustive": "#009ade",
    "dynamic-exhaustive": "#009ade"
}

linestyles = {
    "adaptive_reinit": "-",
    "dynamic": "--",
    "adaptive_reinit-exhaustive": "-",
    "dynamic-exhaustive": "--"
}

labels = {
    "adaptive_reinit": "AdaptWindowSize",
    "dynamic": "AdaptTupleCount",
    "adaptive_reinit-exhaustive": "AWS-exhaustive",
    "dynamic-exhaustive": "ATC-exhaustive"
}
plt.figure(figsize=(4.25, 2.5))
for benchmark in benchmarks:
    for routing_strategy in ["adaptive_reinit", "dynamic"]:
        plt.plot(exploration_budgets, normalized_results[routing_strategy], color=line_colors[routing_strategy], label=labels[routing_strategy])

plt.xlabel("Regret budget")
plt.ylabel("Exec. Time Overhead (%)")
#plt.ylim(bottom=0)
#plt.xscale("log", base=2)
plt.legend(frameon=False)
#plt.xticks(ticks=init_counts, labels=init_counts)
plt.tight_layout()
plt.savefig("paper/figures/2_6_sample_perf.pdf")
