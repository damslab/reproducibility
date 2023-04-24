
import plot_util
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-x", "--machines", nargs="+", required=False)
args = parser.parse_args()
machinesList = args.machines
mVSizes = ["16"]
plus = ["", "+"]
names = ["mml", "mmr", "euclidean"]


yticks = [0.1, 1, 10, 100, 1000, 10000]
for machine in machinesList:
    for s in mVSizes:
        for p in plus:
            for name in names:
                full = s+"_"+name+p+"_"+machine
                data = plot_util.pars(
                    "plots/microbenchmark/tab/table_"+full+".csv")

                if data != {}:
                    plot_util.plotBarPartial(
                        data, "plots/microbenchmark/mm/"+full+".pdf", yticks)
