import pandas as pd
import plot_util as pu

import matplotlib.pyplot as plt
import numpy as np


def plot(df, m):
    fig_size = (3.33, 0.8)
    names = [
        None,
        "Cat",
        None,
        None,
        "KDD",
        "Sal",
        None,
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

    color = ["tab:blue", "tab:orange", "tab:green", "tab:brown"]

    for id, ax in enumerate(axi):
        r = df.loc[df["name"] == namesf[id]]
        x = np.array([float(x[1:]) for x in r["lossy"]]) * 5



        if len(r) == 0:
            continue
        # ax.plot(
        #     x[1:],
        #     np.repeat(r["FMTE"][:1], len(x[1:])),
        #     color=color[0],
        #     linewidth=0.8,
        #     ls="--",
        #     label="Lossless",
        # )
        ax.plot(x[1:], r["FMTE"][1:], label="Baseline", alpha=0.6, color=color[0])
       
        # ax.plot(
        #     x[1:],
        #     np.repeat(r["CFMCMCDTE"][:1] + r["CFMCMCDCompTime"][:1], len(x[1:])),
        #     color=color[2],
        #     linewidth=0.8,
        #     ls="dotted",
        #     label="Lossless",
        # )
        ax.plot(
            x[1:],
            r["CFMCMCDTE"][1:] + +r["CFMCMCDCompTime"][1:],
            label="AWARE",
            alpha=0.6,
            color=color[2],
        )

        # ax.plot(
        #     x[1:],
        #     np.repeat(r["CFCMCDTE"][:1] , len(x[1:])),
        #     color=color[1],
        #     linewidth=0.8,
        #     ls="--",
        #     label="Lossless",
        # )
        ax.plot(
            x[1:],
            r["CFCMCDTE"][1:] ,
            label="BWARE",
            alpha=0.6,
            color=color[1],
        )

        # ax.plot(
        #     x[1:],
        #     np.repeat(r["CFCMCDTE"][:1] + r["CFCMCDCompTime"][:1], len(x[1:])),
        #     color=color[3],
        #     linewidth=0.8,
        #     ls="--",
        #     label="Lossless",
        # )
        ax.plot(
            x[1:],
            r["CFCMCDTE"][1:] + r["CFCMCDCompTime"][1:],
            label="+BWARE+Morph",
            alpha=0.6,
            color=color[3],
        )


        mx = max(
            max(r.FMTE),
            mx,
            max(r.CFCMCDTE),
            max(r.CFMCMCDTE + r.CFMCMCDCompTime),
        )
        mi = min(
            min(r.FMTE),
            mi,
            min(r.CFCMCDTE ),
            min(r.CFMCMCDTE + r.CFMCMCDCompTime),
        )

        ax.grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)
        ax.grid(True, "minor", axis="y", ls="dotted", linewidth=0.2, alpha=0.9)

        if id in [0, 5]:
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

        elif id in [1, 6]:
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
        r = df.loc[df["name"] == namesf[id]]
        x = np.array([float(x[1:]) for x in r["lossy"]]) * 5
        ax.set_xscale("log", base=10)
        if len(x) > 1:
            if id == 5:
                xtics = pu.set_tics_x_log10(ax, min(x[1:]) * 0.7, max(x[1:]) * 2.0, lim=2)
            else:
                xtics = pu.set_tics_x_log10(ax, min(x[1:]) * 0.7, max(x[1:]) * 1.3, lim=2)
            
        ax.set_yscale("log", base=10)
        ax.tick_params(axis="y", labelsize=7)
        ax.tick_params(axis="x", labelsize=5)
        # if id == 5:
        #     ytics = pu.set_tics_y_log10(ax, mi * 0.6, mx * 1.4, 0)
        # else:
        ytics = pu.set_tics_y_log10(ax, mi * 0.6, mx * 1.4)
        if id == 0:
            ax.set_ylabel("Time [s]", size=8)
            ax.yaxis.set_label_coords(-1.1, 0.5)
        else:
            ax.set_yticklabels(["" for x in range(len(ytics))])


    fig.text(0.1,0,"Δ→")
    # axi[7].legend(
    #     ncol=6,
    #     loc="upper center",
    #     bbox_to_anchor=(-4.0, 1.3),
    #     fontsize=7,
    #     markerscale=0.6,
    #     handlelength=1.5,
    #     columnspacing=0.8,
    #     handletextpad=0.1,
    # )

    plt.subplots_adjust(
        left=0.135, right=0.99, top=0.98, bottom=0.2, wspace=0.17, hspace=0.30
    )

    plt.savefig("plotting/plots/lossy_transform_" + m + "_time.pdf")


df = pd.read_csv("plotting/tables/te/XPS-15-7590_lossy.csv")
plot(df, "XPS-15-7590")
df = pd.read_csv("plotting/tables/te/dams-su1_lossy.csv")
plot(df, "su1")
