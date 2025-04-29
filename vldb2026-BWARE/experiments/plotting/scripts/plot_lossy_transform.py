import pandas as pd
import plot_util as pu

import matplotlib.pyplot as plt
import numpy as np


def plot(df, m):
    fig_size = (3.33, 1)
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

    mx = 1000000000
    mi = 1000000000
    bar_labels = ["String", "Detected", "BWARE", "Morph"]

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
        #     np.repeat(r["FMSize"][:1], len(x[1:])),
        #     label="LL",
        #     color=color[0],
        #     linewidth=0.8,
        #     ls="--",
        # )
        ax.plot(x[1:], r["FMSize"][1:], label="Baseline", alpha=0.6, color=color[0])
        # ax.plot(
        #     x[1:],
        #     np.repeat(r["CFMCMCDCompSize"][:1], len(x[1:])),
        #     # label="LL",
        #     color=color[2],
        #     linewidth=0.8,
        #     ls="dotted",
        # )
        ax.plot(
            x[1:], r["CFMCMCDCompSize"][1:], label="AWARE", alpha=0.6, color=color[2]
        )
        # ax.plot(
        #     x[1:],
        #     np.repeat(r["CFCMCDSize"][:1], len(x[1:])),
        #     # label="LL",
        #     color=color[1],
        #     linewidth=0.8,
        #     ls="--",
        # )
        ax.plot(x[1:], r["CFCMCDSize"][1:], label="BWARE", alpha=0.6, color=color[1])


        # ax.plot(
        #     x[1:],
        #     np.repeat(r["CFCMCDCompSize"][:1], len(x[1:])),
        #     # label="LL",
        #     color=color[3],
        #     linewidth=0.8,
        #     ls="--",
        # )
        ax.plot(x[1:], r["CFCMCDCompSize"][1:], label="BWARE+Morph", alpha=0.6, color=color[3])

        # ax.bar(
        #     range(3),
        #     [r.StringSize, r.SchemaSize, r.CompSize],
        #     label=bar_labels,
        #     color=["tab:red", "tab:blue", "tab:orange"],
        #     edgecolor="black",
        #     lw=0.01,
        # )
        mx = max(max(r.FMSize), mx, max(r.CFCMCDSize), max(r.CFMCMCDCompSize))
        mi = min(min(r.FMSize), mi, min(r.CFCMCDSize), min(r.CFMCMCDCompSize))

        # mx = max(max(r.CFCMCDSize), mx)
        # mi = min(min(r.CFCMCDSize), mi)
        # mx = max(max(r.CFMCMCDCompSize), mx)
        # mi = min(min(r.CFMCMCDCompSize), mi)

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
            
            ax.set_xticklabels(["" for x in range(len(xtics))])
        ax.set_yscale("log", base=10)
        ax.tick_params(axis="y", labelsize=7)
        ytics = pu.set_tics_y_log10(ax, mi * 0.6, mx * 1.4)
        if id == 0:
            ax.set_ylabel("Memory [B]", size=8)
            ax.yaxis.set_label_coords(-1.1, 0.5)
        else:
            ax.set_yticklabels(["" for x in range(len(ytics))])

    axi[7].legend(
        ncol=6,
        loc="upper center",
        bbox_to_anchor=(-4.0, 1.3),
        fontsize=7,
        markerscale=0.6,
        handlelength=1.5,
        columnspacing=0.8,
        handletextpad=0.1,
    )

    plt.subplots_adjust(
        left=0.135, right=0.99, top=0.8, bottom=0.05, wspace=0.17, hspace=0.30
    )

    plt.savefig("plotting/plots/lossy_transform_" + m + ".pdf")


df = pd.read_csv("plotting/tables/te/XPS-15-7590_lossy.csv")
plot(df, "XPS-15-7590")
df = pd.read_csv("plotting/tables/te/dams-su1_lossy.csv")
plot(df, "su1")
