import pandas as pd
import plot_util as pu

import matplotlib.pyplot as plt
import numpy as np


def plot(df, m):
    fig_size = (3.33, 1.)
    names = [
        "E2E",
        "TE",
    ]
    fig, axi = plt.subplots(
        1,
        3,
        num=None,
        figsize=fig_size,
        dpi=pu.dpi,
        facecolor="w",
        edgecolor="k",
    )

    bar_labels = ["String", "Detected", "BWARE"]
    mx = 1
    mi = 1000000000
    namesf = [
        "Time",
        "TE",
    ]

    color = ["tab:blue", "tab:orange", "tab:green", "tab:brown"]
    words = [10000, 100000, 999995]

    for id, ax in enumerate(axi):
        ax.grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)
        ax.grid(True, "minor", axis="y", ls="dotted", linewidth=0.2, alpha=0.9)

    r = df.loc[df["conf"] == "ULAb16"].loc[ df["words" ] == 10000]
    x = r.abstracts
    y = r.time 
    axi[0].plot(x,y, color="tab:blue", alpha=0.6,label="ULA")
    mx = max(max(y), mx)
    mi = min(min(y), mi)

    r = df.loc[df["conf"] == "tf"].loc[ df["words" ] == 10000]
    x = r.abstracts
    y = r.time 
    axi[0].plot(x,y, color="tab:pink", alpha=0.6,label="TensorFlow 2.15")
    mx = max(max(y), mx)
    mi = min(min(y), mi)

    r = df.loc[df["conf"] == "torch"].loc[ df["words" ] == 10000]
    x = r.abstracts
    y = r.time 
    axi[0].plot(x,y, color="tab:gray", alpha=0.6,label="PyTorch 2.2")
    mx = max(max(y), mx)
    mi = min(min(y), mi)

    r = df.loc[df["conf"] == "AWAb16"].loc[ df["words" ] == 10000]
    x = r.abstracts
    y = r.time 
    axi[0].plot(x,y, color="tab:brown", alpha=0.6,label="BWARE")
    mx = max(max(y), mx)
    mi = min(min(y), mi)

    r = df.loc[df["conf"] == "ULAb16"].loc[ df["words" ] == 10000]
    x = r.abstracts
    y = r.tableExpand + r.reshape + r["multiply"]
    axi[1].plot(x,y, color="tab:blue", alpha=0.6,label="ULA")
    mx = max(max(y), mx)
    mi = min(min(y), mi)

    r = df.loc[df["conf"] == "tf"].loc[ df["words" ] == 10000]
    x = r.abstracts
    y = r.tfEncode 
    axi[1].plot(x,y, color="tab:pink", alpha=0.6,label="TensorFlow 2.15")
    mx = max(max(y), mx)
    mi = min(min(y), mi)

    r = df.loc[df["conf"] == "torch"].loc[ df["words" ] == 10000]
    x = r.abstracts
    y = r.tfEncode 
    axi[1].plot(x,y, color="tab:gray", alpha=0.6,label="PyTorch 2.2")
    mx = max(max(y), mx)
    mi = min(min(y), mi)


    r = df.loc[df["conf"] == "AWAb16"].loc[ df["words" ] == 10000]
    x = r.abstracts
    y = r.tableExpand + r.reshape + r["multiply"]
    axi[1].plot(x,y, color="tab:brown", alpha=0.6,label="BWARE")
    mx = max(max(y), mx)
    mi = min(min(y), mi)


        # if id not in [0]:
        #     ax.text(
        #         0.94,
        #         0.05,
        #         names[id],
        #         bbox=dict(boxstyle="square", pad=0.1, fc="w", ec="k", lw=0.1),
        #         # rotation=90,
        #         size=6,
        #         ha="right",
        #         va="bottom",
        #         transform=ax.transAxes,
        #     )
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

    for id, ax in enumerate(axi):
        ax.set_xticks([])
        #   r = df.loc[df["name"] == namesf[id]]
        #   x = np.array([float(x[1:]) for x in r["lossy"]])
        ax.set_xscale("log", base=10)
        #   if len(x) > 1:
        xtics = pu.set_tics_x_log10(ax, min(x), max(x), lim=4)
        ax.set_yscale("log", base=10)
        ax.tick_params(axis="y", labelsize=7)
        ax.tick_params(axis="x", labelsize=5)
        ytics = pu.set_tics_y_log10(ax, mi * 0.6, mx * 1.4)
        if id == 0:
            ax.set_ylabel("Time [s]", size=8)
            ax.yaxis.set_label_coords(-0.3, 0.9)
        else:
            ax.set_yticklabels(["" for x in range(len(ytics))])

    axi[1].legend(
        ncol=3,
        loc="lower center",
        bbox_to_anchor=(-.1, .93),
        fontsize=7,
        markerscale=0.6,
        handlelength=1.5,
        columnspacing=1.8,
        handletextpad=0.4,
    )
    fig.text(0.003, 0.1, "#abstracts→", fontsize=8)

    plt.subplots_adjust(
        left=0.17, right=0.97, top=0.65, bottom=0.19, wspace=0.17, hspace=0.30
    )
    out = "plotting/plots/wordemb_random_" + m + ".pdf"
    print("Script:", "plotting/scripts/plot_27_wordemb_random.py", "out:", out)
    plt.savefig(out)


df = pd.read_csv("plotting/tables/27-wordemb-random/dams-su1.csv")
plot(df, "su1")
