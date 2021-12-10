
import numpy as np
import argparse
from sklearn.linear_model import LogisticRegression

parser = argparse.ArgumentParser()
parser.add_argument('-x', '--datapath', type=str, required=True)
parser.add_argument('-y', '--labels', type=str, required=True)
parser.add_argument('-v', '--verbose', type=bool,   default=False)
parser.add_argument('-o', '--outputpath', type=str,  required=True)
args = parser.parse_args()


X = np.load(args.datapath, allow_pickle=True)
y = np.load(args.labels, allow_pickle=True)
# https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
lr = LogisticRegression(tol=  1e-15, max_iter=30, verbose=args.verbose).fit(X,y)



np.savetxt(args.outputpath, lr.coef_, delimiter=",")

