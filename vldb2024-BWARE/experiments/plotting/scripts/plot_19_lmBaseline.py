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
        "Sal",
        "San",
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

    mx = 1
    mi = 1000000000
    bar_labels = ["String", "Detected", "BWARE"]

    namesf = [
        "adult",
        "cat",
        "criteo",
        "crypto",
        "kdd",
        "salaries",
        "santander",
        "home",
    ]


    for id, ax in enumerate(axi):
        r = df.loc[df["name"] == namesf[id]]
        ula = r.loc[df.Conf == "ULAb16"].loc[df.FileType == "bin"]
        awa = r.loc[df.Conf == "TAWAb16"].loc[df.FileType == "cla"]

        ax.bar(
            [0],
            ula.Time,
            color="tab:blue",
            label="ULA"
        )
        if ula.Time.any():
            mi = min(min(ula.Time), mi)
            mx = max(max(ula.Time), mx)
        ax.bar(
            [1],
            awa.Time,
            color="tab:brown",
            label="BWARE+Morphing"
        )

        if awa.Time.any():
            mi = min(min(awa.Time), mi)
            mx = max(max(awa.Time), mx)

        ax.grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)
        ax.grid(True, "minor", axis="y", ls="dotted", linewidth=0.2, alpha=0.9)

        if id not in [2]:
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
                0.025,
                names[id],
                bbox=dict(boxstyle="square", pad=0.1, fc="w", ec="k", lw=0.1),
                rotation=90,
                size=6,
                ha="left",
                va="bottom",
                transform=ax.transAxes,
            )

    for id, ax in enumerate(axi):
        ax.set_xticks([])
        # r = df.loc[df["name"] == namesf[id]]
        # x = np.array([float(x[1:]) for x in r["lossy"]]) * 5
        # ax.set_xscale("log", base=10)
        # if len(x) > 1:
            # xtics = pu.set_tics_x_log10(ax, min(x[1:]) * 0.7, max(x[1:]) * 1.3, lim=2)
        ax.set_yscale("log", base=10)
        ax.tick_params(axis="y", labelsize=7)
        ax.tick_params(axis="x", labelsize=5)
        ytics = pu.set_tics_y_log10(ax, mi * 0.6, mx * 1.4)
        if id == 0:
            ax.set_ylabel("Time [s]", size=8)
        else:
            ax.set_yticklabels(["" for x in range(len(ytics))])

    axi[6].legend(
        ncol=6,
        loc="lower center",
        bbox_to_anchor=(-3.0, 0.95),
        fontsize=7,
        markerscale=0.6,
        handlelength=1.5,
        columnspacing=0.8,
        handletextpad=0.1,
    )

    plt.subplots_adjust(
        left=0.135, right=0.997, top=0.74, bottom=0.01, wspace=0.17, hspace=0.30
    )
    out = "plotting/plots/lm_baseline_" + m + "_time.pdf"

    print("Script", "/plotting/scripts/plot_19_lmBaseline.py", "out:", out)
    plt.savefig(out)



df = pd.read_csv("plotting/tables/19-LMBaseline/dams-su1.csv")
plot(df, "su1")
# df = pd.read_csv("plotting/tables/te/dams-su1_lossy.csv")
# plot(df, "su1")
