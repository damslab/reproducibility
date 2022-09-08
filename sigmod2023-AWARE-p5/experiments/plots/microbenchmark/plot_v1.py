import os
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams["font.family"] = "serif"
plt.close("all")

tableFile = "plots/microbenchmark/table.csv"
algFile = "plots/microbenchmark/table_algs.csv"
latex_column_size = (42 / 6 * 1.0, 3 * 1.0)


def parsMM(functionName, machine, path=tableFile):

    data = {}
    if os.path.isfile(path):
        with open(path) as f:
            for line in f:
                split = [x.strip() for x in line.split(",")]
                if (
                    functionName in split[1][: len(functionName)]
                    and split[1][len(functionName):].isnumeric()
                ):
                    rowCols = int(split[1][len(functionName):])
                    if split[0] not in data.keys():
                        data[split[0]] = {}
                    if functionName not in data.get(split[0]).keys():
                        data[split[0]][functionName] = {}
                    if split[2] not in data.get(split[0]).get(functionName).keys():
                        data[split[0]][functionName][split[2]] = []

                    data[split[0]][functionName][split[2]].append(
                        (rowCols, float(split[1 + machine * 2]))
                    )
    return data


def plotMM(data, outputFilePath, title, yticks=[1, 10, 100, 1000], xlabel="# rows in left matrix", data2=None):
    fig, ax = plt.subplots(
        1,
        1,
        num=None,
        figsize=(latex_column_size[0]/2, latex_column_size[1]),
        dpi=80,
        facecolor="w",
        edgecolor="k",
    )
    x = []
    for n in data:
        x = [v[0] for v in data[n]]
        y = [v[1] for v in data[n]]
        if n == "claWorkload":
            n = "Wcla"
        ax.plot(x, y, label=n)
    if data2:
        for n in data2:
            # if n != "ula":
            x = [v[0] for v in data2[n]]
            y = [v[1] for v in data2[n]]
            if n == "claWorkload":
                n = "Wcla"
            ax.plot(x, y, label="bew-"+n)
    # print(data)
    # print(data2)
    ax.semilogx(base=2)
    ax.semilogy()
    ax.grid()
    ax.set_ylabel("execution time [ms]")
    ax.set_xlabel(xlabel)
    # ax.set_xticks([1, 2, 4, 8, 16, 32, 64, 128, 256])
    # ax.get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    # ax.set_yticks(yticks)
    # ax.get_yaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    ax.legend()
    ax.margins(x=0)
    plt.subplots_adjust(
        left=0.18, right=0.95, top=0.92, bottom=0.15, wspace=0.35, hspace=0.35
    )
    plt.title(title)
    plt.savefig(outputFilePath)
    plt.close()


def pars(functionName, machine, path=tableFile):
    data = {}
    if os.path.isfile(path):
        with open(path) as f:
            for line in f:
                split = [x.strip() for x in line.split(",")]
                # print(split[1])
                if functionName == split[1]:
                    if split[0] not in data.keys():
                        data[split[0]] = {}
                    # if(functionName not in data.get(split[0]).keys()):
                    #     data[split[0]][functionName] = {}
                    # if(split[2] not in data.get(split[0]).keys()):
                    #     data[split[0]][split[2]] = []

                    data[split[0]][split[2]] = float(split[1 + machine * 2])

    return data


def parsComp(machine):
    data = {}
    path = "plots/microbenchmark/table_compress.csv"
    if os.path.isfile(path):
        with open(path) as f:
            for line in f:
                if machine in line and not "NAN" in line and not "No File" in line:
                    split = [x.strip() for x in line.split(",")]

                    if split[0] not in data.keys():
                        data[split[0]] = {}
                    times = {}
                    times["avgT"] = float(split[3]) / 1000
                    times["rep"] = float(split[4]) / 1000
                    times["compT"] = float(split[5]) / 1000
                    times["disk"] = float(split[6]) / 1000
                    # oh no someone spotted the eval ! quickly run away !
                    # jokes aside.. it is fairly safe to do here since it is parsing a file that is just created.
                    # and not run as sudo.
                    times["phases"] = [x /1000 for x in eval(split[7].replace(":", ","))]
                    data[split[0]][split[1]] = times
    return data


