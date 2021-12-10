import argparse

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

mpl.rcParams["font.family"] = "serif"

plt.close("all")


def is_outlier(s):
    lower_limit = s.mean() - (s.std() * 1.2)
    upper_limit = s.mean() + (s.std() * 1.2)
    return ~s.between(lower_limit, upper_limit)


def parse(name):
    ds = pd.read_csv(
        name, sep=",\s+", delimiter=",", encoding="utf-8", skipinitialspace=True
    )
    ds.rename(columns=lambda x: x.strip(), inplace=True)

    ds = ds.replace(np.nan, 0)
    # ds = ds[ds["TIME sec"] > 5]
    if not ds.empty:
        mstd = ds.groupby(["mode"])["TIME sec"].std()

        if len(ds) > 10:
            ma = (
                ds[~ds.groupby("mode")["TIME sec"].apply(is_outlier)]
                .groupby(["mode"])["TIME sec"]
                .mean()
            )
        else:
            ma = ds.groupby(["mode"])["TIME sec"].mean()

        # Area variance...
        if "loc  " in ma.keys():
            local_ma = ma["loc  "]
            local_mstd = mstd["loc  "]
            mstd = mstd.drop(labels=["loc  "])
            ma = ma.drop(labels=["loc  "])
        else:
            local_ma = 0
            local_mstd = 0
    else:
        ma = 0
        local_ma = 0
        mstd = 0
        local_mstd = 0

    return ma, local_ma, mstd, local_mstd


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--data", required=True, type=str)
parser.add_argument("-l", "--location", required=True, type=str)
parser.add_argument("-c", "--config", required=False, type=str, default="")
args = parser.parse_args()

location = args.location

plotId = 0
algorithms = ["P2v2", "P2_FFN"]

NiceAlgorithmNames = ["P2_LM", "P2_FFN"]

# One column in latex is 42 pc.  https://tex.stackexchange.com/questions/8260/what-are-the-various-units-ex-em-in-pt-bp-dd-pc-expressed-in-mm
# Figure size is in inches. and there goes 6 pc in an inch.

fig, ax = plt.subplots(
    1,
    len(algorithms),
    num=None,
    figsize=((42) / 6 * 1.0, 3 * 1.0),
    dpi=80,
    facecolor="w",
    edgecolor="k",
)
for alg in algorithms:

    ma, local_ma, mstd, local_mstd = parse(
        "plots/" + args.data + "_" + alg + "_" + args.location + "_mkl_table.csv"
    )

    ax[plotId].hlines(local_ma, xmin=0, xmax=6, label="Local", color="purple")

    markerId = 0

    markers = ["o",  "v",  "s",  "*",  "D",  "^",  "",
               "", "", "", "", "", "", "", "", "", "", ""]

    linestyle = "solid"

    if len(ma) >= 7:
        ax[plotId].plot(
            [0, 1, 2, 3, 4, 5, 6],
            ma[:7],
            marker=markers[markerId],
            label="Fed LAN",
            linestyle=linestyle,
        )
        markerId += 1
        lower = ma - mstd
        upper = ma + mstd
        ax[plotId].fill_between([0, 1, 2, 3, 4, 5, 6],
                                lower[:7], upper[:7], alpha=0.2)

    # if alg in ["kmeans", "logreg","glm", "lm", "l2svm", "pca"]:
    ma, local_ma, mstd, local_mstd = parse(
        "plots/" + args.data + "_" + alg + "_XPS-15-7590_mkl_table.csv"
    )
    if len(ma) >= 7:
        ax[plotId].plot(
            [0, 1, 2, 3, 4, 5, 6],
            ma[:7],
            marker=markers[markerId],
            label="Fed WAN",
            linestyle=linestyle,
        )

    ax[plotId].set_ylim(ymin=0)
    ax[plotId].set_xlim(xmin=-0.3, xmax=6.3)

    ax[plotId].set_title(NiceAlgorithmNames[plotId])
    ax[plotId].set_xticks([0, 1, 2, 3, 4, 5, 6])
    ax[plotId].set_xticklabels([1, 2, 3, 4, 5, 6, 7])
    if plotId == 0:
        ax[plotId].set(ylabel=("Execution Time [s]"))
    ax[plotId].set(xlabel=("# Workers"))
    plotId += 1
# fig.text(0.5, 0.15, '# Workers', ha='center')
plt.subplots_adjust(
    left=0.1, right=0.97, top=0.92, bottom=0.26, wspace=0.35, hspace=0.35
)
plt.legend(
    ncol=6,
    loc="lower center",
    bbox_to_anchor=(len(algorithms) * -0.1, -0.4),
    markerscale=1.2,
)
plt.savefig("plots/pdfs/workersPL.pdf")
