
import numpy as np
import argparse
from sklearn.svm import LinearSVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_regression

parser = argparse.ArgumentParser()
parser.add_argument('-x', '--datapath', type=str, required=True)
parser.add_argument('-y', '--labels', type=str, required=True)
parser.add_argument('-v', '--verbose', type=bool,   default=False)
parser.add_argument('-o', '--outputpath', type=str,  required=True)
args = parser.parse_args()

X = np.load(args.datapath, allow_pickle=True)
y = np.load(args.labels, allow_pickle=True)
# http://scikit-learn.sourceforge.net/stable/modules/generated/sklearn.svm.LinearSVC.html#sklearn.svm.LinearSVC
regr = make_pipeline(StandardScaler(),
    LinearSVR(verbose=args.verbose, tol = 1e-5, max_iter = 300))

regr.fit(X,y)

np.savetxt(args.outputpath, regr.named_steps['linearsvr'].coef_, delimiter=",")

