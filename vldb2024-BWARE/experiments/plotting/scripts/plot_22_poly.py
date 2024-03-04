import pandas as pd
import plot_util as pu

import matplotlib.pyplot as plt
import numpy as np


def plot(df, m):
    fig_size = (3.33, 0.8)
    names = [
        "Adult",
        "Crypto",
        "KDD",
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
        "crypto",
        "kdd",
        "santander",
        "home",
    ]

    color = ["tab:blue", "tab:orange", "tab:green", "tab:brown"]

    for id, ax in enumerate(axi):
        r = df.loc[df["name"] == namesf[id]]
        ula = (
            r.loc[df.Conf == "ULAb16"].loc[df.FileType == "bin"].loc[df.lossy == "full"]
        )
        awa = (
            r.loc[df.Conf == "TAWAb16"]
            .loc[df.FileType == "cla"]
            .loc[df.lossy == "full"]
        )

        ulaL = (
            r.loc[df.Conf == "ULAb16"].loc[df.FileType == "bin"].loc[df.lossy == "l10"]
        )
        awaL = (
            r.loc[df.Conf == "TAWAb16"].loc[df.FileType == "cla"].loc[df.lossy == "l10"]
        )

        ax.plot(ula.PolyDegree, ula.Time, color="tab:blue", alpha=0.6,label="ULA")

        if ula.Time.any():
            mi = min(min(ula.Time), mi)
            mx = max(max(ula.Time), mx)
        ax.plot(awa.PolyDegree, awa.Time, color="tab:brown", alpha=0.6,label="BWARE")

        if awa.Time.any():
            mi = min(min(awa.Time), mi)
            mx = max(max(awa.Time), mx)

        ax.plot(ulaL.PolyDegree, ulaL.Time, color="tab:blue", alpha=0.6,label="ULA-50Δ", ls="--")

        # if ulaL.Time.any():
        #     mi = min(min(ulaL.Time), mi)
        #     mx = max(max(ulaL.Time), mx)
        ax.plot(awaL.PolyDegree, awaL.Time, color="tab:brown", alpha=0.6,label="BWARE-50Δ", ls="--")

        if awaL.Time.any():
            mi = min(min(awaL.Time), mi)
            mx = max(max(awaL.Time), mx)

        ax.grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)
        ax.grid(True, "minor", axis="y", ls="dotted", linewidth=0.2, alpha=0.9)

        if id not in [0]:
            ax.text(
                0.94,
                0.05,
                names[id],
                bbox=dict(boxstyle="square", pad=0.1, fc="w", ec="k", lw=0.1),
                # rotation=90,
                size=6,
                ha="right",
                va="bottom",
                transform=ax.transAxes,
            )
        else:
            ax.text(
                0.06,
                0.94,
                names[id],
                bbox=dict(boxstyle="square", pad=0.1, fc="w", ec="k", lw=0.1),
                # rotation=90,
                size=6,
                ha="left",
                va="top",
                transform=ax.transAxes,
            )

    for id, ax in enumerate(axi):
        ax.set_xticks([])
        #   r = df.loc[df["name"] == namesf[id]]
        #   x = np.array([float(x[1:]) for x in r["lossy"]])
        #   ax.set_xscale("log", base=10)
        #   if len(x) > 1:
        xtics = pu.set_tics_x(ax, 1, 9, lim=4, include0=True)
        ax.set_yscale("log", base=10)
        ax.tick_params(axis="y", labelsize=7)
        ax.tick_params(axis="x", labelsize=5)
        ytics = pu.set_tics_y_log10(ax, mi * 0.6, mx * 1.4)
        if id == 0:
            ax.set_ylabel("Time [s]", size=8)
        else:
            ax.set_yticklabels(["" for x in range(len(ytics))])

    axi[4].legend(
        ncol=6,
        loc="upper center",
        bbox_to_anchor=(-2.0, 1.65),
        fontsize=7,
        markerscale=0.6,
        handlelength=1.5,
        columnspacing=0.8,
        handletextpad=0.1,
    )
    # fig.text(0.08, 0.04, "poly→", fontsize=8)

    plt.subplots_adjust(
        left=0.133, right=0.994, top=0.71, bottom=0.2, wspace=0.11, hspace=0.33
    )
    out = "plotting/plots/lm_poly_" + m + "_time.pdf"
    print("Script:", "plotting/scripts/plot_22_poly.py", "out:", out)
    plt.savefig(out)


df = pd.read_csv("plotting/tables/22-poly/dams-su1.csv")
plot(df, "su1")
# df = pd.read_csv("plotting/tables/te/dams-su1_lossy.csv")
# plot(df, "su1")
