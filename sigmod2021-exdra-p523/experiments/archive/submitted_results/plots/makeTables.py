
import os
import numpy as np
import sys
import argparse


def parse(algorithm, execution, x, samplesize, location):
    if samplesize:
        file = "results/" + execution + "/" + algorithm + \
            "_" + x+"_" + str(samplesize) + "_"+location+ ".log"
    else:
        file = "results/" + execution + "/" + algorithm + "_" + x + "_" +location+ ".log"
    # print(file)
    # valid = False
    valid = True
    if os.path.isfile(file):
        with open(file) as f:
            time = []
            for line in f:
                if "real " in line:
                    # split = line.split("\t")
                    # t =  60 * float(split[0])
                    t = float(line.split("real ")[1].replace(",", "."))
                    time.append(t)
                # if "Total elapsed time:" in line:
                #     t = float(line.split("Total elapsed time:")[1][:-5].replace(",",".").replace("\t",""))
                #     time.append(t)
                # if "SystemDS Statistics:" in line:
                #     valid = True
        if valid and len(time) > 0:
            return time
    return [float("NaN")]


parser = argparse.ArgumentParser()
parser.add_argument('-a', '--algs', nargs='+', required=True)
parser.add_argument('-s', '--samplesize', type=int)
parser.add_argument('-n', '--numberOfWorkers', required=True, type=int)
parser.add_argument('-d', '--data', required=True, type=str)
parser.add_argument('-l', '--location', required =True, type=str)
parser.add_argument('-y', '--includeY', required =False, type= bool, default=False)
parser.add_argument('-o', '--includeOther', required =False, type= bool, default=False)
parser.add_argument('-c', '--config', required=False, type= str, default="")
args = parser.parse_args()

executions = ["loc"]

if args.includeOther:
    executions.append("other")

for x in range(1, args.numberOfWorkers + 1):
    executions.append("fed" + str(x))

if args.includeY:
    for x in range(args.numberOfWorkers):
        executions.append("fedy" + str(x))


algorithms = args.algs

for algorithm in algorithms:
    # print("making table for: " + algorithm)
    with open("plots/"+args.data+"_"+algorithm+"_"+args.location+ args.config+"_table.csv", "w") as f:
        f.write("{0:10}, {1:5}\n".format("TIME sec", "mode"))
        for execution in executions:
            for time in parse(algorithm, execution, args.data, args.samplesize, args.location + args.config):
                f.write("{0:10.3f}, {1:5}\n".format(time, execution))
