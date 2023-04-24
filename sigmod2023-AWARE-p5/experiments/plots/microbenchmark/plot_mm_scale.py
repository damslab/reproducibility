
import os
import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.transforms
import numpy as np

warnings.filterwarnings("ignore")


mpl.rcParams["font.family"] = "serif"
plt.close("all")


labelfontSize = 7.45


def parsMM(path):

    firstLine = True
    data = {}
    if os.path.isfile(path):
        with open(path) as f:
            for line in f:
                if firstLine:
                    firstLine = False
                    continue

                split = [x.strip() for x in line.split(",")]

                rowCols = split[1][6:].replace("+", "")
                idx = split[2].strip() + split[1][:-(len(rowCols))
                                                  ].replace(" ", "_")
                rowCols = int(rowCols)
                if idx not in data.keys():
                    data[idx] = []
                data[idx].append(
                    (rowCols, float(split[3]))
                )
    return data


def plotMM(data, outputFilePath, title, keys, yticks=[1, 10, 100, 1000], xlabel="# rows in left matrix", data2=None):
    fig, ax = plt.subplots(
        1,
        1,
        num=None,
        figsize=((42) / 6 * 1.0 / 2, 3 * 0.5),
        dpi=80,
        facecolor="w",
        edgecolor="k",
    )

    minV =10000000
    maxV = 0.0000001
    x = []
    labels = ["CLA", "ULA", "Mem", "AWARE"]
    for n in range(len(keys)):

        x = [v[0] for v in data[keys[n]]]
        y = [v[1] for v in data[keys[n]]]
        if min(y) < minV and min(y) > 0.000001:
            minV = min(y)
        if max(y) > maxV:
            maxV = max(y)
        ax.plot(x, y, label=labels[n])
    if data2:
        for n in data2:
            # if n != "ula":
            x = [v[0] for v in data2[n]]
            y = [v[1] for v in data2[n]]
            if n == "claWorkload":
                n = "Wcla"
            
            if min(y) < minV and min(y) > 0.000001:
                minV = min(y)
            if max(y) > maxV:
                maxV = max(y)

            ax.plot(x, y, label="bew-"+n)
    # print(data)
    # print(data2)
    ax.semilogx(base=2)
    ax.semilogy()
    ax.grid()
    ax.set_ylabel("Execution Time [ms]")
    ax.set_xlabel(xlabel)
    ax.xaxis.set_label_coords(0.5, -0.13)
    # ax.set_xticks([1, 2, 4, 8, 16, 32, 64, 128, 256])
    # ax.get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    ax.set_yticks(yticks)
    # ax.get_yaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    ax.legend(ncol=2, loc="upper center", bbox_to_anchor=(0.23, 1.09),
              fontsize=7.45, frameon=True)
    ax.yaxis.set_label_coords(-0.13, 0.4)
    ax.margins(x=0)
    plt.ylim([minV / 1.8, maxV ])
    dy = 5/72.
    dx = -6.3/72.
    for idx, label in enumerate(ax.xaxis.get_majorticklabels()):
        offset = matplotlib.transforms.ScaledTranslation(
            dx, dy, fig.dpi_scale_trans)
        label.set_transform(label.get_transform() + offset)
    plt.subplots_adjust(
        left=0.15, right=0.98, top=0.95, bottom=0.2, wspace=0.35, hspace=0.35
    )
    # plt.title(title)
    plt.savefig(outputFilePath)
    plt.close()


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-x", "--machines", nargs="+", required=False)
args = parser.parse_args()
machinesList = args.machines
for machine in machinesList:
    tableFile = "plots/microbenchmark/tab/table_mml_scale_"+machine+".csv"
    xlabel = "# rows in left matrix"
    data = parsMM(tableFile)
    if data != {}:
        keys = ["cla-sysml-singlenode-sysmlMM_mml",
                "ulab16-singlenodeMM_mml",
                "clab16-singlenodeMM_mml",
                "claWorkloadb16-singlenodeMM_mml"]
        plotMM(data, "plots/microbenchmark/mm/mml_census_"+machine+".pdf",
               "MM Left Census", keys, xlabel=xlabel,
               yticks=[10, 100, 1000, 10000])

    tableFile = "plots/microbenchmark/tab/table_mmr_scale_"+machine+".csv"
    xlabel = "# cols in right matrix"
    data = parsMM(tableFile)
    if data != {}:
        keys = ["cla-sysml-singlenode-sysmlMM_mmr",
                "ulab16-singlenodeMM_mmr",
                "clab16-singlenodeMM_mmr",
                "claWorkloadb16-singlenodeMM_mmr"]
        plotMM(data, "plots/microbenchmark/mm/mmr_census_"+machine+".pdf",
               "MM Right Census", keys, xlabel=xlabel,
               yticks=[1, 10, 100, 1000, 10000, 100000])

