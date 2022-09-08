
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


with open("plots/microbenchmark/table_compress_inf.csv", "w") as f:
    base = "{0:15},{1:33},{2:15},{3:10},{4:5},{5:8},{6:10},{7:37}\n".format(
        "DATA", "TYPE", "MACHINE", "AVGTOTAL", "REP", "DISK", "AVGCOMP", "Ratio", "Phases"
    )
    f.write(base)
    datasets_compression = [
        "infimnist_1m",
        "infimnist_2m",
        "infimnist_3m",
        "infimnist_4m",
        "infimnist_5m",
        "infimnist_6m",
        "infimnist_7m",
        "infimnist_8m"
    ]
    for dataSet in datasets_compression:
        table_util.appendOutComp(
            f,
            "results/compression/" + dataSet + "/",
            " compress ",
            "Compress ",
            ["tango"],
            compressMeasures,
            dataSet
        )


with open("plots/microbenchmark/table_compress_all_xps.csv", "w") as f:
    base = "{0:15},{1:33},{2:15},{3:10},{4:5},{5:8},{6:10},{7:37}\n".format(
        "DATA", "TYPE", "MACHINE", "AVGTOTAL", "REP", "DISK", "AVGCOMP", "Ratio", "Phases"
    )
    f.write(base)
    datasets_compression = [
        "airlines",
        "amazon",
        "covtypeNew",
        "census",
        "census_enc",
        "infimnist_1m",
    ]
    for dataSet in datasets_compression:
        table_util.appendOutComp(
            f,
            "results/compression/" + dataSet + "/",
            " compress ",
            "Compress ",
            ["XPS-15-7590"],
            ["clab16-singlenode", "claGreedyb16-singlenode",
                "claWorkloadb16-singlenode",
                "claGreedyWorkloadb16-singlenode", "claStatic-singlenode"],
            dataSet,
            sysmlTechniques= ["cla-sysml-singlenode-sysml"]
        )


with open("plots/microbenchmark/table_compress.csv", "w") as f:
    base = "{0:15},{1:33},{2:15},{3:10},{4:5},{5:8},{6:10},{7:37}\n".format(
        "DATA", "TYPE", "MACHINE", "AVGTOTAL", "REP", "DISK", "AVGCOMP", "Ratio", "Phases"
    )
    f.write(base)
    datasets_compression = [
        "airlines",
        "amazon",
        "covtypeNew",
        "census",
        "census_enc",
        "infimnist_1m",
    ]
    for dataSet in datasets_compression:
        table_util.appendOutComp(
            f,
            "results/compression/" + dataSet + "/",
            " compress ",
            "Compress ",
            ["tango"],
            ["clab16-singlenode", "claGreedyb16-singlenode",
                "claWorkloadb16-singlenode",
                "claGreedyWorkloadb16-singlenode", "claStatic-singlenode"],
            dataSet,
            sysmlTechniques= ["cla-sysml-singlenode-sysml"]
        )

