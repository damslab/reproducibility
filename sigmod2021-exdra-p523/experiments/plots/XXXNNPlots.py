import numpy as np
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'serif'

plt.close('all')

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--algs', nargs='+', required=True)
parser.add_argument('-d', '--data', required=True, type=str)
parser.add_argument('-l', '--location', required=True, type=str)
args = parser.parse_args()

algorithms = args.algs


NiceAlgorithmNames = ["CCN", "FFN"]

plotId = 0
# One column in latex is 42 pc.
# https://tex.stackexchange.com/questions/8260/what-are-the-various-units-ex-em-in-pt-bp-dd-pc-expressed-in-mm
# Figure size is in inches. and there goes 6 pc in an inch.
fig, ax = plt.subplots(1, len(algorithms), num=None, figsize=(42/6*1.0, 3*1.0), dpi=80,
                       facecolor='w', edgecolor='k')
for alg in algorithms:

    ds = pd.read_csv("plots/" + args.data + "_"+alg + "_" + args.location + "_def_table.csv", sep=',\s+',
                     delimiter=',', encoding="utf-8", skipinitialspace=True)
    ds.rename(columns=lambda x: x.strip(), inplace=True)
    ma = ds.groupby(['mode'])[
        "TIME sec"].mean().replace(np.nan, 0)

    local_ma = ma["loc  "]
    ma = ma.drop(labels=["loc  "])
    ax[plotId].hlines(local_ma, xmin=0, xmax=6,
                      label="loc", color="purple")

    for opt in ["_mkl", "_ssl"]:
        optEx = pd.read_csv("plots/" + args.data + "_"+alg + "_" + args.location + opt + "_table.csv", sep=',\s+',
                            delimiter=',', encoding="utf-8", skipinitialspace=True)
        optEx.rename(columns=lambda x: x.strip(), inplace=True)

        ds = pd.concat([ds, optEx], axis=1, ignore_index=True)
    ds = ds.drop(labels=[1, 3, 5], axis=1)
    ds = ds.drop(labels=[0])

    markerId = 0
    markers = ["o", "v", "s", "*", "D", "^", "",
               "", "", "", "", "", "", "", "", "", "", ""]

    linestyle = "solid"
    ax[plotId].plot([0, 1, 2, 3, 4, 5, 6], ds[0],
                    marker=markers[markerId], label="default",
                    linestyle=linestyle)
    markerId += 1
    ax[plotId].plot([0, 1, 2, 3, 4, 5, 6], ds[2],
                    marker=markers[markerId], label="MKL",
                    linestyle=linestyle)
    markerId += 1
    ax[plotId].plot([0, 1, 2, 3, 4, 5, 6], ds[4],
                    marker=markers[markerId], label="SSL",
                    linestyle=linestyle)
    markerId += 1

    ax[plotId].set_title(NiceAlgorithmNames[plotId])
    ax[plotId].set_xticks([0, 1, 2, 3, 4, 5, 6])
    ax[plotId].set_xticklabels([1, 2, 3, 4, 5, 6, 7])
    if plotId == 0:
        ax[plotId].set(ylabel=("Execution Time [s]"))
    ax[plotId].set(xlabel=('# Workers'))
    plotId += 1

# fig.text(0.5, 0.15, '# Workers', ha='center')
plt.subplots_adjust(left=0.12, right=0.99, top=0.92, bottom=0.26, wspace=0.35,
                    hspace=0.35)
plt.legend(ncol=6, loc="lower center",
           bbox_to_anchor=(len(algorithms) * -0.13, -0.4), markerscale=1.2)
plt.savefig("plots/pdfs/NN.pdf")
