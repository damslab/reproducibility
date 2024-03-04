import pandas as pd
import plot_util as pu

import matplotlib.pyplot as plt
import numpy as np


def plot(df, m):
    fig_size = (3.33, 0.6)
    #  names = [
    #      "L2SVM",
    #      "PCA",
    #      #   "KDD",
    #      #   "San",
    #      #   "Home",
    #  ]
    fig, axi = plt.subplots(
        1,
        3,
        num=None,
        figsize=fig_size,
        dpi=pu.dpi,
        facecolor="w",
        edgecolor="k",
    )

    mx = 1
    mi = 1000000000
    bar_labels = ["String", "Detected", "BWARE"]

    color = ["tab:blue", "tab:orange", "tab:green", "tab:brown"]

    #  for id, ax in enumerate(axi):
    r = df.loc[df["name"] == "santander"].loc[df["Algorithm"] == "L2SVM_first"]

    mi = min(min(r.Time), mi)
    mx = max(max(r.Time), mx)
    axi[0].bar([0], r.loc[df.Conf == "ULAb16"].loc[df.lossy == "full"].Time)
    axi[0].bar(
        [1], r.loc[df.Conf == "TAWAb16"].loc[df.lossy == "full"].Time, color="tab:brown"
    )

    axi[0].grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)
    axi[0].grid(True, "minor", axis="y", ls="dotted", linewidth=0.2, alpha=0.9)
    axi[0].text(
        0.5,
        1.1,
        "Sant L2SVM",
        bbox=dict(boxstyle="square", pad=0.1, fc="w", ec="k", lw=0.1),
        # rotation=90,
        size=6,
        ha="center",
        va="top",
        transform=axi[0].transAxes,
    )

    r = (
        df.loc[df["name"] == "criteo"]
        .loc[df["Algorithm"] == "pca_first"]
        .loc[df.lossy == "l10"]
    )
    mi = min(min(r.Time), mi)
    mx = max(max(r.Time), mx)
    axi[1].bar([0], r.loc[df.Conf == "ULAb16"].Time,label="ULA")
    axi[1].bar([1], r.loc[df.Conf == "TAWAb16"].Time, color="tab:brown",label="BWARE+Morph")

    axi[1].grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)
    axi[1].grid(True, "minor", axis="y", ls="dotted", linewidth=0.2, alpha=0.9)
    axi[1].text(
        0.5,
        1.1,
        "Criteo 50Δ PCA",
        bbox=dict(boxstyle="square", pad=0.1, fc="w", ec="k", lw=0.1),
        # rotation=90,
        size=6,
        ha="center",
        va="top",
        transform=axi[1].transAxes,
    )
    r = (
        df.loc[df["name"] == "home"]
        .loc[df["Algorithm"] == "kmeans_first"]
        .loc[df.lossy == "l10"]
    )
    mi = min(min(r.Time), mi)
    mx = max(max(r.Time), mx)
    axi[2].bar([0], r.loc[df.Conf == "ULAb16"].Time, label="ULA")
    axi[2].bar([1], r.loc[df.Conf == "TAWAb16"].Time, color="tab:brown", label="BWARE+Morph")

    axi[2].grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)
    axi[2].grid(True, "minor", axis="y", ls="dotted", linewidth=0.2, alpha=0.9)
    axi[2].text(
        0.5,
        1.1,
        "Home 50Δ K-Means",
        bbox=dict(boxstyle="square", pad=0.1, fc="w", ec="k", lw=0.1),
        # rotation=90,
        size=6,
        ha="center",
        va="top",
        transform=axi[2].transAxes,
    )
    #   if id not in [0]:
    #       ax.text(
    #           0.94,
    #           0.05,
    #           names[id],
    #           bbox=dict(boxstyle="square", pad=0.1, fc="w", ec="k", lw=0.1),
    #           # rotation=90,
    #           size=6,
    #           ha="right",
    #           va="bottom",
    #           transform=ax.transAxes,
    #       )
    #   else:
    #       ax.text(
    #           0.06,
    #           0.94,
    #           names[id],
    #           bbox=dict(boxstyle="square", pad=0.1, fc="w", ec="k", lw=0.1),
    #           # rotation=90,
    #           size=6,
    #           ha="left",
    #           va="top",
    #           transform=ax.transAxes,
    #       )

    for id, ax in enumerate(axi):
        ax.set_xticks([])
        #   r = df.loc[df["name"] == namesf[id]]
        #   x = np.array([float(x[1:]) for x in r["lossy"]])
        #   ax.set_xscale("log", base=10)
        #   if len(x) > 1:
        #   xtics = pu.set_tics_x(ax, 1, 9, lim=4, include0=True)
        ax.set_yscale("log", base=10)
        ax.tick_params(axis="y", labelsize=7)
        ax.tick_params(axis="x", labelsize=5)
        ytics = pu.set_tics_y_log10(ax, mi * 0.6, mx * 1.4)
        if id == 0:
            ax.set_ylabel("Time [s]", size=8)
            ax.yaxis.set_label_coords(x=-0.35, y=.6)
        else:
            ax.set_yticklabels(["" for x in range(len(ytics))])

    axi[1].legend(
         ncol=6,
         loc="lower center",
         bbox_to_anchor=(0.5, 1),
         fontsize=7,
         markerscale=0.6,
         handlelength=1.5,
         columnspacing=0.8,
         handletextpad=0.1,
     )
    #  fig.text(0.08, 0.04, "poly→", fontsize=8)

    plt.subplots_adjust(
        left=0.13, right=0.995, top=0.61, bottom=0.1, wspace=0.17, hspace=0.30
    )
    out = "plotting/plots/e2e_algorithms_" + m + "_time.pdf"
    print("Script:", "plotting/scripts/plot_23_algorithms.py", "out:", out)
    plt.savefig(out)


df = pd.read_csv("plotting/tables/23-algorithm/dams-su1.csv")
plot(df, "su1")
# df = pd.read_csv("plotting/tables/te/dams-su1_lossy.csv")
# plot(df, "su1")
