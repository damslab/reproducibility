
import argparse

import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVR

parser = argparse.ArgumentParser()
parser.add_argument('-x', '--datapath', type=str, required=True)
parser.add_argument('-y', '--labels', type=str, required=True)
parser.add_argument('-v', '--verbose', type=bool,   default=False)
parser.add_argument('-o', '--outputpath', type=str,  required=True)
args = parser.parse_args()

X = np.load(args.datapath, allow_pickle=True)
y = np.load(args.labels, allow_pickle=True)

clf = make_pipeline(StandardScaler(),
                    SGDClassifier(max_iter=1000, tol=1e-3))
clf.fit(X, y)

