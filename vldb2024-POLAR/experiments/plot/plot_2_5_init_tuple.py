#!/usr/bin/env python3

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt

benchmarks = ["imdb", "ssb"]
init_counts = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

results = {}
baselines = {}
for benchmark in benchmarks:
    results[benchmark] = []
    path = f"{os.getcwd()}/experiment-results/2_3_routing/{benchmark}/default_path"
    txt_files = glob.glob(os.path.join(path, "*.txt"))
    txt_files.sort()

    intms = []
    for txt_file in txt_files:
        with open(txt_file) as f:
            line = f.readline()
            if line == "":
                print("Warning: " + txt_file + " empty.")
                continue
            intms.append(int(line))
    baselines[benchmark] = sum(intms)

    for init_count in init_counts:
        path = f"{os.getcwd()}/experiment-results/2_5_init_tuple/{benchmark}/{init_count}"
        txt_files = glob.glob(os.path.join(path, "*.txt"))
        txt_files.sort()

        intms = []
        for txt_file in txt_files:
            with open(txt_file) as f:
                line = f.readline()
                if line == "":
                    print("Warning: " + txt_file + " empty.")
                    continue
                intms.append(int(line))
        results[benchmark].append(sum(intms))

print(results)

normalized_results = {}
for benchmark in benchmarks:
    normalized_results[benchmark] = []
    for result in results[benchmark]:
        normalized_results[benchmark].append(result / baselines[benchmark])

line_colors = {
    "imdb": "#00cd6c",
    "ssb": "#009ade"
}

labels = {
    "imdb": "JOB",
    "ssb": "SSB"
}

plt.figure(figsize=(4.4, 2.25))
for benchmark in benchmarks:
    plt.plot(init_counts, normalized_results[benchmark], label=labels[benchmark], color=line_colors[benchmark])
plt.plot(init_counts, [1] * len(init_counts), label="DuckDB", color="black", linestyle="dotted")

plt.xlabel("Init Tuple Count")
plt.ylabel("Rel. Intermediate Count")
plt.ylim(bottom=0)
plt.xscale("log", base=2)
plt.legend(frameon=False)
plt.xticks(ticks=init_counts, labels=init_counts)
plt.tight_layout()
plt.savefig("paper/figures/2_5_init_tuple.pdf")
