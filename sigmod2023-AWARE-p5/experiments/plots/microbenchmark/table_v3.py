
import argparse
import table_util

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--data", nargs="+", required=False)
parser.add_argument("-t", "--techniques", nargs="+", required=False)
parser.add_argument("-m", "--matrixVector", nargs="+", required=False)
parser.add_argument("-s", "--mVSizes", nargs="+", required=False)

parser.add_argument("-a", "--algorithms", nargs="+", required=False)
parser.add_argument("-b", "--algorithmsData", nargs="+", required=False)
parser.add_argument("-tt", "--algorithmsTechniques", nargs="+", required=False)

parser.add_argument("-u", "--unaryAggregate", nargs="+", required=False)
parser.add_argument("-c", "--scalar", nargs="+", required=False)
parser.add_argument("-v", "--compressMeasures", nargs="+", required=False)
parser.add_argument("-x", "--machines", nargs="+", required=False)
args = parser.parse_args()


compressionTypes = args.techniques
compressMeasures = args.compressMeasures
dataSets = args.data
machines = args.machines

matrixVector = args.matrixVector
unaryAggregate = args.unaryAggregate
scalar = args.scalar
mVSizes = args.mVSizes
algorithms = args.algorithms

algorithmsData = args.algorithmsData
algorithmsTechniques = args.algorithmsTechniques


with open("plots/microbenchmark/table_algs.csv", "w") as f:
    base = "{0:10},{1:20},{2:16},".format("DATA", "RUN", "TYPE")
    for machine in machines:
        base = base + "{0:12} {1:6},{2:5},".format(machine, "T   sec", "REP")

    base = base + "\n"
    f.write(base)
    for dataSet in dataSets:
        for alg in algorithms:
            op = None
            table_util.appendOut(
                f,
                "results/algorithms/" + alg + "/" + dataSet + "/",
                None,
                alg,
                compressionTypes,
                machines,
                dataSet
            )

with open("plots/microbenchmark/table_census.csv", "w") as f:
    base = "{0:10},{1:20},{2:16},".format("DATA", "RUN", "TYPE")
    machines = ["tango"]
    for machine in machines:
        base = base + "{0:12} {1:6},{2:5},".format(machine, "TIME ms", "REP")
    census_data = [
        "census_enc_16k",
        "census_enc_4x_16k",
        "census_enc_8x_16k",
        "census_enc_16x_16k",
    ]
    algorithmsTechniques = ["ulab16-hybrid", "claWorkloadb16-hybrid"]
    unaryAggregate = ["sum", "sum+"]
    base = base + "\n"
    f.write(base)
    for dataSet in census_data:
        for ua in unaryAggregate:
            op = " ua"
            if "row" in ua:
                op += "r"
            elif "col" in ua:
                op += "c"

            if "max" in ua:
                op += "max"
            elif "mean" in ua:
                op += "mean"
                if "xminusmean" in ua:
                    op = [" uacmean", " -     "]
                    if "Single" in ua:
                        op = None
            elif "min" in ua:
                op += "min"
            elif "sq" in ua:
                op += "sqk+"
            elif "sum" in ua:
                op += "k+"
            elif "tsmm" in ua:
                op = " tsmm "

            table_util.appendOut(
                f,
                "results/UA/" + ua + "/" + dataSet + "/",
                op,
                "UA " + ua,
                algorithmsTechniques,
                machines,
                dataSet
            )


with open("plots/microbenchmark/table_divvector.csv", "w") as f:
    base = "{0:10},{1:20},{2:16},".format("DATA", "RUN", "TYPE")
    machines = ["tango"]
    for machine in machines:
        base = base + "{0:12} {1:6},{2:5},".format(machine, "TIME ms", "REP")
    data_x = ["covtypeNew", "census", "airlines",
              "infimnist_1m_16k", "census_enc_16k"]
    algorithmsTechniques = ["ulab16-hybrid", "claWorkloadb16-hybrid"]
    unaryAggregate = ["xdivvector", "xdivvector+"]
    base = base + "\n"
    f.write(base)
    for dataSet in data_x:
        for ua in unaryAggregate:
            op = " "
            if "div" in ua:
                op += "/ "
            if "minus" in ua:
                op += "- "

            table_util.appendOut(
                f,
                "results/UA/" + ua + "/" + dataSet + "/",
                op,
                "UA " + ua,
                algorithmsTechniques,
                machines,
                dataSet
            )


with open("plots/microbenchmark/table_minusvector.csv", "w") as f:
    base = "{0:10},{1:20},{2:16},".format("DATA", "RUN", "TYPE")
    machines = ["tango"]
    for machine in machines:
        base = base + "{0:12} {1:6},{2:5},".format(machine, "TIME ms", "REP")
    data_x = ["covtypeNew", "census", "airlines",
              "infimnist_1m_16k", "census_enc_16k"]
    algorithmsTechniques = ["ulab16-hybrid", "claWorkloadb16-hybrid"]
    unaryAggregate = ["xminusvector", "xminusvector+"]
    base = base + "\n"
    f.write(base)
    for dataSet in data_x:
        for ua in unaryAggregate:
            op = " "
            if "div" in ua:
                op += "/ "
            if "minus" in ua:
                op += "- "

            table_util.appendOut(
                f,
                "results/UA/" + ua + "/" + dataSet + "/",
                op,
                "UA " + ua,
                algorithmsTechniques,
                machines,
                dataSet
            )


