
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
    with open("plots/microbenchmark/tab/table_algs_"+machines[0]+".csv", "w") as f:
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

    with open("plots/microbenchmark/tab/table_census_"+machines[0]+".csv", "w") as f:
        base = "{0:10},{1:20},{2:16},".format("DATA", "RUN", "TYPE")
        # machines = ["tango"]
        for machine in machines:
            base = base + "{0:12} {1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
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


    with open("plots/microbenchmark/tab/table_divvector_"+machines[0]+".csv", "w") as f:
        base = "{0:10},{1:20},{2:16},".format("DATA", "RUN", "TYPE")
        # machines = ["tango"]
        for machine in machines:
            base = base + "{0:12} {1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
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


    with open("plots/microbenchmark/tab/table_minusvector_"+machines[0]+".csv", "w") as f:
        base = "{0:10},{1:20},{2:16},".format("DATA", "RUN", "TYPE")
        # machines = ["tango"]
        for machine in machines:
            base = base + "{0:12} {1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
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


    with open("plots/microbenchmark/tab/table_tsmm_"+machines[0]+".csv", "w") as f:
        base = "{0:10},{1:20},{2:16},".format("DATA", "RUN", "TYPE")
        # machines = ["tango"]
        for machine in machines:
            base = base + "{0:12} {1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
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

    with open("plots/microbenchmark/tab/table_MML_"+machines[0]+".csv", "w") as f:
        base = "{0:10},{1:20},{2:16},".format("DATA", "RUN", "TYPE")
        # machines = ["tango"]
        for machine in machines:
            base = base + "{0:12} {1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
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

    with open("plots/microbenchmark/tab/table_MMR_"+machines[0]+".csv", "w") as f:
        base = "{0:10},{1:20},{2:16},".format("DATA", "RUN", "TYPE")
        # machines = ["tango"]
        for machine in machines:
            base = base + "{0:12} {1:6},{2:5},{3:10},{4:10}".format(machine, "TIME ms", "REP", "Read", "Comp") 
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

    with open("plots/microbenchmark/tab/table_algs_v2_"+machines[0]+".csv", "w") as f:
        base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")

        for machine in machines:
            base = base + "{1:20},{2:5},{3:10},{4:10}".format(machine, "TIME sec", "REP", "Read", "Comp") 


        algorithmsData = [
            "census_enc_16k",
            # "census_enc_4x_16k",
            "census_enc_8x_16k",
            "census_enc_16x_16k",
            "census_enc_32x_16k",
            "census_enc_128x_16k",
        ]
        algorithms = ["kmeans+","PCA+","mLogReg+","lmCG+","lmDS+","l2svm+"]

        algorithmsTechniques = ["ulab16-hybrid", "claWorkloadb16-hybrid"]
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


    with open("plots/microbenchmark/tab/table_algs_local_"+machines[0]+".csv", "w") as f:
        base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")

        for machine in machines:
            base = base + "{1:20},{2:5},{3:10},{4:10}".format(machine, "TIME sec", "REP", "Read", "Comp") 


        algorithmsData = ["census_enc_16k"]
        algorithms = ["kmeans+","PCA+","mLogReg+","lmCG+","lmDS+","l2svm+"]

        algorithmsTechniques = ["ulab16-hybrid", "clab16-hybrid", "claWorkloadb16-hybrid"]
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


    with open("plots/microbenchmark/tab/table_algs_sysml_" + machines[0]+".csv", "w") as f:
        base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")

        for machine in machines:
            base = base + "{1:20},{2:5},{3:10},{4:10}".format(machine, "TIME sec", "REP", "Read", "Comp") 


        algorithmsData = ["census_enc_16k", "census_enc_128x_16k",
                           "census_enc_256x_16k", 
                           "train_census_enc", "train_census_enc_128x", 
                           "train_census_enc_256x"]
        algorithms = ["l2svmml"]

        algorithmsTechniques = [ "ulab16-hybrid", "clab16-hybrid", "claWorkloadb16-hybrid"]
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
                    dataSet,
                sysmlTechniques= ["cla-sysml-hybrid-spark", "ula-sysml-hybrid-spark", "cla-sysmlb16-hybrid-spark",
                                   "ula-sysmlb16-hybrid-spark",  "ula-sysmlb16-singlenode-spark", "cla-sysmlb16-singlenode-spark"]
                )

    with open("plots/microbenchmark/tab/table_grid_" + machines[0]+".csv", "w") as f:
        base = "{0:20},{1:20},{2:35},".format("DATA", "RUN", "TYPE")

        for machine in machines:
            base = base + "{1:20},{2:5},{3:10},{4:10}".format(machine, "TIME sec", "REP", "Read", "Comp") 


        algorithmsData = ["census_enc_16k"]
        algorithms = ["GridMLogReg+"]

        algorithmsTechniques = [ "ulab16-hybrid", "clab16-hybrid", "claWorkloadb16-hybrid"]
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
