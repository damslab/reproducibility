
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
machinesArg = args.machines

matrixVector = args.matrixVector
unaryAggregate = args.unaryAggregate
scalar = args.scalar
mVSizes = args.mVSizes
algorithms = args.algorithms

algorithmsData = args.algorithmsData
algorithmsTechniques = args.algorithmsTechniques
machinesList = [[x] for x in machinesArg]


for machines in machinesList:
 

    with open("plots/microbenchmark/tab/table_compress_"+machines[0]+".csv", "w") as f:
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
                machines,
                ["clab16-singlenode",
                    "claWorkloadb16-singlenode",
                    ],
                dataSet,
                sysmlTechniques= ["cla-sysml-singlenode-sysml"]
            )