def plotBar(
    data,
    outputFilePath,
    title,
    runs,
    yticks=[1, 10, 100, 1000],
    seconds=False,
    scale=True,
):

    times = []
    for x in runs:
        times.append([])
    labels = []
    for x in data:
        labels.append(x)
        for idx, r in enumerate(runs):
            if seconds and scale:
                times[idx].append(data[x][r] * 0.001)
            else:
                times[idx].append(data[x][r])

    # print(times)
    x = np.arange(len(times[0]))
    width = 2 / len(data)

    fix, ax = plt.subplots(
        1,
        1,
        num=None,
        figsize=((42) / 6 * 1.0, 3 * 1.0),
        dpi=80,
        facecolor="w",
        edgecolor="k",
    )
    # oddOffset = -((width / 2) * (len(runs) % 2))
    oddOffset = (width) * ((len(runs)) % 2) + width / 2
    startOffset = oddOffset - width * (len(runs) / 2)

    for idx, bars in enumerate(times):
        off = x + startOffset + width * idx
        ax.bar(off, bars, width, label=runs[idx])
        if idx > 0:
            for idy, t in enumerate(bars):
                speedup = times[0][idy] / t
                if speedup > 0:
                    offy = -30
                    if t < yticks[1]:
                        offy = 3
                    ax.annotate(
                        "{0:2.1f}x".format(speedup),
                        xy=(off[idy], t),
                        xytext=(0, offy),
                        textcoords="offset points",
                        ha="center",
                        va="bottom",
                        rotation=90,
                    )

    if seconds:
        ax.set_ylabel("Execution Time [s]")
    else:
        ax.set_ylabel("Execution Time [ms]")
    ax.set_xticks(x)
    ax.set_yscale("log")
    ax.set_yticks(yticks)
    ax.get_yaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    ax.set_xticklabels(labels)
    ax.legend()
    ax.margins(x=0)
    fix.autofmt_xdate(rotation=20)
    plt.title(title)
    plt.savefig(outputFilePath)

    plt.close()


def plotBarCompress(data, outputFilePath, title, runs):
    if len(data) == 0:
        return
    x = np.arange(len(data))
    width = 0.8 / len(runs)
    fix, ax = plt.subplots(
        1,
        1,
        num=None,
        figsize=(latex_column_size[0]/1.5, latex_column_size[1] * 0.6),
        dpi=80,
        facecolor="w",
        edgecolor="k",
    )


    color = [
        "tab:blue",
        "tab:orange",
        "tab:green",
        "tab:red",
        "tab:purple",
        "tab:brown",
        "tab:pink",
        "tab:gray"
    ]
    phases = ["Classification", "Grouping", "Transpose", "Compress", "Share", "Clean/GC"]

    for run in runs:
        for idx, bars in enumerate(data):
            if run in data[bars]:
                # print(data[bars][run])
                off = idx
                tot = 0
                stdsum = 0

                for idy, p in enumerate(data[bars][run]["phases"]):
                    # print(p)
                    # if isinstance(p, float):
                    #     continue
                    # elif len(p) > 0:
                    avg = p
                    # stdsum = stdsum + p
                    if avg < 0.2:
                        continue
                    if idx == 0:
                        ax.bar(
                            off,
                            avg,
                            width,
                            bottom=tot,
                            color=color[idy],
                            label=phases[idy],
                        )
                    elif idy == len(phases) - 1:
                        ax.bar(
                            off,
                            p,
                            width,
                            bottom=tot,
                            color=color[idy],
                        )
                    else:
                        ax.bar(
                            off,
                            p,
                            width,
                            bottom=tot,
                            color=color[idy],
                        )
                    tot = avg + tot
                
                if idx == 0:
                    ax.bar(off, data[bars][run]["disk"] - tot,
                           width, bottom=tot,color=color[7], label="IO")
                else:
                    ax.bar(off, data[bars][run]["disk"]- tot, width,bottom=tot, color=color[7])

    # ax.set_xticks(x)
    ax.set_ylabel("Execution Time [s]")
    ax.set_xlabel("# Million Rows")
    # ax.set_yscale("log")
    # ax.get_yaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    ax.set_xticklabels([ str(x) for x in range(len(data) + 1)])
    ax.legend(  ncol=3, loc="upper center", bbox_to_anchor=(0.38, 1.0), fontsize="x-small")
    plt.subplots_adjust(
        left=0.12, right=0.99, top=0.94, bottom=0.22, wspace=0.35, hspace=0.35
    )
    # fix.autofmt_xdate()
    # fix.autofmt_xdate(rotation=0)
    # plt.title(title)
    plt.savefig(outputFilePath)
    plt.close()


