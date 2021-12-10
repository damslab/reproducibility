
import numpy as np
import argparse
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


parser = argparse.ArgumentParser()
parser.add_argument('-x', '--datapath', type=str, required=True)
parser.add_argument('-y', '--labels', type=str, required=True)
parser.add_argument('-v', '--verbose', type=bool,   default=False)
parser.add_argument('-o', '--outputpath', type=str,  required=True)
args = parser.parse_args()

X = np.load(args.datapath, allow_pickle=True)

# https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.make_pipeline.html#sklearn.pipeline.make_pipeline
# https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html
# https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA
pca = make_pipeline(StandardScaler(), PCA(n_components=10,svd_solver="full")).fit(X)

np.savetxt(args.outputpath, pca.steps[1][1].components_, delimiter=",")