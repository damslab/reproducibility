import pandas as pd
import plot_util as pu

import matplotlib.pyplot as plt
import numpy as np

def plot(df, m):
    fig_size = (3.33, 0.8)
    names = [
        "Adult",
        "Cat",
        "Crit10M",
        "Crypto",
        "KDD",
        "Salaries",
        "Santander",
        "Home",
    ]
    fig, axi = plt.subplots(
        1,
        len(names),
        num=None,
        figsize=fig_size,
        dpi=pu.dpi,
        facecolor="w",
        edgecolor="k",
    )

    # mx = 10
    mi = 0
    bar_labels = ["String", "Detected", "BWARE"]

    namesf=[
        "adult",
        "cat",
        "criteo",
        "crypto",
        "kdd",
        "salaries",
        "santander",
        "home",

    ]

    color =[
        # "tab:blue"
        (42/256,186/256,212/256),
        "tab:orange",
        "tab:green",
        (196/256, 13/256, 30/256, 0.7)
    ]

    heights = []

    for id, ax in enumerate(axi):
        r = df.loc[df["name"] == namesf[id]]
        if len(r) == 0:
            r = {"FMRead":[0],"FMDetectSchema":[0],"FMApplySchema":[0],"FMTE":[0]}
      
        # s = r["FMCompile"]
        # ax.bar([0], s, label = "Compile", zorder = 3)
        s =  r["FMRead"]
        ax.bar([0], s, label = "I/O", zorder = 2, color=color[0])
        if np.array(r["FMRead"])[0]  < 2* np.array(r["FMDetectSchema"])[0]: # correct the included read time 
            s = s + r["FMDetectSchema"] - r["FMRead"]
        else:
            s = s + r["FMDetectSchema"] 
        ax.bar([0], s, label = "Detect Schema", zorder = 1, color=color[1])
        s = s + r["FMApplySchema"]
        ax.bar([0], s, label = "Apply Schema", zorder = 0, color=color[2])
        s = s + r["FMTE"]
        ax.bar([0], s, label = "Transform Encode", zorder = -1, color=color[3])

        heights.append(np.array(s)[0])
        ax.grid(True, "major", axis="y", ls="--", linewidth=0.4, alpha=1.0)

        ax.text(
                0.94,
                0.025,
                names[id],
                bbox=dict(boxstyle="square", pad=0.1, fc="w", ec="k", lw=0.1),
                rotation=90,
                size=6,
                ha="right",
                va="bottom",
                transform=ax.transAxes,
            )



    for id, ax in enumerate(axi):
        r = df.loc[df["name"] == namesf[id]]
        # ax.set_xscale("log", base=10)
        # if len(r) == 1:
        #     xtics = pu.set_tics_x_log10(ax, min(r[1:]) * 0.7,max(r[1:])* 1.3, lim=2)
        # ax.set_yscale("log", base=10)
        ax.tick_params(axis="y", labelsize=5)
        # ax.tick_params(axis="x", labelsize=5)
        pu.set_tics_y(ax, 0, heights[id], 4)
        # ytics = pu.set_tics_y(ax, mi * 0.6, mx * 1.4)
        if id == 0:
            ax.set_ylabel("Time [s]", size=8)
        # else:
            # ax.set_yticklabels([""])
        ax.set_xticks=([0, 1])
        ax.set_xticklabels(["", ""])
        # ax.yaxis.get_majorticklabels()[2].set_y(-.1)

    axi[7].legend(
        ncol=6,
        loc="upper center",
        bbox_to_anchor=(-7.0, 1.4),
        fontsize=6,
        markerscale=0.6,
        handlelength=1.5,
        columnspacing=0.8,
        handletextpad=0.1,
    ).set_zorder(1000000)

    plt.subplots_adjust(
        left=0.11, right=0.99, top=0.75, bottom=0.04, wspace=1.1, hspace=0.30
    )

    plt.savefig("plotting/plots/micro_cost_breakdown_" + m + ".pdf")


df = pd.read_csv("plotting/tables/te/XPS-15-7590_full.csv")
plot(df, "XPS-15-7590")
df = pd.read_csv("plotting/tables/te/dams-su1_full.csv")
plot(df, "su1")
