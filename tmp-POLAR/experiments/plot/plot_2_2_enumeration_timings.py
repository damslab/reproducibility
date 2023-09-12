#!/usr/bin/env python3

import pandas as pd
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

enumerators = ["bfs_random", "bfs_min_card", "bfs_uncertain", "each_last_once", "each_first_once"]

results = {}

for enumerator in enumerators:
    path = f"{os.getcwd()}/experiment-results/2_2_enumeration_timings/greedy-equisets-ldt/imdb/{enumerator}"
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    csv_files.sort()

    enumeration_times = {}
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        num_joins = df["num_joins"].min()
        duration = df["enumeration_time_ms"].min()

        if num_joins not in enumeration_times:
            enumeration_times[num_joins] = []

        enumeration_times[num_joins].append(duration)

    results[enumerator] = {}
    for num_joins in enumeration_times:
        results[enumerator][num_joins] = np.mean(enumeration_times[num_joins])

print(results)

line_colors = {
    "each_last_once": "#00cd6c",
    "each_first_once": "#009ade",
    "bfs_random": "#af58ba",
    "bfs_min_card": "#ffc61e",
    "bfs_uncertain": "#f28522"
}

labels = {
    "each_last_once": "PullUp",
    "each_first_once": "PushDown",
    "bfs_random": "GetRandom",
    "bfs_min_card": "GetMinCard",
    "bfs_uncertain": "GetMinCardUc"
}

x_values = []
for enumerator in enumerators:
    if len(results[enumerator]) > 0:
        x_values = sorted(list(results[enumerator].keys()))
        break

plt.figure(figsize=(4.25, 2.5))
for enumerator in enumerators:
    if len(results[enumerator]) == 0:
        continue

    y_values = []
    for num_joins in sorted(results[enumerator].keys()):
        y_values.append(results[enumerator][num_joins])

    plt.plot(x_values, y_values, label=labels[enumerator], color=line_colors[enumerator], marker="^")

plt.xlabel("Number of joins in pipeline")
plt.ylabel("Compilation time (ms)")
#plt.ylim(bottom=0)
plt.yscale("log")
plt.legend(frameon=False)
plt.xticks(ticks=x_values, labels=x_values)
plt.tight_layout()
plt.savefig("paper/figures/2_2_enumeration_timings.pdf")
