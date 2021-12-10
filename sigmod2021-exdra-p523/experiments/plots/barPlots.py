
import argparse
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rc
from matplotlib.ticker import MaxNLocator
from scipy import stats


def parseOther(file):
    valid = True
    if os.path.isfile(file):
        with open(file) as f:
            time = []
            for line in f:
                if "real " in line:
                    # split = line.split("\t")
                    # t =  60 * float(split[0])
                    t = float(line.split("real ")[1].replace(",", "."))
                    time.append(t)
                # if "Total elapsed time:" in line:
                #     t = float(line.split("Total elapsed time:")[1][:-5].replace(",",".").replace("\t",""))
                #     time.append(t)
                # if "SystemDS Statistics:" in line:
                #     valid = True
        if valid and len(time) > 0:
            return time
    return [0.0]


def is_outlier(s):
    lower_limit = s.mean() - (s.std() * 1.2)
    upper_limit = s.mean() + (s.std() * 1.2)
    return ~s.between(lower_limit, upper_limit)

def parse(name):
    ds = pd.read_csv(name, sep=',\s+',
                     delimiter=',', encoding="utf-8", skipinitialspace=True)
    ds.rename(columns=lambda x: x.strip(), inplace=True)

    ds = ds.replace(np.nan, 0)
    # ds = ds[ds["TIME sec"] > 5]
    if not ds.empty:
        mstd = ds.groupby(['mode'])["TIME sec"].std()

        if(len(ds) > 10):
            ma = ds[~ds.groupby("mode")["TIME sec"].apply(is_outlier)].groupby(['mode'])["TIME sec"].mean()
        else:
            ma = ds.groupby(['mode'])["TIME sec"].mean()

        ## Area variance...
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
parser.add_argument("-l", "--location", required=True, type=str)
args = parser.parse_args()

location = args.location

mpl.rcParams['font.family'] = 'serif'

plt.close('all')

mode = ["loc", "fed"]
sp = [0.9, 0.5, 0.1]

algorithms = ["kmeans", "pca", "FNN", "CNN"]

hatchs = ["/", "\\", "--", "-", "o", "*", "", "", "", "", "", ""]

NiceAlgorithmNames = ["K-Means", "PCA", "FFN", "CNN"]
# One column in latex is 42 pc.  https://tex.stackexchange.com/questions/8260/what-are-the-various-units-ex-em-in-pt-bp-dd-pc-expressed-in-mm
# Figure size is in inches. and there goes 6 pc in an inch.
fig, ax = plt.subplots(1, len(algorithms), num=None, figsize=(42/6*1.0, 3*1.0), dpi=80,
                       facecolor='w', edgecolor='k')
plotId = 0
for alg in algorithms:
    if alg in ["kmeans"]:
        ma, local_ma, mstd, local_mstd = parse("plots/P2P_"+alg+"_"+location+"_mkl_table.csv")
        other = parseOther("results/other/"+alg + "_P2P_"+location+"_SKLEARN.log")
    elif alg in ["pca"]:
        ma, local_ma, mstd, local_mstd = parse("plots/P2P_"+alg+"_"+location+"_mkl_table.csv")
        other = parseOther("results/other/"+alg + "_P2P_"+location+"_SKLEARN.log")
        # other = parseOther("results/other/"+alg +"_P2P_XPS-15-7590_SKLEARN.log")
    elif alg in ["CNN"]:
        ma, local_ma, mstd, local_mstd = parse("plots/mnist_"+alg+"_"+location+"_mkl_table.csv")
        other = parseOther("results/other/"+alg + "_mnist_"+location+".log")
        # other = parseOther("results/other/"+alg +"_mnist_XPS-15-7590.log")
    else:
        other = parseOther("results/other/"+alg+"_P2P_"+location+".log")
        ma, local_ma, mstd, local_mstd = parse("plots/P2P_"+alg+"_"+location+"_mkl_table.csv")
        # other = parseOther("results/other/"+alg +"_P2P_XPS-15-7590.log")

    idx = 0
    axis = [" fed", " loc"]

    try:
        # err = mstd[x].iat[len(sp)-idy]
        ax[plotId].bar(idx,  ma[3], hatch=hatchs[idx], label="Fed LAN 4")
        idx += 1
        ax[plotId].bar(idx, local_ma, hatch=hatchs[idx],
                       color="purple", label="Local")
        idx += 1
        if alg in ["CNN", "FNN"]:
            ax[plotId].bar(idx, 0, hatch=hatchs[idx], label="SK-Learn")
            ax[plotId].bar(idx, sum(other) / len(other),
                           hatch=hatchs[idx], label="TensorFlow")
        else:
            ax[plotId].bar(idx, sum(other) / len(other),
                           hatch=hatchs[idx], label="SK-Learn")
            ax[plotId].bar(idx, 0, hatch=hatchs[idx], label="TensorFlow")
    except:
        print("error in plotting: " +
              alg + " index " + str(idx))
    # idy += 1
    ax[plotId].set_title(NiceAlgorithmNames[plotId])
    off = -0.2
    ax[plotId].set_xticks([])
    ax[plotId].set_xticklabels([])
    ax[plotId].yaxis.set_major_locator(MaxNLocator(integer=True))

    if plotId == 0:
        ax[plotId].set(ylabel=("Execution Time [s]"))
    plotId += 1
plt.subplots_adjust(left=0.1, right=0.99, top=0.92, bottom=0.20, wspace=0.35,
                    hspace=0.35)
# ["Fed LAN 4", "Local", "Other"],
handles, labels = ax[3].get_legend_handles_labels()
# fig.legend(handles, labels, loc='upper center')
plt.legend(handles,
           ["Fed LAN 4", "Local", "SK-Learn", "TensorFlow"],
           ncol=6, loc="lower center",
           bbox_to_anchor=(len(algorithms) * -0.42, -0.2), markerscale=1.2)
plt.savefig("plots/pdfs/mlsystems.pdf")
