
from re import S
import warnings

warnings.filterwarnings("ignore")

import os

import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.transforms
import numpy as np
import matplotlib

mpl.rcParams["font.family"] = "serif"
plt.rcParams.update({'hatch.color': '#0a0a0a00'})
plt.rcParams.update({'hatch.linewidth': 1.2})
# print(plt.rcParams.keys())

# mpl.rcParams["font.family"] = "sans-serif"
# mpl.rcParams["font.family"] = ["LinLibertine"] #"cmss10" , "Computer Modern Sans Serif"]
# mpl.rcParams["font.serif"] = "Computer Modern Sans Serif"
# plt.rcParams["font.monospace"] = ["Computer Modern Typewriter"]

def pars(path):
    data = {}
    first_line = True
    if os.path.isfile(path):
        with open(path) as f:
            for line in f:
                if first_line:
                    first_line = False
                    continue
                split = [x.strip() for x in line.split(",")]
                ex = split[0]
                if ex not in data.keys():
                    data[ex] = []
                if "No File at" in line or "Failed Parsing" in line:
                    data[ex].append("Nan")
                else:
                # idx = (split[2] + "-" + split[1]).replace(" ", "-")
                    data[ex].append(float(split[3]))

    return data


def plotBar(data, outputFilePath, yticks):
    times = [[], [], [], [], [], [], []]
    names = ["ML-ULA", "CLA", "ULA", "Mem", "MemG", "AWARE", "AWAREG"]
    plotBarWithNames(data, outputFilePath, yticks, times, names)


def plotBarPartial(data, outputFilePath, yticks):
    times = [[], [], [], []]
    names =  ["CLA", "ULA", "Mem", "AWARE"]
    plotBarWithNames(data, outputFilePath, yticks, times, names)

def plotBarWithNames(data, outputFilePath, yticks, times, names):
    # yticks = []
    minV =10000000
    maxV = 0.0000001
    # labels = []
    for x in data:
        # labels.append(x)
        for idx, v in enumerate(data[x]):
            if times[idx] is None:
                times[idx] = []
            if v < minV and v > 0:
                minV = v
            if v > maxV:
                maxV = v
            times[idx].append(v)

    # if minV

    # labels[0] = "covtype"
    # labels[3] = "infimnist"
    # labels[4] = "census_enc"

    x = np.arange(len(times[0]))
    width = 0.9 / len(times)
    # latex_column_size = (42 / 6 * 1.0, 3 * 1.0)
    fix, ax = plt.subplots(
        1,
        1,
        num=None,
        figsize=((42) / 6 * 1.0 / 2, 3 * 0.5),
        dpi=80,
        facecolor="w",
        edgecolor="k",
    )
    # oddOffset = -((width / 2) * (len(times) % 2))
    oddOffset = 0 #-((width / 2) * (len(times) % 2))
    # oddOffset = (width) * ((len(times)) % 2) + width / 2
    startOffset = oddOffset - width * ((len(times)-1) / 2)

    hatchs = ["////", "\\\\\\\\", "----", "||||", "o", "*", "", "", "", "", "", ""]
    for idx, bars in enumerate(times):
        # label = ""
        # if "ula" in runs[idx]:
        #     label = "ULA" + runs[idx][27:]
        # else:
        #     label = "CLA" + runs[idx][35:]
        off = x + startOffset + width * idx
        ax.bar(off, bars, width, label=names[idx], hatch=hatchs[idx])
        # if idx > 0:
        # for idy, t in enumerate(bars):
        #     offy = -30
        #     if np.isnan(t):
        #         # continue
        #         ax.annotate(
        #             "Out Of Memory",
        #             xy=(off[idy], 1),
        #             xytext=(0, 3),
        #             textcoords="offset points",
        #             ha="center",
        #             va="bottom",
        #             rotation=90,
        #             fontsize=annotationfontSize
        #         )
        #     if idx > 0:
        #         speedup = times[0][idy] / t
        #         if speedup > 0:
        #             if t < yticks[2]:
        #                 offy = 3
        #             vf = "{0:2.1f}x".format(speedup)
        #             if speedup > 100:
        #                 vf = "{0:2.0f}x".format(speedup)
        #             ax.annotate(
        #                 vf,
        #                 xy=(off[idy], t),
        #                 xytext=(0, offy),
        #                 textcoords="offset points",
        #                 ha="center",
        #                 va="bottom",
        #                 rotation=90,
        #                 fontsize=annotationfontSize
        #             )

    ax.set_ylabel("Execution Time [ms]")
    # ax.set_xlabel("# Replication")

    ax.set_xticks(x)
    # ax.set_yscale("log")
    # ax.semilogy()

    # ax.set_yticks(yticks)

    absMin = max(minV/ 1.8, 0.0001)
    absMax = maxV * 3
    ax.set_yscale("log")

    yticks = []
    s = 10 ** math.ceil(math.log10(absMin))
    while(s <= absMax):
        yticks.append(int( s))
        s = s * 10

    plt.ylim([absMin, absMax])
    if yticks is not []:
        ax.set_yticks(yticks)

    # if 0.1 in yticks:
    #     yticsA = []
    #     for x in yticks:
    #         if x != 0.1:
    #             yticsA.append(x)
    # ax.set(yticklabels=yticks)
    # ax.get_yaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    ax.set_xticklabels(["Covtype", "Census", "Airline", "Mnist1m", "Census Enc"])
    # ax.legend()
    ax.legend(
        ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.07), 
        fontsize=7.45, frameon=False
    )
    ax.yaxis.set_label_coords(-0.13, 0.43)
    ax.margins(x=width / len(times))
    fix.autofmt_xdate(rotation=10)
    dy = 5/72. 
    for idx, label in enumerate(ax.xaxis.get_majorticklabels()):
        dx = (idx) * 6.3/72. 
        offset = matplotlib.transforms.ScaledTranslation(dx, dy, fix.dpi_scale_trans)
        label.set_transform(label.get_transform() + offset)
    plt.subplots_adjust(
        left=0.15, right=0.99, top=0.96, bottom=0.18, wspace=0.35, hspace=0.35
    )
    plt.grid(True,"major",axis='y', ls='--',linewidth=0.3, alpha=0.8)
    plt.savefig(outputFilePath,dpi=1600)
    plt.close()
