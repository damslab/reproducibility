import argparse
import os
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.transforms

mpl.rcParams["font.family"] = "serif"
plt.close("all")
latex_column_size = (42 / 6 * 1.0, 3 * 1.0)


def parse_timestamp(timeString):
    sp = timeString[5:].split("m")
    time = int(sp[0]) * 60
    time += float(sp[1][:-2].replace(",", ""))
    return time


def parse_systemds(path):
    if os.path.isfile(path):
        time = 0
        io = 0
        with open(path) as f:
            for line in f:
                if "real\t" in line:
                    time = parse_timestamp(line)
                if "Cache times (ACQr/m, RLS, EXP):" in line:
                    io = float(line[32:-5].split("/")[0])
        return time, io
    else:
        # print("Missing : " + path)
        return 0, 0


def parse_tensorflow(path):
    if os.path.isfile(path):
        time = 0
        io = 0
        with open(path) as f:
            for line in f:
                if "real\t" in line:
                    time = parse_timestamp(line)
                if "IO Time:" in line:
                    io = float(line[8:])
        return time, io
    else:
        # print("Missing : " + path)
        return 0, 0


def parse_avg(path_template, number=10, tensorflow=True):
    times = []
    io = []
    for i in range(1, number):
        if tensorflow:
            t = parse_tensorflow(path_template.format(i=i))
        else:
            t = parse_systemds(path_template.format(i=i))
        if t[0] > 0.0:
            times.append(t[0])
            io.append(t[1])

    if len(times) == 0:
        return 0, 0
    # Remove outliers... did not make a difference.
    # if len(times)> 3:
    #     maxTime = max(times)
    #     minTime = min(times)
    #     tmp = times 
    #     tmpIO = io 
    #     times=[]
    #     io =[]
    #     for i in range(len(tmp)):
            
    #         if maxTime == tmp[i] or  minTime == tmp[i]:
    #             continue

    #         times.append(tmp[i])
    #         io.append(tmpIO[i])
        
    ret = (np.average(times), np.average(io))
    if np.isnan(ret[0]) or np.isnan(ret[1]):
        return 0, 0
    return ret


