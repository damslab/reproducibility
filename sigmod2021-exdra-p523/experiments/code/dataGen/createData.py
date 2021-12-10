import argparse
import numpy as np
import os

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', type=str, required=True)
args = parser.parse_args()

basePath = "data/" + args.path + ".csv"
savePath = "data/" + args.path + ".npy"

# Save X
if os.path.isfile(basePath):
    # print("its a file!")
    X = np.genfromtxt(basePath, delimiter=',', skip_header=0)
    np.save(savePath, X)
elif os.path.isdir(basePath):
    # print("its a directory!")
    files = os.listdir(basePath)
    X = np.genfromtxt(basePath + "/" + files[0], delimiter=',', skip_header=0)
    for f in files[1:]:
        A = np.genfromtxt(basePath + "/" + f, delimiter=',', skip_header=0)
        X = np.concatenate((X, A), axis=0)
    np.save(savePath, X)
else:
    print("error No datafile at there. " + basePath)

