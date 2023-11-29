#!/usr/bin/env python3

import pandas as pd
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

benchmarks = ["ssb"]
enumerators = ["sample", "each_last_once", "each_first_once"]
sample_sizes = list(range(2, 33, 2))

results = {}

for benchmark in benchmarks:
    results[benchmark] = {}
    for enumerator in enumerators:
        compile_times = []
        path = ""
        if enumerator == "sample":
            for sample_size in sample_sizes:
                path = f"{os.getcwd()}/experiment-results/2_0_sample_size/{benchmark}/{sample_size}/timings"
                csv_files = glob.glob(os.path.join(path, "*.csv"))
                csv_files.sort()

                total_compile_time = 0
                for csv_file in csv_files:
                    df = pd.read_csv(csv_file)
                    total_compile_time += df["enumeration_time_ms"].min()
                compile_times.append(total_compile_time / len(csv_files))
        else:
            path = f"{os.getcwd()}/experiment-results/2_2_enumeration_timings/dphyp-equisets/{benchmark}/{enumerator}"
            csv_files = glob.glob(os.path.join(path, "*.csv"))
            csv_files.sort()

            total_compile_time = 0
            for csv_file in csv_files:
                df = pd.read_csv(csv_file)
                total_compile_time += df["enumeration_time_ms"].min()
            compile_times = [total_compile_time / len(csv_files)] * len(sample_sizes)
        results[benchmark][enumerator] = compile_times

print(results)

line_colors = {
    "sample": "#00cd6c",
    "each_first_once": "#009ade",
    "each_last_once": "#af58ba"
}

labels = {
    "sample": "SelSampling",
    "each_first_once": "PushDown",
    "each_last_once": "PullUp"
}

linestyles = {
    "sample": "-",
    "each_first_once": "--",
    "each_last_once": "-."
}

plt.figure(figsize=(4.25, 2.5))
for enumerator in enumerators:
    plt.plot(sample_sizes, results["ssb"][enumerator], label=labels[enumerator], color=line_colors[enumerator], linestyle=linestyles[enumerator])

plt.xlabel("Sample Count")
plt.ylabel("Average compile time (ms)")
#plt.ylim(bottom=0)
#plt.yscale("log")
plt.legend(frameon=False)
#plt.xticks(ticks=x_values, labels=x_values)
plt.tight_layout()
plt.savefig("paper/figures/2_2_enumeration_timings.pdf")