with open("plots/microbenchmark/table_tsmm.csv", "w") as f:
    base = "{0:10},{1:20},{2:16},".format("DATA", "RUN", "TYPE")
    machines = ["tango"]
    for machine in machines:
        base = base + "{0:12} {1:6},{2:5},".format(machine, "TIME ms", "REP")
    data_x = ["covtypeNew", "census", "airlines",
              "infimnist_1m_16k", "census_enc_16k"]
    algorithmsTechniques = ["ulab16-hybrid", "claWorkloadb16-hybrid"]
    unaryAggregate = ["tsmm", "tsmm+"]
    base = base + "\n"
    f.write(base)
    for dataSet in data_x:
        for ua in unaryAggregate:
            op = " tsmm"

            table_util.appendOut(
                f,
                "results/UA/" + ua + "/" + dataSet + "/",
                op,
                "UA " + ua,
                algorithmsTechniques,
                machines,
                dataSet
            )

with open("plots/microbenchmark/table_MML.csv", "w") as f:
    base = "{0:10},{1:20},{2:16},".format("DATA", "RUN", "TYPE")
    machines = ["tango"]
    for machine in machines:
        base = base + "{0:12} {1:6},{2:5},".format(machine, "TIME ms", "REP")
    data_x = ["covtypeNew", "census", "airlines",
              "infimnist_1m_16k", "census_enc_16k"]
    algorithmsTechniques = ["ulab16-hybrid", "claWorkloadb16-hybrid"]
    matrixVector = ["mml", "mml+"]
    mVSizes = ["16"]
    base = base + "\n"
    f.write(base)
    for dataSet in data_x:
        for run in matrixVector:
            for size in mVSizes:
                op = " ba+* "

                table_util.appendOut(
                    f,
                    "results/MM/" + run + "-" + size + "/" + dataSet + "/",
                    op,
                    "MM " + run + size,
                    algorithmsTechniques,
                    machines,
                    dataSet
                )

with open("plots/microbenchmark/table_MMR.csv", "w") as f:
    base = "{0:10},{1:20},{2:16},".format("DATA", "RUN", "TYPE")
    machines = ["tango"]
    for machine in machines:
        base = base + "{0:12} {1:6},{2:5},".format(machine, "TIME ms", "REP")
    data_x = ["covtypeNew", "census", "airlines",
              "infimnist_1m_16k", "census_enc_16k"]
    algorithmsTechniques = ["ulab16-hybrid", "claWorkloadb16-hybrid"]
    matrixVector = ["mmr", "mmr+"]
    mVSizes = ["16"]
    base = base + "\n"
    f.write(base)
    for dataSet in data_x:
        for run in matrixVector:
            for size in mVSizes:
                op = " ba+* "

                table_util.appendOut(
                    f,
                    "results/MM/" + run + "-" + size + "/" + dataSet + "/",
                    op,
                    "MM " + run + size,
                    algorithmsTechniques,
                    machines,
                    dataSet
                )

with open("plots/microbenchmark/table_algs_v2.csv", "w") as f:
    base = "{0:20},{1:20},{2:30},".format("DATA", "RUN", "TYPE")

    machines = ["tango"]
    for machine in machines:
        base = base + "{0:12} {1:6},{2:5},".format(machine, "T   sec", "REP")


    algorithmsData = [
        "census_enc_16k",
        # "census_enc_4x_16k",
        "census_enc_8x_16k",
        "census_enc_16x_16k",
        "census_enc_32x_16k",
        "census_enc_128x_16k",
    ]
    algorithms = ["kmeans","kmeans+","PCA","PCA+","mLogReg","mLogReg+","lmCG","lmCG+","lmDS","lmDS+","l2svm","l2svm+"]
    base = base + "\n"
    f.write(base)
    for dataSet in algorithmsData:
        for alg in algorithms:
            op = None
            table_util.appendOut(
                f,
                "results/algorithms/" + alg + "/" + dataSet + "/",
                None,
                alg,
                algorithmsTechniques,
                machines,
                dataSet
            )

with open("plots/microbenchmark/table_algs_v2_xps.csv", "w") as f:
    base = "{0:20},{1:20},{2:30},".format("DATA", "RUN", "TYPE")

    machines = ["XPS-15-7590"]
    for machine in machines:
        base = base + "{0:12} {1:6},{2:5},".format(machine, "T   sec", "REP")

    algorithmsData = [
        "census_enc",
        "census_enc_2x"
    ]
    algorithmsTechniques = ["ulab16-singlenode", "claWorkloadb16-singlenode"]
    algorithms = ["kmeans","kmeans+","PCA","PCA+","mLogReg","mLogReg+","lmCG","lmCG+","lmDS","lmDS+","l2svm","l2svm+"]
    base = base + "\n"
    f.write(base)
    for dataSet in algorithmsData:
        for alg in algorithms:
            op = None
            table_util.appendOut(
                f,
                "results/algorithms/" + alg + "/" + dataSet + "/",
                None,
                alg,
                algorithmsTechniques,
                machines,
                dataSet
            )