def plot_times(times, outputFilePath):
    # if t in times:
    #     if t == (0,0):
    #         t = (1,1)
    # return
    if len(times) == 0:
        return
    fix, ax = plt.subplots(
        1,
        1,
        num=None,
        figsize=(latex_column_size[0]/1.3, latex_column_size[1] * 0.45),
        dpi=80,
        facecolor="w",
        edgecolor="k",
    )

    colors = [
        "tab:cyan",
        "tab:gray",
        "tab:purple",
        "tab:brown",
        "tab:pink",
        "tab:orange",
        "goldenrod",
        "tab:red",
        "tab:olive",
        "tab:green",
        "tab:blue",
    ]

    for idx, _ in enumerate(times):
        # print(times[idx])
        ax.bar(idx-0.2, times[idx][0], 0.5,
               # label=names[idx]
               color=colors[idx],
               )
        ax.bar(
            idx,
            times[idx][0] - times[idx][1],
            0.5,
            # label=names[idx],
            color=colors[idx],
        )
        # Overlapping bar to make it slightly more white
        ax.bar(
            idx,
            times[idx][0] - times[idx][1],
            0.5,
            # label=names[idx],
            color="white",
            alpha=0.5,
        )
        ax.bar(idx + 0.2, times[idx][1], 0.5,
               #    label=names[idx],
               color=colors[idx])
        ax.bar(idx + 0.2, times[idx][1], 0.5,
               #    label=names[idx],
               color="white", alpha=0.7)

        ax.annotate(
            "{0:0.1f}".format(times[idx][0]),
            xy=(idx, times[idx][0]),
            xytext=(0, 0),
            textcoords="offset points",
            ha="center",
            va="bottom",
        )

        t = ax.annotate("IO", xy=(idx+0.1, 4.5), xytext=(0, 0),
                        textcoords="offset points",
                        ha="center",
                        va="bottom",
                        weight='bold',
                        size=3.4, alpha=0.6)
        t.set_rotation(90)
        t = ax.annotate("Compute", xy=(idx-0.15, 4.5), xytext=(0, 0),
                        textcoords="offset points",
                        ha="center",
                        va="bottom",
                        weight='bold',
                        size=3.4, alpha=0.6)
        t.set_rotation(90)
        t = ax.annotate("Total", xy=(idx-0.35, 4.5), xytext=(0, 0),
                        textcoords="offset points",
                        ha="center",
                        va="bottom",
                        weight='bold',
                        size=3.4, alpha=0.6)
        t.set_rotation(90)
        # ax.annotate(
        #     "{0:0.1f}".format(times[idx][1]),
        #     xy=(idx + 0.4, times[idx][1]),
        #     xytext=(0, idx),
        #     textcoords="offset points",
        #     ha="center",
        #     va="bottom",
        # )
    ax.annotate("TensorFlow", xy=(2, 3000), xytext=(0, 0), weight='bold',
                textcoords="offset points", ha="center", va="bottom")
    ax.plot((4.5, 4.5), (4, 7000), 'k--', linewidth=0.4, alpha=0.8)
    ax.annotate("ULA", xy=(5.5, 3000), xytext=(0, 0), weight='bold',
                textcoords="offset points", ha="center", va="bottom")
    ax.plot((6.5, 6.5), (4, 7000), 'k--', linewidth=0.4, alpha=0.8)
    ax.annotate("AWARE", xy=(7.5, 3000), xytext=(0, 0), weight='bold',
                textcoords="offset points", ha="center", va="bottom")
    ax.set_ylabel("Execution Time [s]")
    # ax.set_xlabel("# Replication")
    yticks = [10, 100, 1000]
    ax.set_yscale("log")
    ax.set_ylim([4, 9000])
    ax.set_yticks(yticks)
    # ax.get_yaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    ax.set_xticks(range(9))
    ax.set_xticklabels([
        "FP64", "FP32", "BF16", "SFP64", "SFP32", "Mt", "St",  "Mt", "St",
    ])
    ax.yaxis.set_label_coords(-0.08, 0.43)
    # fix.autofmt_xdate(rotation=15)
    dy = 3/72.
    dx = 0./72.
    for idx, label in enumerate(ax.xaxis.get_majorticklabels()):
        offset = matplotlib.transforms.ScaledTranslation(
            dx, dy, fix.dpi_scale_trans)
        label.set_transform(label.get_transform() + offset)
    # plt.subplots_adjust(
    #     left=0.15, right=0.99, top=0.96, bottom=0.18, wspace=0.35, hspace=0.35
    # )
    # ax.legend()
    # ax.legend(
    #     ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.05), fontsize="x-small"
    # )
    ax.margins(x=0.01)
    # fix.autofmt_xdate(rotation=15)
    plt.grid(True, "major", axis='y', ls='--', linewidth=0.3, alpha=0.8)
    plt.subplots_adjust(
        left=0.105, right=0.995, top=0.98, bottom=0.14, wspace=0.35, hspace=0.35
    )
    plt.savefig(outputFilePath)
    plt.close()


parser = argparse.ArgumentParser()
parser.add_argument("-x", "--machines", nargs="+", required=False)
args = parser.parse_args()
machinesList = args.machines

for machine in machinesList:
    try:
        base = "results/tensorflow/" + machine
        times = []
        # Tensorflow:

        times.append(parse_avg(base + "/tlrG-{i}.log"))
        times.append(parse_avg(base + "/tlrG-FP32-{i}.log"))
        times.append(parse_avg(base + "/tlrG-BF16-{i}.log"))
        times.append(parse_avg(base + "/tlrG-Sparse-{i}.log"))
        times.append(parse_avg(base + "/tlrG-SparseFP32-{i}.log"))

        # ULA
        times.append(parse_avg(base + "/ds_ula-{i}.log", tensorflow=False))
        times.append(parse_avg(base + "/ds_STR-{i}.log", tensorflow=False))

        # AWARE
        times.append(parse_avg(base + "/ds_claWorkload-{i}.log", tensorflow=False))
        times.append(parse_avg(base + "/ds_claWorkloadSTR-{i}.log", tensorflow=False))

        resFile = "plots/microbenchmark/comp/tensorflow_compare_" + machine+".pdf"
        plot_times(times, resFile)
    except:
        continue
        # do nothing.
