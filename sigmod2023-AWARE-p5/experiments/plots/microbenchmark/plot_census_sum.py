import os
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# mpl.rcParams["font.family"] = "serif"
# plt.close("all")

tableFile = "plots/microbenchmark/table_census.csv"
latex_column_size = (42 / 6 * 1.0, 3 * 1.0)


def pars(functionName, machine, path=tableFile):
    data = {}
    first_line = True
    if os.path.isfile(path):
        with open(path) as f:
            for line in f:
                if first_line:
                    first_line = False
                    continue
                split = [x.strip() for x in line.split(",")]
                # print(split[1])
                # if functionName == split[1]:
                ex = split[0]
                if ex not in data.keys():
                    data[ex] = {}
                # if(functionName not in data.get(split[0]).keys()):
                #     data[split[0]][functionName] = {}
                # if(split[2] not in data.get(split[0]).keys()):
                #     data[split[0]][split[2]] = []
                idx = (split[2] + "-" + split[1]).replace(" ", "-")
                # print(idx)
                # print(data)

                data[ex][idx] = abs(float(split[1 + machine * 2])) + 0.0000001

    return data


def plotBar(
    data,
    outputFilePath,
    title,
    runs,
    yticks=[1, 10, 100, 1000],
    seconds=False,
    scale=True,
):

    times = []
    for x in runs:
        times.append([])
    labels = []
    for x in data:
        labels.append(x)
        for idx, r in enumerate(runs):
            if seconds and scale:
                times[idx].append(data[x][r] * 0.001)
            else:
                times[idx].append(data[x][r])

    # labels = ["1","4","8","16","32","128"]
    labels = ["1", "4", "8", "16"]
    x = np.arange(len(times[0]))
    width = 0.8 / len(data)

    fix, ax = plt.subplots(
        1,
        1,
        num=None,
        figsize=((42) / 6 * 1.0 / 2, 3 * 0.7),
        dpi=80,
        facecolor="w",
        edgecolor="k",
    )
    # oddOffset = -((width / 2) * (len(runs) % 2))
    oddOffset = (width) * ((len(runs)) % 2) + width / 2
    startOffset = oddOffset - width * (len(runs) / 2)

    for idx, bars in enumerate(times):
        label = ""
        if "ula" in runs[idx]:
            label = "ULA" + runs[idx][20:]
        else:
            label = "CLA" + runs[idx][28:]
        off = x + startOffset + width * idx
        ax.bar(off, bars, width, label=label)
        if idx > 1:
            for idy, t in enumerate(bars):
                offy = -30

                speedup = times[(idx) % 2][idy] / t
                if speedup > 0:
                    if t < yticks[1]:
                        offy = 3
                    vf = "{0:2.1f}x".format(speedup)
                    if speedup > 100:
                        vf = "{0:2.0f}x".format(speedup)
                    ax.annotate(
                        vf,
                        xy=(off[idy], t),
                        xytext=(0, offy),
                        textcoords="offset points",
                        ha="center",
                        va="bottom",
                        rotation=90,
                    )
        for idy, t in enumerate(bars):
            offy = -30
            if np.isnan(t):
                ax.annotate(
                    "OOM",
                    xy=(off[idy], 1),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    rotation=90,
                )
    ax.set_ylabel("Execution Time [ms]")
    ax.set_xlabel("# Replication Census Enc")

    ax.set_xticks(x)
    ax.set_yscale("log")
    ax.set_yticks(yticks)
    # ax.get_yaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    ax.set_xticklabels(labels)
    # ax.legend()
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(
        0.5, 1.05),  fontsize='x-small')
    ax.margins(x=0)
    # fix.autofmt_xdate(rotation=20)
    # plt.title(title)
    plt.subplots_adjust(
        left=0.20, right=0.99, top=0.97, bottom=0.25, wspace=0.35, hspace=0.35
    )
    plt.savefig(outputFilePath)
    plt.close()


# def p5():
#     data = pars("UA sum", 1)
#     print (data)
#     if data != {}:
#         plotBar(data, "plots/microbenchmark/ua/sum_census.pdf",
#             "Sum", ["ulab16-hybrid-UA-sum", "ulab16-hybrid-UA-sum+",
#                     "claWorkloadb16-hybrid-UA-sum", "claWorkloadb16-hybrid-UA-sum+"])


# if __name__ == '__main__':
#     p5()
