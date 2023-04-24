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

for machines in machinesList:

    with open("plots/microbenchmark/tab/table_colsum_"+machines[0]+".csv", "w") as f:
        base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")
        for machine in machines:
            base = base + \
               "{1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
        data_x = ["covtypeNew", "census", "airlines",
                  "infimnist_1m", "census_enc"]

        unaryAggregate = ["colsum"]
        base = base + "\n"
        f.write(base)
        for dataSet in data_x:
            for ua in unaryAggregate:
                op = "uack+"

                table_util.appendOut(
                    f,
                    "results/UA/" + ua + "/" + dataSet + "/",
                    op,
                    "UA " + ua,
                    algorithmsTechniques,
                    machines,
                    dataSet,
                    sysmlTechniques,
                )

    with open("plots/microbenchmark/tab/table_colsum+_"+machines[0]+".csv", "w") as f:
        base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")
        for machine in machines:
            base = base + \
               "{1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
        data_x = ["covtypeNew", "census", "airlines",
                  "infimnist_1m", "census_enc"]

        unaryAggregate = ["colsum+"]
        base = base + "\n"
        f.write(base)
        for dataSet in data_x:
            for ua in unaryAggregate:
                op = "uack+"

                table_util.appendOut(
                    f,
                    "results/UA/" + ua + "/" + dataSet + "/",
                    op,
                    "UA " + ua,
                    algorithmsTechniques,
                    machines,
                    dataSet,
                    sysmlTechniques,
                )

    with open("plots/microbenchmark/tab/table_sum_"+machines[0]+".csv", "w") as f:
        base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")

        for machine in machines:
            base = base + \
               "{1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
        data_x = ["covtypeNew", "census", "airlines",
                  "infimnist_1m", "census_enc"]

        unaryAggregate = ["sum"]
        base = base + "\n"
        f.write(base)
        for dataSet in data_x:
            try:
                for ua in unaryAggregate:
                    op = "uak+"

                    table_util.appendOut(
                        f,
                        "results/UA/" + ua + "/" + dataSet + "/",
                        op,
                        "UA " + ua,
                        algorithmsTechniques,
                        machines,
                        dataSet,
                        sysmlTechniques,
                    )
            except:
                print("failed reading sum" + dataSet)


    with open("plots/microbenchmark/tab/table_sum+_"+machines[0]+".csv", "w") as f:
        base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")

        for machine in machines:
            base = base + \
               "{1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
        data_x = ["covtypeNew", "census", "airlines",
                  "infimnist_1m", "census_enc"]

        unaryAggregate = ["sum+"]
        base = base + "\n"
        f.write(base)
        for dataSet in data_x:
            try:
                for ua in unaryAggregate:
                    op = "uak+"

                    table_util.appendOut(
                        f,
                        "results/UA/" + ua + "/" + dataSet + "/",
                        op,
                        "UA " + ua,
                        algorithmsTechniques,
                        machines,
                        dataSet,
                        sysmlTechniques,
                    )

            except:
                print("failed reading sum+" + dataSet)

    with open("plots/microbenchmark/tab/table_tsmm_new_"+machines[0]+".csv", "w") as f:
        base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")
        for machine in machines:
            base = base + \
               "{1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
        data_x = ["covtypeNew", "census", "airlines",
                  "infimnist_1m", "census_enc"]

        unaryAggregate = ["tsmm"]
        base = base + "\n"
        f.write(base)
        for dataSet in data_x:
            for ua in unaryAggregate:
                op = "tsmm "

                table_util.appendOut(
                    f,
                    "results/UA/" + ua + "/" + dataSet + "/",
                    op,
                    "UA " + ua,
                    algorithmsTechniques,
                    machines,
                    dataSet,
                    sysmlTechniques,
                )

    with open("plots/microbenchmark/tab/table_tsmm+_new_"+machines[0]+".csv", "w") as f:
        base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")
        for machine in machines:
            base = base + \
               "{1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
        data_x = ["covtypeNew", "census", "airlines",
                  "infimnist_1m", "census_enc"]

        unaryAggregate = ["tsmm+"]
        base = base + "\n"
        f.write(base)
        for dataSet in data_x:
            for ua in unaryAggregate:
                op = "tsmm "

                table_util.appendOut(
                    f,
                    "results/UA/" + ua + "/" + dataSet + "/",
                    op,
                    "UA " + ua,
                    algorithmsTechniques,
                    machines,
                    dataSet,
                    sysmlTechniques,
                )

    
    with open("plots/microbenchmark/tab/table_scaleshift+_"+machines[0]+".csv", "w") as f:
        base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")
        for machine in machines:
            base = base + \
               "{1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
        data_x = ["covtypeNew", "census", "airlines",
                  "infimnist_1m", "census_enc"]

        unaryAggregate = ["scaleshift+"]
        base = base + "\n"
        f.write(base)
        ops = [" uacmean ", " uacsqk+ ", " - ", " / " ]
        for dataSet in data_x:
            for ua in unaryAggregate:

                table_util.appendOut(
                    f,
                    "results/UA/" + ua + "/" + dataSet + "/",
                    ops,
                    "UA " + ua,
                    algorithmsTechniques,
                    machines,
                    dataSet,
                    sysmlTechniques,
                )

    with open("plots/microbenchmark/tab/table_scaleshift_"+machines[0]+".csv", "w") as f:
        base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")
        for machine in machines:
            base = base + \
               "{1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
        data_x = ["covtypeNew", "census", "airlines",
                  "infimnist_1m", "census_enc"]

        unaryAggregate = ["scaleshift"]
        base = base + "\n"
        f.write(base)
        ops = [" uacmean ", " uacsqk+ ", " - ", " / " ]
        for dataSet in data_x:
            for ua in unaryAggregate:

                table_util.appendOut(
                    f,
                    "results/UA/" + ua + "/" + dataSet + "/",
                    ops,
                    "UA " + ua,
                    algorithmsTechniques,
                    machines,
                    dataSet,
                    sysmlTechniques,
                )
    
    with open("plots/microbenchmark/tab/table_divvector+_"+machines[0]+".csv", "w") as f:
        base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")
        for machine in machines:
            base = base + \
               "{1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
        data_x = ["covtypeNew", "census", "airlines",
                  "infimnist_1m", "census_enc"]

        unaryAggregate = ["xdivvector+"]
        base = base + "\n"
        f.write(base)
        ops = " / " 
        for dataSet in data_x:
            for ua in unaryAggregate:

                table_util.appendOut(
                    f,
                    "results/UA/" + ua + "/" + dataSet + "/",
                    ops,
                    "UA " + ua,
                    algorithmsTechniques,
                    machines,
                    dataSet,
                    sysmlTechniques,
                )

    with open("plots/microbenchmark/tab/table_divvector_"+machines[0]+".csv", "w") as f:
        base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")
        for machine in machines:
            base = base + \
               "{1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
        data_x = ["covtypeNew", "census", "airlines",
                  "infimnist_1m", "census_enc"]

        unaryAggregate = ["xdivvector"]
        base = base + "\n"
        f.write(base)
        ops = " / " 
        for dataSet in data_x:
            for ua in unaryAggregate:

                table_util.appendOut(
                    f,
                    "results/UA/" + ua + "/" + dataSet + "/",
                    ops,
                    "UA " + ua,
                    algorithmsTechniques,
                    machines,
                    dataSet,
                    sysmlTechniques,
                )