tasks = []


def p1():
    xlabel = "# rows in left matrix"
    data = parsMM("MM mml", 1)
    plotMM(data["covtypeNew"]["MM mml"],
           "plots/microbenchmark/mm/mml_covtype.pdf", "MM Left Covtype", xlabel=xlabel)
    plotMM(data["mnist"]["MM mml"],
           "plots/microbenchmark/mm/mml_mnist.pdf", "MM Left MNIST", xlabel=xlabel)
    plotMM(data["infimnist_1m"]["MM mml"],
           "plots/microbenchmark/mm/mml_infimnist_1m.pdf", "MM Left INFINIMNIST 1m", xlabel=xlabel)
    plotMM(data["binarymnist_1m"]["MM mml"],
           "plots/microbenchmark/mm/mml_binarymnist_1m.pdf", "MM Left BINARY MNIST 1m", xlabel=xlabel)
    plotMM(data["census"]["MM mml"],
           "plots/microbenchmark/mm/mml_census.pdf", "MM Left Census", xlabel=xlabel)


def p1_plus():
    xlabel = "# rows in left matrix"
    data = parsMM("MM mml+", 1)
    plotMM(data["covtypeNew"]["MM mml+"],
           "plots/microbenchmark/mm/mml+_covtype.pdf", "MM Left + Covtype", xlabel=xlabel)
    plotMM(data["mnist"]["MM mml+"],
           "plots/microbenchmark/mm/mml+_mnist.pdf", "MM Left + MNIST", xlabel=xlabel)
    plotMM(data["infimnist_1m"]["MM mml+"],
           "plots/microbenchmark/mm/mml+_infimnist_1m.pdf", "MM Left + INFINIMNIST 1m", xlabel=xlabel)
    plotMM(data["binarymnist_1m"]["MM mml+"],
           "plots/microbenchmark/mm/mml+_binarymnist_1m.pdf", "MM Left + BINARY MNIST 1m", xlabel=xlabel)
    plotMM(data["census"]["MM mml+"],
           "plots/microbenchmark/mm/mml+_census.pdf", "MM Left + Census", xlabel=xlabel)


def p2():
    xlabel = "# rows in left matrix"
    data = parsMM("MM mmls", 1)
    plotMM(data["covtypeNew"]["MM mmls"],
           "plots/microbenchmark/mm/mmls_covtype.pdf", "MM Left Sparse CovType", xlabel=xlabel)
    plotMM(data["mnist"]["MM mmls"],
           "plots/microbenchmark/mm/mmls_mnist.pdf", "MM Left Sparse MNIST", xlabel=xlabel)
    plotMM(data["infimnist_1m"]["MM mmls"],
           "plots/microbenchmark/mm/mmls_infimnist_1m.pdf", "MM Left Sparse INFINIMNIST 1m", xlabel=xlabel)
    plotMM(data["binarymnist_1m"]["MM mmls"],
           "plots/microbenchmark/mm/mmls_binarymnist_1m.pdf", "MM Left Sparse BINARY MNIST 1m", xlabel=xlabel)
    plotMM(data["census"]["MM mmls"],
           "plots/microbenchmark/mm/mmls_census.pdf", "MM Left Sparse Census", xlabel=xlabel)


