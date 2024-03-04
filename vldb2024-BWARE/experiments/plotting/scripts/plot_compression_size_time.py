import pandas as pd
import plot_util as pu

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe


def plot(df, m):
    fig_size = (3.33, 0.8)
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
    # bar_labels = [None, None, "Snappy", "ZStd", None, "BEWARE-Snappy", "BEWARE-ZStd"]

    names = [
        "Adult",
        "Cat",
        "Crit10M",
        "Crypto",
        "KDD",
        "Salaries",
        "San",
        "Home",
    ]
    for id, ax in enumerate(axi):
        r = df.loc[id]

        # for ii in range(7):

        ec = "black"
        ax.bar([0], r.DetectSchemaExec - r.DetectSchemaRead, color="tab:blue", edgecolor=ec, lw=0.01)
        ax.bar(
            [1],
            r.OrgSnappyExec,
            color="tab:blue",
            edgecolor="tab:purple",
            lw=0.01,
            hatch="...",
        )
        ax.bar(
            [2],
            r.OrgZstdExec,
            color="tab:blue",
            edgecolor="tab:green",
            lw=0.01,
            hatch="///",
        )
        ax.bar([3], r.CompExec, color="tab:orange", edgecolor=ec, lw=0.01)
        ax.bar(
            [4],
            r.CompSnappyExec,
            color="tab:orange",
            edgecolor="tab:purple",
            lw=0.01,
            hatch="...",
        )
        ax.bar(
            [5],
            r.CompZstdExec,
            color="tab:orange",
            edgecolor="tab:green",
            lw=0.01,
            hatch="///",
        )

        uncompressedRead = r.DetectSchemaTime - r.DetectSchemaSysDSTime
        uncompressedRead = uncompressedRead + r.DetectSchemaCompile + r.DetectSchemaRead
        ax.plot(
            [0, 5],
            [uncompressedRead, uncompressedRead],
            color="tab:red",
            linewidth=1.2,
            alpha=0.8,
            path_effects=[
                pe.Stroke(linewidth=1.3, foreground="black", alpha=0.8),
                pe.Normal(),
            ],
        )

        mx = max(r.CompSnappyTime, mx)
        mi = min(r.CompDisk, mi)

        ax.grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)

        if id in [0,1,4,5,6,7]:
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
                0.06,
                0.01,
                names[id],
                bbox=dict(boxstyle="square", pad=0.1, fc="w", ec="k", lw=0.1),
                rotation=90,
                size=6,
                ha="left",
                va="bottom",
                transform=ax.transAxes,
            )

        # print(df.loc[0])
    for id, ax in enumerate(axi):
        ax.set_xticks([])
        # ax.set_yscale("log", base=10)
        ax.tick_params(axis="y", labelsize=7)

        rmx = round(mx + 0.5)
        # print(round(mx))
        step = round(rmx / 7)
        ytics = ax.set_yticks(range(step, rmx + step - rmx % step + 1, step))
        ax.set_ylim(0, rmx + 0.5 * step)

        # ytics=   ax.get_yticks()
        if id == 0:
            ax.set_ylabel("Time [s]", size=8)
            ax.yaxis.set_label_coords(-1.1, 0.5)
        else:
            ax.set_yticklabels(["" for x in range(len(ytics))])

    # axi[7].legend(
    #     ncol=5,
    #     loc="upper center",
    #     bbox_to_anchor=(-4.5, 1.3),
    #     fontsize=7,
    #     markerscale=0.6,
    #     handlelength=1.5,
    #     columnspacing=0.8,
    #     handletextpad=0.1,
    # )

    plt.subplots_adjust(
        left=0.135, right=0.99, top=0.99, bottom=0.01, wspace=0.17, hspace=0.30
    )

    out = "plotting/plots/compress_data_time_" + m + ".pdf"
    print("Script","/plotting/scripts/plot_compression_size_time.py", "Out:",out)

    plt.savefig(out)


df = pd.read_csv("plotting/tables/comp/XPS-15-7590.csv")
plot(df, "XPS-15-7590")
df = pd.read_csv("plotting/tables/comp/dams-su1.csv")
plot(df, "su1")
