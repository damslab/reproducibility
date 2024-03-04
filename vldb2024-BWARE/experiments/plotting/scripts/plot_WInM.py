from pathlib import Path

import matplotlib.pyplot as plt

import plot_util as pu
import math
import numpy as np


def splitV(v):
    try:
        data = v.split(",")
        time = data[0].split("+-")
        inSize = data[1].split("+-")
        outSize = data[2].split("+-")
        time[1] = time[1][:-2]
        inSize[1] = inSize[1][:-6]
        outSize[1] = outSize[1][:-6]
        time = [float(x.strip()) for x in time]
        inSize = [float(x.strip()) for x in inSize]
        outSize = [float(x.strip()) for x in outSize]
        return time, inSize, outSize
    except Exception as e:
        print(e)
        print(v)
        exit(-1)


def parse(path):
    data = {}
    with open(path) as f:
        for l in f:
            if "Profiling started\n" in l:
                continue
            elif len(l) < 4:
                # elif "Performance counter " in l:
                return data
            elif " WriteTest  Repetitions:" in l:
                continue
            # Everything else:
            kv = l.split(",", 1)
            if len(kv) > 1:
                k = kv[0].strip()
                v = kv[1].strip()
                data[k] = splitV(v)
    return data


def parse_params(path):
    p = str(path)
    f = p.split("/")[-1]
    return f[5:-4].split("-")


def use_key(props, key):
    return key(
        rows=props[0], cols=props[1], sp=props[3], uniq=props[2], threads=props[4]
    )


def key_1(rows, cols, sp, uniq, threads):
    return rows + "_" + cols + "_" + sp + "_" + uniq


def order_1(rows, cols, sp, uniq, threads):
    return int(threads)


def take_1(data):
    ret = {}
    for k in data:
        ret[k] = data[k][1]
    return ret


def filter_1(data):
    return float(data[3]) == 1.0 and float(data[0]) == 10000 and float(data[2]) == 64


def fix(d):
    ret = {}
    for k in d:
        a = d[k]
        for aa in a:
            for key in aa[1]:
                full_key = k + "_" + key
                if full_key in ret.keys():
                    ret[full_key].append([aa[0], aa[1][key]])
                else:
                    ret[full_key] = [[aa[0], aa[1][key]]]

                ret[full_key].sort()

    for k in ret:
        ret[k] = [[a[0], a[1][0], a[1][1]] for a in ret[k]]
    return ret


def parse_all(machine, t=take_1, k=key_1, o=order_1, f=filter_1):
    path_list = Path("results/performance/" + machine).glob("WinM/**/*.log")
    ret1 = {}
    for p in path_list:
        props = parse_params(p)
        if f(props):
            d = parse(p)
            if d == None:
                continue
            key = use_key(props, k)
            ord = use_key(props, o)
            if key in ret1.keys():
                ret1[use_key(props, k)].append([ord, t(d)])
            else:
                ret1[use_key(props, k)] = [[ord, t(d)]]

    ret = fix(ret1)
    return ret


def plot(d, machine, name="plt"):
    if len(d) == 0:
        return

    _, ax = plt.subplots(
        1, 1, num=None, figsize=pu.fig_size, dpi=pu.dpi, facecolor="w", edgecolor="k"
    )

    # ax.set_xscale('log', base=2)
    # x = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    y_tics = [math.pow(10, x) for x in range(15)]
    # y_labels = ["B/s", "$10$", "$10^(2)$", "KiB/s", "$10^4$", "$10^5$",
    #             "MiB/s", "$10^7$", "$10^8$", "GiB/s", "$10^[10]$", "$10^11$", "TiB/s"]
    ymin = None
    ymax = None
    x_tics = []
    for k in d:
        x = np.array([a[0] for a in d[k]])
        y = np.array([a[1] for a in d[k]])
        err = np.array([a[2] for a in d[k]])
        pu.add_line(ax, x, y, err, k, "dashed", "o", markersize=1)

        if ymin == None:
            ymin = min(y)
            ymax = max(y)
        else:
            ymin = min(min(y), ymin)
            ymax = max(max(y), ymax)
        if len(x) > len(x_tics):
            x_tics = x
    if "so" in machine:
        bandwidth = 200 * 1024 * 1024 * 1024
    elif machine == "XPS-15-7590":
        bandwidth = 21333 * 1024 * 1024 * 2
    ax.axhline(bandwidth, 0, max(x_tics), label="MemBandWidth", linewidth=0.5)

    ymax = max(bandwidth, ymax)

    ax.set_ylabel("In [B/sec]")
    ax.set_xlabel("# Threads")
    if len(x) < 10:
        ax.set_xticks(x)
    ax.set_yscale("log")
    # ax.set_yticklabels(y_labels[7:])
    ax.set_yticks(y_tics[7:])
    ax.set_ylim([ymin / 5, ymax * 5])

    ax.set_xmargin(0)
    plt.subplots_adjust(
        left=0.25, right=0.95, top=0.85, bottom=0.28, wspace=0.35, hspace=0.35
    )
    ax.legend(ncol=2, loc="upper center", bbox_to_anchor=(0.35, 1.27), fontsize=3.0)
    plt.grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)
    plt.savefig("plotting/plots/Performance/" + machine + "/" + name + ".pdf", dpi=1600)

    plt.close()


def filter_2(d):
    return d[0] == "100000" and d[1] == "1000" and d[3] == "0.01"


def filter_800MB100(d):
    return d[0] == "100000" and d[1] == "1000" and d[3] == "1.0"


def filter_1sparsity(d):
    return d[3] == "0.01" and d[2] == "64"


def filter_38sparsity(d):
    return d[3] == "0.38" and d[2] == "64"


def filter_noSparse(d):
    return d[3] == "1.0" and d[2] == "64"


if __name__ == "__main__":
    m = "dams-so010"
    plot(parse_all(m, f=filter_1), m)
    plot(parse_all(m, f=filter_800MB100), m, "800MB100%")
    m = "XPS-15-7590"
    plot(parse_all(m, f=filter_2), m, "12MB1%")
    plot(parse_all(m, f=filter_800MB100), m, "800MB100%")
    plot(parse_all(m, f=filter_1sparsity), m, "1%Sparsity")
    plot(parse_all(m, f=filter_38sparsity), m, "38%Sparsity")
    plot(parse_all(m, f=filter_noSparse), m, "Dense")
    m = "dams-so002"
    plot(parse_all(m, f=filter_1sparsity), m, "1%Sparsity")
    plot(parse_all(m, f=filter_38sparsity), m, "38%Sparsity")
    plot(parse_all(m, f=filter_noSparse), m, "Dense")

    m = "dams-so011"
    plot(parse_all(m, f=filter_1sparsity), m, "1%Sparsity")
    plot(parse_all(m, f=filter_38sparsity), m, "38%Sparsity")
    plot(parse_all(m, f=filter_noSparse), m, "Dense")