def p3():
    xlabel = "# cols in right matrix"
    data = parsMM("MM mmr", 1)
    data2 = parsMM("MM mmrbem", 1)
    plotMM(data["covtypeNew"]["MM mmr"],
           "plots/microbenchmark/mm/mmr_covtype.pdf", "MM Right CovType", xlabel=xlabel, data2=data2["covtypeNew"]["MM mmrbem"])
    plotMM(data["mnist"]["MM mmr"],
           "plots/microbenchmark/mm/mmr_mnist.pdf", "MM Right MNIST", xlabel=xlabel)
    plotMM(data["infimnist_1m"]["MM mmr"],
           "plots/microbenchmark/mm/mmr_infimnist_1m.pdf", "MM Right INFINIMNIST 1m", xlabel=xlabel)
    plotMM(data["binarymnist_1m"]["MM mmr"],
           "plots/microbenchmark/mm/mmr_binarymnist_1m.pdf", "MM Right BINARY MNIST 1m", xlabel=xlabel)
    plotMM(data["census"]["MM mmr"],
           "plots/microbenchmark/mm/mmr_census.pdf", "MM Right Census", xlabel=xlabel)


def p3_plus():
    xlabel = "# cols in right matrix"
    data = parsMM("MM mmr+", 1)
    data2 = parsMM("MM mmrbem+", 1)
    plotMM(data["covtypeNew"]["MM mmr+"],
           "plots/microbenchmark/mm/mmr+_covtype.pdf", "MM Right + CovType", xlabel=xlabel, data2=data2["covtypeNew"]["MM mmrbem+"])
    plotMM(data["mnist"]["MM mmr+"],
           "plots/microbenchmark/mm/mmr+_mnist.pdf", "MM Right + MNIST", xlabel=xlabel)
    plotMM(data["infimnist_1m"]["MM mmr+"],
           "plots/microbenchmark/mm/mmr+_infimnist_1m.pdf", "MM Right + INFINIMNIST 1m", xlabel=xlabel)
    plotMM(data["binarymnist_1m"]["MM mmr+"],
           "plots/microbenchmark/mm/mmr+_binarymnist_1m.pdf", "MM Right + BINARY MNIST 1m", xlabel=xlabel)
    plotMM(data["census"]["MM mmr+"],
           "plots/microbenchmark/mm/mmr+_census.pdf", "MM Right + Census", xlabel=xlabel)


def p4():
    xlabel = "# cols in right matrix"
    data = parsMM("MM mmrs", 1)
    plotMM(data["covtypeNew"]["MM mmrs"],
           "plots/microbenchmark/mm/mmrs_covtype.pdf", "MM Right Sparse CovType", xlabel=xlabel)
    plotMM(data["mnist"]["MM mmrs"],
           "plots/microbenchmark/mm/mmrs_mnist.pdf", "MM Right Sparse MNIST", xlabel=xlabel)
    plotMM(data["infimnist_1m"]["MM mmrs"],
           "plots/microbenchmark/mm/mmrs_infimnist_1m.pdf", "MM Right Sparse INFINI MNIST 1m", xlabel=xlabel)
    plotMM(data["binarymnist_1m"]["MM mmrs"],
           "plots/microbenchmark/mm/mmrs_binarymnist_1m.pdf", "MM Right Sparse BINARY MNIST 1m", xlabel=xlabel)
    plotMM(data["census"]["MM mmrs"],
           "plots/microbenchmark/mm/mmrs_census.pdf", "MM Right Sparse Census", xlabel=xlabel)


def p5():
    data = pars("UA sum", 1)
    plotBar(data, "plots/microbenchmark/ua/sum.pdf", "Sum", ["ula", "cla"])


def p6():
    data = pars("UA rowsum", 1)
    plotBar(data, "plots/microbenchmark/ua/rowSums.pdf",
            "rowSums", ["ula", "cla"])


