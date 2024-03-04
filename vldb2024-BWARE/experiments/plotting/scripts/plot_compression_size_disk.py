import pandas as pd
import plot_util as pu

import matplotlib.pyplot as plt
import numpy as np


def plot(df, m):
    fig_size = (3.33, 0.8)
    fig, axi = plt.subplots(
        1,
        df.shape[0],
        num=None,
        figsize=fig_size,
        dpi=pu.dpi * 20,
        facecolor="w",
        edgecolor="k",
    )

    mx = 10000
    mi = 100000000
    bar_labels = [None, None, "Snappy", "ZStd", None, "BEWARE-Snappy", "BEWARE-ZStd"]

    names = [
        "Adult",
        "Cat",
        "Crit10M",
        "Crypto",
        "KDD",
        "Salaries",
        "San",
        "Home",
    ]
    for id, ax in enumerate(axi):
        r = df.loc[id]

        if(r.CompDisk < 0) or np.isnan(np.array(r.CompDisk)).any():
            continue            

        # for ii in range(7):

        ec = "black"
        ax.bar([0], r.OrgDiskSize, label=None, color="tab:red", edgecolor=ec, lw=0.01)
        ax.bar(
            [1], r.SchemaDiskSize, label=None, color="tab:blue", edgecolor=ec, lw=0.01
        )
        ax.bar(
            [2],
            r.OrgDiskSnappy,
            label="Snappy",
            color="tab:blue",
            edgecolor="tab:purple",
            lw=0.01,
            hatch="...",
        )
        ax.bar(
            [3],
            r.OrgDiskZstd,
            label="ZStd",
            color="tab:blue",
            edgecolor="tab:green",
            lw=0.01,
            hatch="///",
        )
        ax.bar([4], r.CompDisk, label=None, color="tab:orange", edgecolor=ec, lw=0.01)
        ax.bar(
            [5],
            r.CompDiskSnappy,
            label="BEWARE-Snappy",
            color="tab:orange",
            edgecolor="tab:purple",
            lw=0.01,
            hatch="...",
        )
        ax.bar(
            [6],
            r.CompDiskZstd,
            label="BEWARE-ZStd",
            color="tab:orange",
            edgecolor="tab:green",
            lw=0.01,
            hatch="///",
        )


        mx = max(r.OrgDiskSize, mx)
        mi = min(r.CompDisk, mi)

        ax.grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)

        if id == 5 or id == 0:
            ax.text(
                0.94,
                0.97,
                names[id],
                bbox=dict(boxstyle="square", pad=0.1, fc="w", ec="k", lw=0.1),
                rotation=90,
                size=6,
                ha="right",
                va="top",
                transform=ax.transAxes,
            )

        else:
            ax.text(
                0.06,
                0.01,
                names[id],
                bbox=dict(boxstyle="square", pad=0.1, fc="w", ec="k", lw=0.1),
                rotation=90,
                size=6,
                ha="left",
                va="bottom",
                transform=ax.transAxes,
            )

        # print(df.loc[0])
    for id, ax in enumerate(axi):
        ax.set_xticks([])
        ax.set_yscale("log", base=10)
        ax.tick_params(axis="y", labelsize=7)
        ytics = pu.set_tics_y_log10(ax, mi * 0.3, mx * 1.4)
        if id == 0:
            ax.set_ylabel("Disk [B]", size=8)
            ax.yaxis.set_label_coords(-1.1, 0.5)
        else:
            ax.set_yticklabels(["" for x in range(len(ytics))])

    axi[7].legend(
        ncol=5,
        loc="upper center",
        bbox_to_anchor=(-4.5, 1.5),
        fontsize=7,
        markerscale=0.6,
        handlelength=1.5,
        columnspacing=0.8,
        handletextpad=0.1,
    )

    plt.subplots_adjust(
        left=0.135, right=0.99, top=0.68, bottom=0.01, wspace=0.17, hspace=0.30
    )

    plt.savefig("plotting/plots/compress_data_disk_" + m + ".pdf")


df = pd.read_csv("plotting/tables/comp/XPS-15-7590.csv")
plot(df, "XPS-15-7590")
df = pd.read_csv("plotting/tables/comp/dams-su1.csv")
plot(df, "su1")
