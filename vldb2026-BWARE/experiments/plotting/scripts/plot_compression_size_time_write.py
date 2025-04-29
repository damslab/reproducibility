import pandas as pd
import plot_util as pu

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

import numpy as np


def plot(df, m):
    fig_size = (3.3, 0.6)
    fig, axi = plt.subplots(
        1,
        df.shape[0],
        num=None,
        figsize=fig_size,
        dpi=pu.dpi * 20,
        facecolor="w",
        edgecolor="k",
    )

    mx = 30
    mi = 100000000
    # bar_labels = [None, None, "Snappy", "ZStd", None, "BWARE-Snappy", "BWARE-ZStd"]

    names = [
        "Adult",
        "Cat",
        "Crit10M",
        "Crypto",
        "KDD",
        "Sal",
        "San",
        None,
    ]
    for id, ax in enumerate(axi):
        r = df.loc[id]

        # uncompressedRead = r.DetectSchemaTime - r.DetectSchemaSysDSTime
        # uncompressedRead = uncompressedRead + r.DetectSchemaCompile + r.DetectSchemaRead

        # for ii in range(7):

        data = [
            r.DetectSchemaExec - r.DetectSchemaRead,
            r.OrgSnappyExec - r.OrgSnappyRead,
            r.OrgZstdExec - r.OrgZstdRead,
            r.CompExec - r.CompRead,
            r.CompSnappyExec - r.CompSnappyRead,
            r.CompZstdExec - r.CompZStdRead,
        ]

        ec = "black"
        ax.bar(
            [0],
            data[0],
            color="tab:blue",
            edgecolor=ec,
            lw=0.01,
            label="Write Detect",
        )
        ax.bar(
            [1],
            data[1],
            color="tab:blue",
            # edgecolor="tab:purple",
            lw=0.01,
            hatch="...",
        )
        ax.bar(
            [2],
            data[2],
            color="tab:blue",
            # edgecolor="tab:green",
            lw=0.01,
            hatch="///",
        )
        ax.bar(
            [3], data[3], color="tab:orange", edgecolor=ec, lw=0.01, label="Write BWARE"
        )
        ax.bar(
            [4],
            data[4],
            color="tab:orange",
            # edgecolor="tab:purple",
            lw=0.01,
            hatch="...",
        )
        ax.bar(
            [5],
            data[5],
            color="tab:orange",
            # edgecolor="tab:green",
            lw=0.01,
            hatch="///",
        )

        # ax.plot(
        #     [0, 5],
        #     [uncompressedRead, uncompressedRead],
        #     color="tab:red",
        #     linewidth=1.2,
        #     alpha=0.8,
        #     path_effects=[
        #         pe.Stroke(linewidth=1.3, foreground="black", alpha=0.8),
        #         pe.Normal(),
        #     ],
        # )

        if not np.isnan(data).any():
            mx = max(max(data), mx)
            mi = min(min(data), mi)

        if id in [0, 1, 5, 6]:
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
                0.94,
                0.01,
                names[id],
                bbox=dict(boxstyle="square", pad=0.1, fc="w", ec="k", lw=0.1),
                rotation=90,
                size=6,
                ha="right",
                va="bottom",
                transform=ax.transAxes,
            )

        # print(df.loc[0])
    for id, ax in enumerate(axi):
        ax.set_xticks([])
        ax.set_yscale("log", base=10)
        ax.tick_params(axis="y", labelsize=7)

        ax.set_yscale("log", base=10)
        ax.tick_params(axis="y", labelsize=7)
        ytics = pu.set_tics_y_log10(ax, mi * 0.6, mx * 1.4)

        if id == 0:
            ax.set_ylabel("Time [s]", size=8)
            ax.yaxis.set_label_coords(-1.1, 0.5)
            ax.tick_params(axis="y", pad=-0.06)
        else:
            ax.set_yticklabels(["" for x in range(len(ytics))])

        ax.grid(True, "minor", axis="both", ls="dotted", linewidth=0.2, alpha=0.9)
        ax.grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)
    # axi[7].legend(
    #     ncol=5,
    #     loc="upper center",
    #     bbox_to_anchor=(-4.5, 1.5),
    #     fontsize=7,
    #     markerscale=0.6,
    #     handlelength=1.5,
    #     columnspacing=0.8,
    #     handletextpad=0.1,
    # )

    handles, labels = axi[7].get_legend_handles_labels()
    labels = [x.replace(" ", "\n").replace("-", "\n") for x in labels]

    plt.legend(handles,labels,
               loc='center left',
            #    alignment = 'lower center',
               bbox_to_anchor=[1.,.5],
               fontsize=7,
        markerscale=0.6,
        handlelength=1.5,
        columnspacing=0.8,
        handletextpad=0.1,
        frameon= False
        )

    # plt.subplots_adjust(
        # left=0.135, right=0.99, top=0.68, bottom=0.01, wspace=0.17, hspace=0.30
    # )
    plt.subplots_adjust(
        left=0.13, right=0.8, top=0.98, bottom=0.01, wspace=0.17, hspace=0.30
    )

    out = "plotting/plots/compress_data_time_write_" + m + ".pdf"
    print("Script", "plotting/scripts/plot_compression_size_time_write.py", "Out:", out)

    plt.savefig(out)


df = pd.read_csv("plotting/tables/comp/XPS-15-7590.csv")
plot(df, "XPS-15-7590")
df = pd.read_csv("plotting/tables/comp/dams-su1.csv")
plot(df, "su1")
