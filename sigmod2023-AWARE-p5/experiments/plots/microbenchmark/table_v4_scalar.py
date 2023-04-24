import argparse
import os

import numpy as np

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


machinesList =  [[x] for x in machinesArg]

algorithmsTechniques = [
    "ulab16-singlenode",
    "clab16-singlenode",
    # "claGreedyb16-singlenode",
    "claWorkloadb16-singlenode",
    # "claGreedyWorkloadb16-singlenode",
]
sysmlTechniques = [
    # "ula-sysml-singlenode-sysml",
    "cla-sysml-singlenode-sysml"]

for machines in machinesList:
    with open("plots/microbenchmark/tab/table_scalar_plus_"+machines[0]+".csv", "w") as f:
        base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")
        for machine in machines:
            base = base + \
                "{1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
        data_x = ["covtypeNew", "census", "airlines",
                  "infimnist_1m", "census_enc"]

        scalar = ["plus"]
        base = base + "\n"
        f.write(base)
        for dataSet in data_x:
            for sc in scalar:
                if sc == "plus":
                    op = " + "

                table_util.appendOut(
                    f,
                    "results/Sc/" + sc + "/" + dataSet + "/",
                    op,
                    "Sc " + sc,
                    algorithmsTechniques,
                    machines,
                    dataSet,
                    sysmlTechniques,
                )
    with open("plots/microbenchmark/tab/table_scalar_plus+_"+machines[0]+".csv", "w") as f:
        base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")
        for machine in machines:
            base = base + \
                "{1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
        data_x = ["covtypeNew", "census", "airlines",
                  "infimnist_1m", "census_enc"]

        scalar = ["plus+"]
        base = base + "\n"
        f.write(base)
        for dataSet in data_x:
            for sc in scalar:
                if sc == "plus":
                    op = " + "

                table_util.appendOut(
                    f,
                    "results/Sc/" + sc + "/" + dataSet + "/",
                    op,
                    "Sc " + sc,
                    algorithmsTechniques,
                    machines,
                    dataSet,
                    sysmlTechniques,
                )

    with open("plots/microbenchmark/tab/table_scalar_mult_"+machines[0]+".csv", "w") as f:
        base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")
        for machine in machines:
            base = base + \
                "{1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
        data_x = ["covtypeNew", "census", "airlines",
                  "infimnist_1m", "census_enc"]

        scalar = ["mult"]
        base = base + "\n"
        f.write(base)
        for dataSet in data_x:
            for sc in scalar:
                if sc == "mult":
                    op = " * "

                table_util.appendOut(
                    f,
                    "results/Sc/" + sc + "/" + dataSet + "/",
                    op,
                    "Sc " + sc,
                    algorithmsTechniques,
                    machines,
                    dataSet,
                    sysmlTechniques,
                )
