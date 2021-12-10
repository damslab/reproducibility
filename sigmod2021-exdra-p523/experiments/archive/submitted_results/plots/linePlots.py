import numpy as np
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'serif'

plt.close('all')

def is_outlier(s):
    lower_limit = s.mean() - (s.std() * 1.2)
    upper_limit = s.mean() + (s.std() * 1.2)
    return ~s.between(lower_limit, upper_limit)

def parseNoFed(name):
    with(open(name)) as f:
        return float(f.readline())

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
parser.add_argument('-a', '--algs', nargs='+')
parser.add_argument('-s', '--Salgs', nargs='+')
parser.add_argument('-n', '--networks', nargs='+')
parser.add_argument('-m', '--cnn', nargs='+')
parser.add_argument('-d', '--data', required=True, type=str)
parser.add_argument('-l', '--location', required=True, type=str)
parser.add_argument('-c', '--config', required=False, type= str, default="")
args = parser.parse_args()

sAlgorithms = args.algs
algorithms = args.Salgs
location = args.location
networks = args.networks

algorithms.append(sAlgorithms[0])
algorithms.append(sAlgorithms[1])
algorithms.append(networks[0])

algorithms.append(args.cnn[0])

plotId = 0

NiceAlgorithmNames = ["LM", "L2SVM", "MLogReg", "K-Means", "PCA", "FFN", "CNN"]

# One column in latex is 42 pc.  https://tex.stackexchange.com/questions/8260/what-are-the-various-units-ex-em-in-pt-bp-dd-pc-expressed-in-mm
# Figure size is in inches. and there goes 6 pc in an inch.

fig, ax = plt.subplots(1, len(algorithms) , num=None, figsize=((42 * 2) /6*1.0, 3*1.0), dpi=80,
                       facecolor='w', edgecolor='k')
for alg in algorithms:
    
    
    if alg == "CNN":
        args.data = "mnist"
        ma, local_ma, mstd, local_mstd = parse("plots/" + args.data + "_"+alg + "_" + args.location + "_mkl_table.csv")
    # elif alg in ["glm", "pca"]:
    #     ma, local_ma, mstd, local_mstd = parse("plots/" + args.data + "_"+alg + "_" + args.location + "_def_table.csv")
    else:
        ma, local_ma, mstd, local_mstd = parse("plots/" + args.data + "_"+alg + "_" + args.location + "_mkl_table.csv")

    ax[plotId].hlines(local_ma, xmin=0, xmax=6,
                      label="Local", color="purple")
    
    if alg not in ["CNN", "TwoNN"]:
        ax[plotId].hlines(parseNoFed("plots/" + args.data + "_"+alg + "_" + args.location + "_mkl_table_NoFed.csv"),
            xmin= 0, xmax= 6, label="Fed LowerBound", color="red")

    markerId = 0

    markers = ["o", "v", "s", "*", "D", "^", "",
               "", "", "", "", "", "", "", "", "", "", ""]
    linestyle = "solid"
    try:
        ax[plotId].plot([0, 1, 2, 3, 4, 5, 6], ma[:7],
                    marker=markers[markerId], label="Fed LAN" , linestyle=linestyle)
    except :
        print("failed on : " + alg)
    markerId += 1
    # if alg in ["kmeans", "logreg","glm", "lm", "l2svm", "pca"]:

    lower = ma - mstd 
    upper = ma + mstd 
    try:
        ax[plotId].fill_between(
        [0, 1, 2, 3, 4,5,6], lower[:7], upper[:7], alpha=0.2)
    except : 
        print("failed on : "  + alg)

    ma, local_ma, mstd, local_mstd = parse("plots/" + args.data + "_"+alg + "_XPS-15-7590_mkl_table.csv")
    # if alg in [ "pca"]:
    #     ma, local_ma, mstd, local_mstd  = parse("plots/" + args.data + "_"+alg + "_XPS-15-7590_def_table.csv")

    try:
        ax[plotId].plot([0, 1, 2, 3, 4,5,6], ma[:7],
                marker=markers[markerId], label="Fed WAN" , linestyle=linestyle)
        lower = ma - mstd 
        upper = ma + mstd 
        ax[plotId].fill_between(
            [0, 1, 2, 3, 4,5,6], lower[:7], upper[:7], alpha=0.2)
    except Exception as identifier:
        pass

    # markerId += 1
    # if alg in ["TwoNN" , "CNN"]:
    #     ma, local_ma = parse("plots/" + args.data + "_"+alg + "_XPS-15-7590_sslmkl_table.csv")
    #     ax[plotId].plot([0, 1, 2, 3, 4,5, 6], ma[:7],
    #             marker=markers[markerId], label="Fed WAN" , linestyle=linestyle)
    # markerId += 1
    # if alg == "TwoNN":
    #     ma, local_ma = parse("plots/" + args.data + "_"+alg + "_XPS-15-7590_sslmkl_table.csv")
    #     ax[plotId].plot([0, 1, 2, 3, 4,5, 6], ma[:7],
    #             marker=markers[markerId], label="MKLSSLWide" , linestyle=linestyle)
        # Hack to ensure same type lines
    # ax[plotId].plot([1000], [0],  marker=markers[markerId],
    #                     label="XY" + str(alg),  linestyle=linestyle)
    # markerId += 1
    # standard deviation

    # if ("l2svm" in alg or "logreg" in alg):
    #     ax[plotId].fill_between(
    #         [0, 1, 2, 3, 4], lower[5:], upper[5:], alpha=0.2)
    # else:
    #     # Hack to ensure same colour regions
    #     ax[plotId].fill_between(
    #         [1000], [0], [1], alpha=0.2)
    # if(plotId == 0):
    #     ax[plotId].set_ylim(ymin=0, ymax=25)
    # elif(plotId == 1):
    #     ax[plotId].set_ylim(ymin=0, ymax=35)
    # else:
    ax[plotId].set_ylim(ymin=0)
    ax[plotId].set_xlim(xmin=-0.3, xmax=6.3)

    ax[plotId].set_title(NiceAlgorithmNames[plotId])
    ax[plotId].set_xticks([0, 1, 2, 3, 4,5,6])
    ax[plotId].set_xticklabels([1, 2, 3, 4, 5,6,7])
    if plotId == 0:
        ax[plotId].set(ylabel=("Execution Time [s]"))
    if plotId == 1:
        ax[plotId].legend(ncol=6, loc="lower center",
           bbox_to_anchor=( 3.2, -0.4), markerscale=1.2)

    ax[plotId].set(xlabel=('# Workers'))
    plotId += 1
# fig.text(0.5, 0.15, '# Workers', ha='center')
plt.subplots_adjust(left=0.05, right=0.99, top=0.92, bottom=0.26, wspace=0.35,
                    hspace=0.35)
plt.savefig("plots/pdfs/workers.pdf")