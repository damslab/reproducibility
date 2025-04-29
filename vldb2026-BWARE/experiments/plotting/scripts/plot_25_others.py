import pandas as pd
import plot_util as pu
import math
import matplotlib.pyplot as plt
import numpy as np
mx = 1
mi = 1000000000


def plot(df, m):
    fig_size = (3.3, 1.)
    names = [
        "E2E",
        "TE",
        "TaskClock"
    ]
    
    fig, axi = plt.subplots(
        1,
        2,
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
        "TaskClock"
    ]

    color = ["tab:blue", "tab:orange", "tab:green", "tab:brown"]

    for id, ax in enumerate(axi):


        r = df.loc[df["alg"] =="pl"].dropna()
        x = r.name
        if namesf[id] == "TE":
            y = r[namesf[id]] - r["ReadTime"]
        else:
            y = r[namesf[id]]
        ax.plot(x,y, color="tab:gray", alpha=0.6,label="Polars 0.20")
        if(id < 2):
            mx = max(max(y), mx)
            mi = min(min(y), mi)

        r = df.loc[df["alg"] =="pd"].dropna()
        x = r.name
        if namesf[id] == "TE":
            y = r[namesf[id]] - r["ReadTime"]
        else:
            y = r[namesf[id]]
        ax.plot(x,y, color="tab:red", alpha=0.6,label="Pandas 2.1")
        if(id < 2):
            mx = max(max(y), mx)
            mi = min(min(y), mi)

        r = df.loc[df["alg"] =="sk"].dropna()
        x = r.name
        if namesf[id] == "TE":
            y = r[namesf[id]] - r["ReadTime"]
        else:
            y = r[namesf[id]]
        ax.plot(x,y, color="tab:olive", alpha=0.6,label="SKLearn 1.4.1")
        if(id < 2):
            mx = max(max(y), mx)
            mi = min(min(y), mi)

        r = df.loc[df["alg"] =="tf"].dropna()
        x = r.name
        if namesf[id] == "TE":
            y = r[namesf[id]] - r["ReadTime"]
        else:
            y = r[namesf[id]]
        ax.plot(x,y, color="tab:pink", alpha=0.6,label="TensorFlow 2.15")
        if(id < 2):
            mx = max(max(y), mx)
            mi = min(min(y), mi)


        r = df.loc[df["alg"] =="defULAb16"].dropna()
        x = r.name
        y = r[namesf[id]]
        r2 = df.loc[df["alg"] =="traULAb16"].dropna()
        if namesf[id] == "TE":
            y2 = r2[namesf[id]] - r2["ReadTime"]
        else:
            y2 = r2[namesf[id]]
        x = r2.name
        y = [min(a,b) for a,b in zip(y,y2)]
        x = x[:len(y)]
        ax.plot(x,y, color="tab:blue", alpha=0.6,label="ULA")
        if(id < 2):
            mx = max(max(y), mx)
            mi = min(min(y), mi)

        r = df.loc[df["alg"] =="traTAWAb16cla"].dropna()
        x = r.name
        if namesf[id] == "TE":
            y = r[namesf[id]] - r["ReadTime"]
        else:
            y = r[namesf[id]]

        ax.plot(x,y, color="tab:brown", alpha=0.6,label="BWARE", ls="dotted")
        if len(x) > 1 and (id < 2):
            mx = max(max(y), mx)
            mi = min(min(y), mi)     


        r = df.loc[df["alg"] =="traTAWAb16"].dropna()
        x = r.name
        if namesf[id] == "TE":
            y = r[namesf[id]] - r["ReadTime"]
        else:
            y = r[namesf[id]]

        r2 = df.loc[df["alg"] =="defTAWAb16"].dropna()
        x = r2.name
        
        y2 = r2[namesf[id]]
        y = [min(a,b) for a,b in zip(y,y2)]
        x = x[:len(y)]
        ax.plot(x,y, color="tab:brown", alpha=0.6,label="BWARE CSV", ls="--")
        # if np.isnan(y).any():
        if(id < 2):
            mx = max(max(y), mx)
            mi = min(min(y), mi)


        # r = df.loc[df["alg"] =="defTAWAb16"]
        # x = r.name
        # y = r[namesf[id]]
        # ax.plot(x,y, color="tab:brown", alpha=0.6,label="BWARE", ls="--")
        # mx = max(max(y), mx)
        # mi = min(min(y), mi)



        ax.grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)
        ax.grid(True, "minor", axis="y", ls="dotted", linewidth=0.2, alpha=0.9)

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

    for id, ax in enumerate(axi[:2]):
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
            ax.yaxis.set_label_coords(-0.25, 0.5)
        else:
            ax.set_yticklabels(["" for x in range(len(ytics))])
        ax.tick_params(axis="x", pad=-0.06)

        # ax.xaxis("#Rows→", fontsize=6)

        ax.set_xlabel("Number of Rows", fontsize = 5)
        ax.xaxis.set_label_coords(0.5, -0.25)
    axi[0].tick_params(axis="y", pad=-0.06)
    # for id, ax in enumerate(axi[2:]):
    #     ax.set_xticks([])
    #     #   r = df.loc[df["name"] == namesf[id]]
    #     #   x = np.array([float(x[1:]) for x in r["lossy"]])
    #     ax.set_xscale("log", base=10)
    #     #   if len(x) > 1:
    #     xtics = pu.set_tics_x_log10(ax, min(x), max(x), lim=4)
    #     ax.set_yscale("log", base=10)
    #     ax.tick_params(axis="y", labelsize=7)
    #     ax.tick_params(axis="x", labelsize=5)
    #     ytics = pu.set_tics_y_log10(ax, min(y) * 0.1, max(y) * 1.4)
    #     # if id == 0:
    #     ax.set_ylabel("Cycles", size=8)
    #     ax.yaxis.set_label_coords(-0.3, 0.5)
    #     # else:
    #         # ax.set_yticklabels(["" for x in range(len(ytics))])

    # axi[1].legend(
    #     ncol=3,
    #     loc="lower center",
    #     bbox_to_anchor=(-.1, .93),
    #     fontsize=5,
    #     markerscale=0.6,
    #     handlelength=1.5,
    #     columnspacing=1.8,
    #     handletextpad=0.4,
    # )

    handles, labels = axi[0].get_legend_handles_labels()
    # print(labels)
    handles = (
        handles[:5] +[plt.plot([], marker="", ls="")[0]]+ [handles[6]] + [handles[5]]
    )
    labels = (
        labels[:5] + [""]+ [labels[6]] + [labels[5]]
    )

    plt.legend(handles,labels,
        loc="lower center",
        bbox_to_anchor=(-0.25, 1),
               fontsize=6.3,
        markerscale=0.6,
        ncol = 4,
        handlelength=1.5,
        columnspacing=0.8,
        handletextpad=0.1,
        frameon= True
        )
    
    # fig.text(0.003, 0., "#Rows→", fontsize=6)

    plt.subplots_adjust(
        left=0.13, right=0.98, top=0.65, bottom=0.188, wspace=0.17, hspace=0.30
    )
    out = "plotting/plots/others_" + m + ".pdf"
    print("Script:", "plotting/scripts/plot_25_others.py", "out:", out)
    plt.savefig(out)


df = pd.read_csv("plotting/tables/25-others/dams-su1.csv")
plot(df, "su1")
