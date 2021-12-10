
import os
import sys
from datetime import datetime
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputFile',type=str, required=True)
parser.add_argument('-o', '--outputFile',type=str, required=True)
parser.add_argument('-s', '--sampleSize', type=int, required=True)
args = parser.parse_args()

with open(args.inputFile) as org:
    with open(args.outputFile +"_"+str(args.sampleSize)+".csv", "w") as des:
        header = True
        count = 0
        orgTime = 0
        for line in org:
            if header:
                des.write(line[1:])
                # des.write("time" + line)
                header = False
            else:
                sp = line.split(",")
                # if orgTime == 0:
                #     orgTime = int(datetime.strptime(sp[0],"%Y-%m-%d %H:%M:%S").timestamp())
                #     des.write(str(0))
                # else:
                #     t = int(datetime.strptime(sp[0],"%Y-%m-%d %H:%M:%S").timestamp())
                #     des.write(str(t - orgTime))
                # des.write("," + ",".join(sp[1:]))
                des.write(",".join(sp[1:]))
            count += 1
            if count > args.sampleSize:
                break

