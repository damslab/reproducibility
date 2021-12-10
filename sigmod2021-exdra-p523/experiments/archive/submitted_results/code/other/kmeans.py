
import numpy as np
import argparse
from sklearn.cluster import KMeans

parser = argparse.ArgumentParser()
parser.add_argument('-x', '--datapath', type=str, required=True)
parser.add_argument('-y', '--labels', type=str, required=True)
parser.add_argument('-v', '--verbose', type=bool,  default=False)
parser.add_argument('-o', '--outputpath', type=str,  required=True)
args = parser.parse_args()

X = np.load(args.datapath, allow_pickle=True)

print(args.verbose)
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans
kmeans = KMeans(n_clusters=50, verbose = args.verbose, n_init = 1, max_iter =60, tol= 1e-16, copy_x=False, algorithm="full").fit(X)

np.savetxt(args.outputpath, kmeans.cluster_centers_, delimiter=",")
