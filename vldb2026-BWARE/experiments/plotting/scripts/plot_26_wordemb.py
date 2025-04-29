import pandas as pd
import plot_util as pu

import matplotlib.pyplot as plt
import numpy as np


def plot(df, df2, m):
    fig_size = (3.3, 1.2)
    names = [
        "E2E",
        "TE",
    ]
    fig, axi = plt.subplots(
        2,
        3,
        num=None,
        figsize=fig_size,
        dpi=pu.dpi,
        facecolor="w",
        edgecolor="k",
    )

    # bar_labels = ["String", "Detected", "BWARE"]
    mx = 1
    mi = 1000000000

    max_x = 0
    min_x = 10000000
    namesf = [
        "Time",
        "TE",
    ]

    # color = ["tab:blue", "tab:orange", "tab:green", "tab:brown"]
    # words = [10000, 100000, 999995]

    for id, ax in enumerate(axi[0]):
        ax.grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)
        ax.grid(True, "minor", axis="y", ls="dotted", linewidth=0.2, alpha=0.9)

    for id, ax in enumerate(axi[1]):
        ax.grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)
        ax.grid(True, "minor", axis="y", ls="dotted", linewidth=0.2, alpha=0.9)

    # for id, words in enumerate([1000, 3000, 10000, 100000]):
    for id, words in enumerate([1000,  10000, 100000]):
        r = df.loc[df["conf"] == "ULAb16"].loc[df["words"] == words]
        if len(r) > 0:
            x = r.abstracts
            y = r.time
            axi[0][id].plot(x, y, color="tab:blue", alpha=0.6, label="ULA")
            mx = max(max(y), mx)
            mi = min(min(y), mi)
            max_x = max(max(x), max_x)
            min_x = min(min(x), min_x)

        r = df.loc[df["conf"] == "tf"].loc[df["words"] == words]
        if len(r) > 0:
            x = r.abstracts
            y = r.time
            axi[0][id].plot(x, y, color="tab:pink", alpha=0.6, label="TensorFlow 2.15")
            mx = max(max(y), mx)
            mi = min(min(y), mi)
            max_x = max(max(x), max_x)
            min_x = min(min(x), min_x)

        r = df.loc[df["conf"] == "AWAb16"].loc[df["words"] == words]
        if len(r) > 0:
            x = r.abstracts
            y = r.time
            axi[0][id].plot(x, y, color="tab:brown", alpha=0.6, label="BWARE")
            mx = max(max(y), mx)
            mi = min(min(y), mi)
            max_x = max(max(x), max_x)
            min_x = min(min(x), min_x)
        axi[0][id].text(
            0.03,
            0.9,
            "$d=" + str(words//1000)+"K$",
            bbox=dict(boxstyle="square", pad=0.1, fc="w", ec="k", lw=0.1),
            # rotation=90,
            size=6,
            ha="left",
            va="top",
            transform=axi[0][id].transAxes,
        )

    for id, ax in enumerate(axi[0]):
        ax.set_xticks([])
        #   r = df.loc[df["name"] == namesf[id]]
        #   x = np.array([float(x[1:]) for x in r["lossy"]])
        ax.set_xscale("log", base=10)
        #   if len(x) > 1:
        xtics = pu.set_tics_x_log10(ax, min_x, max_x, lim=4)
        ax.set_yscale("log", base=10)
        ax.tick_params(axis="y", labelsize=7, pad = -0.1)
        ax.tick_params(axis="x", labelsize=5, pad = -1.11)
        ytics = pu.set_tics_y_log10(ax, mi * 0.6, mx * 1.4)
        ax.set_xticklabels(["" for x in range(len(xtics))])
        if id == 0:
            ax.set_ylabel("encode", size=5)
            # ax.set_ylabel("Time [s]", size=8)
            ax.yaxis.set_label_coords(-0.3, 0.5)
        else:
            ax.set_yticklabels(["" for x in range(len(ytics))])

    mx = 1
    mi = 1000000000

    # for id, words in enumerate([1000, 3000, 10000, 100000]):
    for id, words in enumerate([1000, 10000, 100000]):
        r = df2.loc[df2["conf"] == "ULAb16"].loc[df2["words"] == words]
        if len(r) > 0:
            x = r.abstracts
            y = r.time
            axi[1][id].plot(x, y, color="tab:blue", alpha=0.6, label="ULA")
            mx = max(max(y), mx)
            mi = min(min(y), mi)
            max_x = max(max(x), max_x)
            min_x = min(min(x), min_x)

        r = df2.loc[df2["conf"] == "tf2"].loc[df2["words"] == words]
        if len(r) > 0:
            x = r.abstracts
            y = r.time
            axi[1][id].plot(x, y, color="tab:pink", alpha=0.6, label="TensorFlow 2.15")
            mx = max(max(y), mx)
            mi = min(min(y), mi)
            max_x = max(max(x), max_x)
            min_x = min(min(x), min_x)

        r = df2.loc[df2["conf"] == "AWAb16"].loc[df2["words"] == words]
        if len(r) > 0:
            x = r.abstracts
            y = r.time
            axi[1][id].plot(x, y, color="tab:brown", alpha=0.6, label="BWARE")
            mx = max(max(y), mx)
            mi = min(min(y), mi)
            max_x = max(max(x), max_x)
            min_x = min(min(x), min_x)

        # if id not in [0]:

    # else:
    # ax.text(
    #         0.06,
    #         0.94,
    #         names[id],
    #         bbox=dict(boxstyle="square", pad=0.1, fc="w", ec="k", lw=0.1),
    #         # rotation=90,
    #         size=6,
    #         ha="left",
    #         va="top",
    #         transform=ax.transAxes,
    #     )

    for ax in axi[1]:
        ax.plot([214748, 214748], [1, 10000], color='green' ,linestyle= 'dotted', linewidth = 0.8, label = ">IntCells")
    for ax in axi[0]:
        ax.plot([214748, 214748], [1, 10000], color='green' ,linestyle= 'dotted', linewidth = 0.8, label = ">IntCells")

    for id, ax in enumerate(axi[1]):
        ax.set_xticks([])
        #   r = df.loc[df["name"] == namesf[id]]
        #   x = np.array([float(x[1:]) for x in r["lossy"]])
        ax.set_xscale("log", base=10)
        #   if len(x) > 1:
        xtics = pu.set_tics_x_log10(ax, min_x, max_x, lim=4)
        ax.set_yscale("log", base=10)
        ax.tick_params(axis="y", labelsize=7, pad = -0.1)
        # ax.tick_params(axis="x", labelsize=5)
        ax.tick_params(axis="x", labelsize=5, pad = -0.1)
        ytics = pu.set_tics_y_log10(ax, mi * 0.6, mx * 1.4)
        if id == 0:
            ax.set_ylabel("+ linear", size=5)
            ax.yaxis.set_label_coords(-0.3, 0.5)
        else:
            ax.set_yticklabels(["" for x in range(len(ytics))])
#    axi[1][0].text(0.0, 0.02, "Number of Abstracts", fontsize=6, 
        # ha="center")
        ax.set_xlabel("Number of Abstracts", fontsize = 5)
        ax.xaxis.set_label_coords(0.5, -0.35)

    axi[0][1].legend(
        ncol=4,
        loc="lower center",
        bbox_to_anchor=(.4, 0.93),
        fontsize=6,
        markerscale=0.6,
        handlelength=1.5,
        columnspacing=1.8,
        handletextpad=0.4,
    )


    plt.subplots_adjust(
        left=0.14, right=0.98, top=0.85, bottom=0.17, wspace=0.17, hspace=0.20
    )

 
    fig.text(
        0.001,
        0.5,
        "Time [s]",
        rotation=90,
        size=8,
        ha="left",
        va="center",
    )
    out = "plotting/plots/wordemb_" + m + ".pdf"
    print("Script:", "plotting/scripts/plot_26_wordemb.py", "out:", out)
    plt.savefig(out)


df = pd.read_csv("plotting/tables/26-wordemb/dams-su1.csv")
df2 = pd.read_csv("plotting/tables/26-wordemb/dams-su1_nn.csv")
plot(df, df2, "su1")
