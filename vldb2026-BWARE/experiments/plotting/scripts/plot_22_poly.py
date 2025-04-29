import pandas as pd
import plot_util as pu
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def plot(df, m):
    fig_size = (2.16, 0.8)
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
        ytics = pu.set_tics_y_log10(ax, mi * 0.6, mx * 2)
        if id == 0:
            ax.set_ylabel("Time [s]", size=8)
            ax.yaxis.set_label_coords(-0.62, 0.5)
        else:
            ax.set_yticklabels(["" for x in range(len(ytics))])
        ax.tick_params(axis="x", pad=-0.04)
        if id == 2:
            ax.set_xlabel("Number of Polynomials Added", fontsize = 5)
            ax.xaxis.set_label_coords(0.5, -0.25)
    axi[0].tick_params(axis="y", pad=-0.8)

    handles, labels = axi[4].get_legend_handles_labels()
    hd = mpl.lines.Line2D([0],[0],alpha=0.6, color="black", ls="--")
    hd.set_color("black")

    handles = (handles[0], handles[1], hd)
    labels = (labels[0], labels[1], "50Δ")

    plt.legend(handles,labels,
        ncol=6,
        loc="upper center",
        bbox_to_anchor=(-2.0, 1.5),
        fontsize=6,
        markerscale=1.0,
        handlelength=1.8,
        columnspacing=0.8,
        handletextpad=0.1,
    )
    # axi[4].legend(
    #     ncol=6,
    #     loc="upper center",
    #     bbox_to_anchor=(-2.0, 1.65),
    #     fontsize=7,
    #     markerscale=0.6,
    #     handlelength=1.5,
    #     columnspacing=0.8,
    #     handletextpad=0.1,
    # )
    # fig.text(0.08, 0.04, "poly→", fontsize=8)

    plt.subplots_adjust(
        left=0.142, right=0.99, top=0.77, bottom=0.225, wspace=0.15, hspace=0.33
    )
    out = "plotting/plots/lm_poly_" + m + "_time.pdf"
    print("Script:", "plotting/scripts/plot_22_poly.py", "out:", out)
    plt.savefig(out)


df = pd.read_csv("plotting/tables/22-poly/dams-su1.csv")
plot(df, "su1")
# df = pd.read_csv("plotting/tables/te/dams-su1_lossy.csv")
# plot(df, "su1")
