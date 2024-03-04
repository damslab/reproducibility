import matplotlib.pyplot as plt
import plot_util as pu
import numpy as np
import pandas as pd
import os


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def plot(d1, name):
    _, ax = plt.subplots(
        1, 1, num=None, figsize=pu.fig_size, dpi=pu.dpi, facecolor="w", edgecolor="k"
    )

    d1 = d1.loc[d1["Time"] > 0]

    confs = d1.Type.unique()
    min_ts = 130212512
    max_ts = 0

    markers = ["o", "v", "s", "x", "*"]
    for ic, c in enumerate(confs):
        d = d1.loc[d1["Type"] == c]
        # print(d)
        min_ts = min(min(d.Size), min_ts)
        max_ts = max(max(d.Size), max_ts)
        pu.add_line(
            ax, d.Size, d.SysDSTime, np.zeros(len(d.Time)), c, "--", marker=markers[ic]
        )
        # pu.add_line(
        #     ax, d.Size, d.Time, np.zeros(len(d.Time)), c, "--", marker=markers[ic]
        # )

    ax.grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)

    ax.set_yscale("log", base=10)
    ax.set_xscale("log", base=10)
    pu.set_tics_x_log10(ax, min_ts, max_ts)
    ax.xaxis.set_label_coords(0.5, -0.3)
    ax.legend(ncol=2, loc="upper center", bbox_to_anchor=(0.32, 1.27), fontsize=7.45)

    ax.set_xlabel("# Rows")
    ax.set_ylabel("Execution Time [Sec]")
    plt.subplots_adjust(
        left=0.15, right=0.97, top=0.85, bottom=0.28, wspace=0.35, hspace=0.35
    )

    plt.savefig("plotting/plots/kmeans/criteo/" + name + ".pdf")


d1 = pd.read_csv("plotting/tables/kmeans10/criteo/log_dams-su1.csv")

plot(d1, "kmeans-su1")

d1 = pd.read_csv("plotting/tables/kmeans10/criteo/log_dams-su1.csv")
plot(d1, "kmeans10-su1")

mkdir("./plotting/plots")
mkdir("./plotting/plots/kmeans/")
mkdir("./plotting/plots/kmeans/criteo")
