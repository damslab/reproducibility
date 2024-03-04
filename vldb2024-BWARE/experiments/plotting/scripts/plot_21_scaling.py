import pandas as pd
import plot_util as pu

import matplotlib.pyplot as plt
import numpy as np


def parseFloat(x):
    sr = x.split("day_0")[1].split(".tsv")[0].replace("_", "")
    if len(sr) > 1:
        return float(sr)
    else:
        return float(195841983)
    

def plot(df, m):
    fig_size = (3.33, 0.8)
    names = [
        "Criteo"
    ]
        # "KDD",
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
    bar_labels = ["ULA", "BWARE"]

    namesf = [
        # "adult",
        # "cat",
        # "criteo",
        "criteo",
        # "kdd",
        # "salaries",
        # "santander",
        # "home",
    ]

    color = ["tab:blue", "tab:brown"]
    if True:
    # for id, ax in enumerate(axi):
        id = 0
        ax = axi
        dfc = df.loc[df["name"] == namesf[id]]
        r = dfc.loc[dfc.lossy == "full"].loc[dfc.FileType == "bin"]
        x = np.array(
            [float(x.split("day_0")[1].split(".tsv")[0].replace("_", "")) for x in r["FullName"]]
        )


        # ax.plot(
        #     x,
        #     np.repeat(r.Time, len(x)),
        #     label="ULA",
        #     alpha=0.6,
        #     color=color[0],
        #     ls="--",
        # )
        ax.plot(x, r.Time, label="ULA", alpha=0.6, color=color[0])

        if r.Time.any():
              mi = min(min(r.Time), mi)
              mx = max(max(r.Time), mx)

        r = dfc.loc[dfc.lossy == "l10"].loc[dfc.FileType == "bin"]
        while(len(r) > len(x)):
            x = list(x)
            v = x[-1] * 10
            if v < 195841983:
                
                x.append(x[-1] * 10)
            else :
                x.append(195841983)
            # list(x).append(195841983)
            # x = np.array(
            #     [float(x.split("day_0")[1].split(".tsv")[0].replace("_", "")) for x in r["FullName"]]
            # )
        ax.plot(x[:len(r.Time)], r.Time, label="ULA-50Δ", alpha=0.6, color=color[0], ls="--")

        if r.Time.any():
              mi = min(min(r.Time), mi)
              mx = max(max(r.Time), mx)

        r = dfc.loc[dfc.lossy == "full"].loc[dfc.FileType == "cla"]
        if(len(r) > len(x)):
            x = np.array(
                [parseFloat(x) for x in r["FullName"]]
            )
        ax.plot(x[:len(r.Time)], r.Time, label="BWARE", alpha=0.6, color=color[1])

        if r.Time.any():
              mi = min(min(r.Time), mi)
              mx = max(max(r.Time), mx)

        r = dfc.loc[dfc.lossy == "l10"].loc[dfc.FileType == "cla"]
        if(len(r) > len(x)):
            x = np.array(
                [parseFloat(x) for x in r["FullName"]]
            )
        ax.plot(x[:len(r.Time)], r.Time, label="BWARE-50Δ", alpha=0.6, color=color[1], ls="--")

        if r.Time.any():
              mi = min(min(r.Time), mi)
              mx = max(max(r.Time), mx)


        #   r = df.loc[df["name"] == namesf[id]]
        #   r = r.loc[df["lossy"] == "cla"].loc[r.Conf == "TAWAb16"]
        #   x = np.array([float(x[1:]) for x in r["FileType"][1:]]) * 5

        #   ax.plot(
        #       x,
        #       np.repeat(r.Time[:1], len(x)),
        #       label="BWARE",
        #       alpha=0.6,
        #       color=color[1],
        #       ls="--",
        #   )
        #   ax.plot(x, r.Time[1:], label="Lossy-BWARE", alpha=0.6, color=color[1])

        #   if r.Time.any():
        #       mi = min(min(r.Time), mi)
        #       mx = max(max(r.Time), mx)

        # ula = r.loc[df.Conf == "ULAb16"].loc[df.FileType == "bin"]
        # awa = r.loc[df.Conf == "TAWAb16"].loc[df.FileType == "cla"]

        # ax.bar(
        #     [0],
        #     ula.Time,
        #     color="tab:blue",
        # )
        # if ula.Time.any():
        #     mi = min(min(ula.Time), mi)
        #     mx = max(max(ula.Time), mx)
        # ax.bar(
        #     [1],
        #     awa.Time,
        #     color="tab:orange",
        # )

        ax.grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)
        ax.grid(True, "minor", axis="both", ls="dotted", linewidth=0.2, alpha=0.9)

        ax.text(
            0.06,
            0.925,
            names[id],
            bbox=dict(boxstyle="square", pad=0.1, fc="w", ec="k", lw=0.1),
            # rotation=90,
            size=6,
            ha="left",
            va="top",
            transform=ax.transAxes,
        )

    # for id, ax in enumerate(axi):
        ax.set_xticks([])
        r = df.loc[df["name"] == namesf[id]]

        ax.set_xscale("log", base=10)
        if len(x) > 1:
            xtics = pu.set_tics_x_log10(ax, min(x) * 0.9, max(x) * 1.1, lim=20)
        ax.tick_params(axis="y", labelsize=7)
        ax.tick_params(axis="x", labelsize=5)
        ax.set_yscale("log", base=10)
        ytics = pu.set_tics_y_log10(ax, mi*0.7, mx * 1.4, 20)
        # ax.set_yscale("log", base=10)
        # ytics = pu.set_tics_y(ax, 0, mx * 1.1)
        if id == 0:
            ax.set_ylabel("Time [s]", size=8)
        else:
            ax.set_yticklabels(["" for x in range(len(ytics))])

    # axi[1].legend(
    axi.legend(
        ncol=6,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.65),
        fontsize=7,
        markerscale=0.6,
        handlelength=1.5,
        columnspacing=0.8,
        handletextpad=0.1,
    )
    fig.text(0.76,0.,"# Rows", fontsize=8)

    plt.subplots_adjust(
        left=0.133, right=0.997, top=0.71, bottom=0.2, wspace=0.07, hspace=0.30
    )
    out = "plotting/plots/lm_scaling_" + m + "_time.pdf"

    print("Script", "/plotting/scripts/plot_21_scaling.py", "out:", out)
    plt.savefig(out)


df = pd.read_csv("plotting/tables/21-scaling/dams-su1.csv")
plot(df, "su1")
