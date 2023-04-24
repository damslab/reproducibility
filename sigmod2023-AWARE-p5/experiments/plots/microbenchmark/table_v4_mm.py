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

machinesList = [[x] for x in machinesArg]
# [["XPS-15-7590"], ["tango"]]
mVSizes = ["1", "2", "4", "8", "16", "32", "64", "128", "256"]
plus = ["", "+"]
for machines in machinesList:
    for s in mVSizes:
        for p in plus:
            with open("plots/microbenchmark/tab/table_"+s+"_euclidean"+p+"_"+machines[0]+".csv", "w") as f:
                base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")
                for machine in machines:
                    base = base + \
                        "{1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
                data_x = ["covtypeNew", "census", "airlines",
                          "infimnist_1m", "census_enc"]
                algorithmsTechniques = [
                    "ulab16-singlenode",
                    "clab16-singlenode",
                    # "claGreedyb16-singlenode",
                    "claWorkloadb16-singlenode",
                    # "claGreedyWorkloadb16-singlenode",
                ]
                sysmlTechniques = [
                    # "ula-sysml-singlenode-sysml",
                    "cla-sysml-singlenode-sysml"
                ]
                ops = [" ba+*", " * ", " + ", " uarmin"]
                base = base + "\n"
                f.write(base)
                for dataSet in data_x:

                    path = "results/MM/euclidean"+p+"-" + s + "/" + dataSet + "/"
                    table_util.appendOut(
                        f,
                        path,
                        ops,
                        "MM euclidean " + s,
                        algorithmsTechniques,
                        machines,
                        dataSet,
                        sysmlTechniques,
                    )

            with open("plots/microbenchmark/tab/table_"+s+"_mml"+p+"_"+machines[0]+".csv", "w") as f:
                base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")
                for machine in machines:
                    base = base + \
                        "{1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
                data_x = ["covtypeNew", "census", "airlines",
                          "infimnist_1m", "census_enc"]
                algorithmsTechniques = [
                    "ulab16-singlenode",
                    "clab16-singlenode",
                    # "claGreedyb16-singlenode",
                    "claWorkloadb16-singlenode",
                    # "claGreedyWorkloadb16-singlenode",
                ]
                sysmlTechniques = [
                    # "ula-sysml-singlenode-sysml",
                    "cla-sysml-singlenode-sysml"
                    ]
                ops = " ba+*"
                base = base + "\n"
                f.write(base)
                for dataSet in data_x:

                    path = "results/MM/mml"+p+"-" + s + "/" + dataSet + "/"
                    table_util.appendOut(
                        f,
                        path,
                        ops,
                        "MML " + s,
                        algorithmsTechniques,
                        machines,
                        dataSet,
                        sysmlTechniques,
                    )

            with open("plots/microbenchmark/tab/table_"+s+"_mmr"+p+"_"+machines[0]+".csv", "w") as f:
                base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")
                for machine in machines:
                    base = base + \
                        "{0:12} {1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp")
                data_x = ["covtypeNew", "census", "airlines",
                          "infimnist_1m", "census_enc"]
                algorithmsTechniques = [
                    "ulab16-singlenode",
                    "clab16-singlenode",
                    # "claGreedyb16-singlenode",
                    "claWorkloadb16-singlenode",
                    # "claGreedyWorkloadb16-singlenode",
                ]
                sysmlTechniques = [
                    # "ula-sysml-singlenode-sysml",
                    "cla-sysml-singlenode-sysml"
                    ]
                ops = " ba+*"
                base = base + "\n"
                f.write(base)
                for dataSet in data_x:

                    path = "results/MM/mmr"+p+"-" + s + "/" + dataSet + "/"
                    table_util.appendOut(
                        f,
                        path,
                        ops,
                        "MMR " + s,
                        algorithmsTechniques,
                        machines,
                        dataSet,
                        sysmlTechniques,
                    )

    with open("plots/microbenchmark/tab/table_mml_scale_"+machines[0]+".csv", "w") as f:
        base = "{0:20},{1:20},{2:30},".format("DATA", "RUN", "TYPE")

        for machine in machines:
            base = base + "{1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
        census_data = ["census_enc"]
        algorithmsTechniques = [
            "cla-sysml-singlenode-sysml", "ulab16-singlenode", "clab16-singlenode", "claWorkloadb16-singlenode"]
        matrixVectorInstances = ["mml"]
        sizes = ["1", "2", "4", "8", "16", "32", "64", "128", "256", "512", "1024"]
        sizes = ["1", "2", "4", "8", "16", "32", "64", "128", "256", "512"]
        base = base + "\n"
        f.write(base)
        for dataSet in census_data:
            for size in sizes:
                for run in matrixVectorInstances:
                    op = " ba+* "
                    if "tsmm" in run:
                        op = " tsmm "
                    if "mmrbem" in run:
                        op = [" *   ", "  ba+*  "]
                    if "mmrbem+" in run:
                        op = [" *   ", "  ba+*  ", " +   "]
                    table_util.appendOut(
                        f,
                        "results/MM/" + run + "-" + size + "/" + dataSet + "/",
                        op,
                        "MM " + run + size,
                        algorithmsTechniques,
                        machines,
                        dataSet
                    )

    with open("plots/microbenchmark/tab/table_512_seqmmr+_"+machines[0]+".csv", "w") as f:
               
        base = "{0:20},{1:20},{2:30},".format("DATA", "RUN", "TYPE")

        for machine in machines:
            base = base + "{1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
        census_data = ["census_enc"]

        algorithmsTechniques = [
            "ulab16-singlenode", 
              "claWorkloadb16NoOL-singlenode",
            "clab16-singlenode",
              "claWorkloadb16-singlenode"]
        
        sysmlTechniques = [
            "cla-sysml-singlenode-sysml",
            "cla-sysmlb16-singlenode-sysml",
            "ula-sysmlb16-singlenode-sysml"
            ]
            # "ula-sysml-singlenode-sysml",
        size = "512"

        ops = " ba+*"
        base = base + "\n"
        f.write(base)
        for dataSet in census_data:

            path = "results/MM/seqmmr-512/" + dataSet + "/"
            table_util.appendOut(
                f,
                path,
                ops,
                "MMR " + s,
                algorithmsTechniques,
                machines,
                dataSet,
                sysmlTechniques,
            )

    with open("plots/microbenchmark/tab/table_mmr_scale_"+machines[0]+".csv", "w") as f:
        base = "{0:10},{1:20},{2:16},".format("DATA", "RUN", "TYPE")
        for machine in machines:
            base = base + "{1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
        census_data = ["census_enc"]
        algorithmsTechniques = [
            "cla-sysml-singlenode-sysml", 
            "ulab16-singlenode",
            "clab16-singlenode",
            "claWorkloadb16-singlenode"]
        matrixVectorInstances = ["mmr"]
        sizes = ["1", "2", "4", "8", "16", "32", "64", "128", "256", "512"]
        base = base + "\n"
        f.write(base)
        for dataSet in census_data:
            for run in matrixVectorInstances:
                for size in sizes:
                    op = " ba+* "
                    if "tsmm" in run:
                        op = " tsmm "
                    if "mmrbem" in run:
                        op = [" *   ", "  ba+*  "]
                    if "mmrbem+" in run:
                        op = [" *   ", "  ba+*  ", " +   "]
                    table_util.appendOut(
                        f,
                        "results/MM/" + run + "-" + size + "/" + dataSet + "/",
                        op,
                        "MM " + run + size,
                        algorithmsTechniques,
                        machines,
                        dataSet
                    )