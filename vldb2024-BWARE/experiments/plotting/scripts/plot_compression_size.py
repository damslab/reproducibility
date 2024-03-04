import pandas as pd
import plot_util as pu

import matplotlib.pyplot as plt


def plot(df, m):
    fig_size = (3.33, 0.8)
    fig, axi = plt.subplots(
        1,
        df.shape[0],
        num=None,
        figsize=fig_size,
        dpi=pu.dpi,
        facecolor="w",
        edgecolor="k",
    )

    mx = 1000000000
    mi = 1000000000
    bar_labels = ["String Type", "Detected Type", "BWARE"]

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
        if r.isnull().values.any():
            continue
        ax.bar(
            range(3),
            [r.StringSize, r.SchemaSize, r.CompSize],
            label=bar_labels,
            color=["tab:red", "tab:blue", "tab:orange"],
            edgecolor="black",
            lw=0.01,
        )
        mx = max(r.StringSize, mx)
        mi = min(r.CompSize, mi)

        ax.grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)

        if id == 5:
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
                0.025,
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
        ax.set_yscale("log", base=10)
        ax.tick_params(axis="y", labelsize=7)
        ytics = pu.set_tics_y_log10(ax, mi * 0.6, mx * 1.4)
        if id == 0:
            ax.set_ylabel("Memory [B]", size=8)
            ax.yaxis.set_label_coords(-1.1, 0.7)
        else:
            ax.set_yticklabels(["" for x in range(len(ytics))])

    axi[7].legend(
        ncol=5,
        loc="upper center",
        bbox_to_anchor=(-4.0, 1.5),
        fontsize=7,
        markerscale=0.6,
        handlelength=1.5,
        columnspacing=0.8,
        handletextpad=0.1,
    )

    plt.subplots_adjust(
        left=0.135, right=0.99, top=0.68, bottom=0.01, wspace=0.17, hspace=0.30
    )

    plt.savefig("plotting/plots/compress_data_inMemory_" + m + ".pdf")


df = pd.read_csv("plotting/tables/comp/XPS-15-7590.csv")
plot(df, "XPS-15-7590")
df = pd.read_csv("plotting/tables/comp/dams-su1.csv")
plot(df, "su1")