def p6_rowMax():
    data = pars("UA rowmax", 1)
    plotBar(data, "plots/microbenchmark/ua/rowMax.pdf",
            "rowMax", ["ula", "cla"])


def p6_colMean():
    data = pars("UA colmean", 1)
    plotBar(data, "plots/microbenchmark/ua/colMean.pdf",
            "colMean", ["ula", "cla"])


def p7():
    data = pars("UA tsmm", 1)
    plotBar(data, "plots/microbenchmark/ua/tsmm.pdf", "tsmm",
            ["ula", "cla", "claWorkload"], [50, 500, 5000, 50000])


def p7_tsmm_plus():
    data = pars("UA tsmm+", 1)
    plotBar(data, "plots/microbenchmark/ua/tsmm+.pdf", "tsmm+",
            ["ula", "cla", "claWorkload"], [50, 500, 5000, 50000])


def p8():
    data = pars("Sc plus", 1)
    plotBar(data, "plots/microbenchmark/sc/plus.pdf", "Plus", ["ula", "cla"])


def p9():
    data = pars("Sc squared", 1)
    plotBar(data, "plots/microbenchmark/sc/squared.pdf",
            "Squared", ["ula", "cla"])


def p10_xminusmeanSingle():
    data = pars("UA xminusmeanSingle", 1)
    plotBar(data, "plots/microbenchmark/ua/xminusmeanSingle.pdf",
            "X minus mean", ["ula", "cla"], [0.1, 1, 10, 30], True)


def p10_xminusmeanTrick():
    data = pars("UA xminusmeanTrick", 1)
    plotBar(data, "plots/microbenchmark/ua/xminusmeanTrick.pdf",
            "X minus mean", ["ula", "cla"], [0.1, 1, 10, 30], True)


def p11():
    data = pars("PCA", 1, algFile)
    plotBar(data, "plots/microbenchmark/alg/PCA.pdf", "PCA",
            ["ula", "cla", "claWorkload"], [1, 10, 100, 500], True, True)


def p12():
    data = pars("mLogReg", 1, algFile)
    plotBar(data, "plots/microbenchmark/alg/mLogReg.pdf", "mLogReg",
            ["ula", "cla", "claWorkload"], [1, 10, 100, 500], True, True)


def p13():
    data = parsComp("XPS")
    plotBarCompress(
        data, "plots/microbenchmark/comp/Compression.pdf", "Compression Time", [
            "cla"]
    )


def p14():
    data = pars("lmCG", 1, algFile)
    plotBar(data, "plots/microbenchmark/alg/lmCG.pdf", "lmCG",
            ["ula", "cla", "claWorkload"], [1, 10, 50], True, True)


def p15():
    data = pars("l2svm", 1, algFile)
    plotBar(data, "plots/microbenchmark/alg/l2svm.pdf", "L2SVM",
            ["ula", "cla", "claWorkload"], [1, 10, 100], True, True)


def p_comp_mnist():
    data = parsComp("charlie")
    data_infi = {k: v for (k, v) in data.items() if "infi" in k}
    # print(data_infi)
    plotBarCompress(
        data_infi, "plots/microbenchmark/comp/Compression_infi_cla.pdf", "Compression INF-MNIST Time", ["claMemory-hybrid"]
    )
    # data_binary = {k: v for (k, v) in data.items() if "binary" in k}
    # plotBarCompress(
    #     data_binary, "plots/microbenchmark/comp/Compression_binary_cla.pdf", "Compression INF-BIN-MNIST Time", ["cla"]
    # )


if __name__ == '__main__':
    # p1()
    # p1_plus()
    # p2()
    # p3()
    # p3_plus()
    # p4()
    # p5()
    # p6()
    # p6_rowMax()
    # p6_colMean()
    # p7()
    # p7_tsmm_plus()
    # p8()
    # p9()
    # p10_xminusmeanSingle()
    # p10_xminusmeanTrick()
    # p11()
    # p12()
    # p13()
    # p14()
    # p15()
    p_comp_mnist()
