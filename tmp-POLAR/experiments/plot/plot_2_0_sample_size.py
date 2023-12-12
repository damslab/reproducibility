import pandas as pd
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

benchmarks = ["imdb", "ssb", "ssb-skew"]
sample_sizes = [1] + list(range(2, 17, 2))

results = {}
for benchmark in benchmarks:
    # Calculate baselines from exhaustive
    path = f"{os.getcwd()}/experiment-results/2_1_enumeration_intms/dphyp-equisets/{benchmark}/optimal"
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

    results[benchmark] = {"default": default, "optimal": exhaustive, "static": static, "sample": {}}

    for sample_size in sample_sizes:
        path = f"{os.getcwd()}/experiment-results/2_0_sample_size/{benchmark}/{sample_size}"
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

        results[benchmark]["sample"][sample_size] = intermediates

    print("### " + benchmark + " ###")
    for mode in results[benchmark]:
        if mode == "sample":
            for sample_size in sample_sizes:
                print(f"SAMPLE({sample_size}): {sum(results[benchmark][mode][sample_size]) / 1000000} M")
        else:
            sum_intermediates = sum(results[benchmark][mode])
            print(str(mode) + ": " + str(sum_intermediates / 1000000) + " M")

formatted_results = {"x_values": [0] + sample_sizes, "optimal": [1] * (len(sample_sizes) + 1)}

for benchmark in benchmarks:
    formatted_results[benchmark] = []
    formatted_results[benchmark].append(sum(results[benchmark]["default"]) / sum(results[benchmark]["optimal"]))
    for sample_size in sample_sizes:
        formatted_results[benchmark].append(sum(results[benchmark]["sample"][sample_size]) / sum(results[benchmark]["optimal"]))

print(formatted_results)

line_colors = {
    "imdb": "#00cd6c",
    "ssb": "#009ade",
    "ssb-skew": "#af58ba"
}

labels = {
    "imdb": "JOB",
    "ssb": "SSB",
    "ssb-skew": "SSB-skew"
}

plt.figure(figsize=(3.1, 2.8))
for benchmark in benchmarks:
    plt.plot(formatted_results["x_values"], formatted_results[benchmark], label=labels[benchmark], color=line_colors[benchmark], marker="x")
plt.plot(formatted_results["x_values"], formatted_results["optimal"], label="Exhaustive", color="black", linestyle='dotted')

plt.xlabel("Selectivity space samples")
plt.ylabel("Min. intermediates")
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
plt.yscale("log", base=2)
#plt.ylim(bottom=0)
plt.legend(frameon=False)
plt.xticks(ticks=formatted_results["x_values"], labels=formatted_results["x_values"])
plt.tight_layout()
plt.savefig("paper/figures/2_0_sample_size.pdf")
