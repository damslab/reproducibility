
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.transforms
import numpy as np


def parse(path):
    if os.path.isfile(path):
        d = [[], [], []]
        with open(path) as f:
            for line in f:
                if "TRACE compress.CompressedMatrixBlockFactory: Cost:" in line:
                    l = line.split("Cost:")[1]
                    cost = float(l.split("Size:")[0])
                    d[0].append(cost)
                elif "DEBUG colgroup.ColGroupFactory: time[ms]:" in line:
                    l = line.split(" est ")[1]
                    sp = l.split("-- act")
                    estCost = float(sp[0])

                    d[1].append(estCost)
                    actCost = float(sp[1].split("cols:[")[0])
                    d[2].append(actCost)
        d[0].sort()
        d[1].sort()
        d[2].sort()
        return d
    else:
        return None


def moveXPoints(fig, ax):
    dy = 16.5/72.
    dx = -7/72.
    for idx, label in enumerate(ax.xaxis.get_majorticklabels()):
        offset = matplotlib.transforms.ScaledTranslation(
            dx, dy, fig.dpi_scale_trans)
        label.set_transform(label.get_transform() + offset)


def addToPlot(d, ax, fig, col, legend):
    r = range(0, len(d))
    zero = np.zeros(len(d))
    ax.plot(r, d, '--', linewidth=0.7, color=col, label=legend)
    ax.fill_between(r, d, zero, alpha=0.3, color=col)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(True, "major", axis='y', ls='--', linewidth=0.3, alpha=0.8)
    ax.grid(True, "minor", axis='x', ls='--', linewidth=0.1, alpha=0.8)


def plot(dataW, dataSW, dataC, dataS, path):
    fig = plt.figure(
        #constrained_layout=True,
                      figsize=((42) / 10 * 1.3 , 3 * 0.25 * 1.3),
                     dpi=40,
                     facecolor="w",
                     edgecolor="k",
                    #  sharey='row'
                     )

    nCol = len(dataW[0])
    nColCost = len(dataW[1])
    nColComp = len(dataC[1])
    # nColRed = max(len(dataW[1]), len(dataC[1]))

    ax = fig.add_gridspec(1, nCol * 2 + 20 + nColCost + nColComp)

    est_work = "tab:cyan"
    act_work = "tab:red"

    est_comp = "tab:purple"
    act_comp = "tab:green"


    tl = fig.add_subplot(ax[0, 0:nCol])
    bl = fig.add_subplot(ax[0, -(nColComp + nCol):-nColComp])
    tr = fig.add_subplot(ax[0, (nCol):(nCol+nColCost)])
    br = fig.add_subplot(ax[0, -nColComp:])

    addToPlot(dataW[0], tl, fig, est_work, legend="Est-Cost")
    addToPlot(dataSW[2], tl, fig, act_work, legend="Act-Cost")
    addToPlot(dataW[1], tr, fig, est_work, legend="Est-Cost")
    addToPlot(dataW[2], tr, fig, act_work, legend="Act-Cost")

    addToPlot(dataC[0],  bl, fig, est_comp, legend="Est-Comp")
    addToPlot(dataS[2], bl, fig, act_comp, legend="Act-Comp")
    addToPlot(dataC[1],  br, fig, est_comp, legend="Est-Comp")
    addToPlot(dataC[2],  br, fig, act_comp, legend="Act-Comp")

    tr.set_xticks([len(dataW[2]) - 1])
    tr.set_xticklabels([len(dataW[2])])
    moveXPoints(fig, tr)

    mt = round(max(dataW[2]))
    tr.set_ylim([0, mt])
    tl.set_ylim([0, mt])
    tt = [0,round(mt/3), round(mt/3 *2), mt]
    tl.set_yticks(tt)
    tr.set_yticks(tt)
    tr.set_yticklabels([])

    br.set_xticks([len(dataC[2]) - 1])
    br.set_xticklabels([len(dataC[2])])
    moveXPoints(fig, br)

    mb = round(max(dataC[2]))
    br.set_ylim([0, mb])
    bl.set_ylim([0, mb])
    tb = [0,round(mb/3), round(mb/3 *2), mb]
    bl.set_yticks(tb)
    br.set_yticks(tb)
    br.set_yticklabels([])


    # for aa in ax:
    #     for a in aa:
    tl.margins(x=0, y=0)
    bl.margins(x=0, y=0)
    tr.margins(x=0, y=0)
    br.margins(x=0, y=0)

    tl.set_ylabel("TOPS")
    tl.yaxis.set_label_coords(-0.2, 0.5)
    bl.set_ylabel("MB")
    bl.yaxis.set_label_coords(-0.12, 0.5)

    tl.set_xlabel("Individual Columns")
    # bl.set_xlabel("Individual Columns")
    bl.xaxis.set_label_coords(0.5, -0.1)

    # tr.set_xlabel("Groups")
    br.set_xlabel("Groups")
    br.xaxis.set_label_coords(0.5, -0.1)

    tl.legend(ncol=1, loc="upper center", bbox_to_anchor=(
        0.3, 1.1), frameon=False,
        fontsize=7.45)

    bl.legend(ncol=1, loc="upper center", bbox_to_anchor=(
    0.3, 1.1), frameon=False,
    fontsize=7.45)
    plt.subplots_adjust(
        left=0.09, right=0.995, top=0.92, bottom=0.2, wspace=0, hspace=0.25
    )

    plt.savefig(path)
    plt.close()


def scaleToMB(data):
    for idx, d in enumerate(data):
        data[idx] = [x / 1000000 for x in d]
    return data


def scaleToGigaFLOPS(data):
    for idx, d in enumerate(data):
        data[idx] = [x / 1000000 for x in d]
    return data


sources = ["covtypeNew", "census", "census_enc", "airlines", "infimnist_1m"]
machine = "XPS-15-7590"
work = "claWorkloadb16-singlenode"
comp = "clab16-singlenode"
static = "claStatic-singlenode"
staticW = "claStaticWorkload-singlenode"

for s in sources:

    dataW = parse("results/compression/" + s +
                  "/" + machine + "/" + work + ".log")
    dataSW = parse("results/compression/" + s +
                   "/" + machine + "/" + staticW + ".log")
    dataS = parse("results/compression/" + s +
                  "/" + machine + "/" + static + ".log")
    dataC = parse("results/compression/" + s +
                  "/" + machine + "/" + comp + ".log")

    dataW = scaleToGigaFLOPS(dataW)
    dataSW = scaleToGigaFLOPS(dataSW)
    dataS = scaleToMB(dataS)
    dataC = scaleToMB(dataC)

    plot(dataW, dataSW, dataC, dataS, "plots/microbenchmark/comp/"+s+"-v2.pdf")
