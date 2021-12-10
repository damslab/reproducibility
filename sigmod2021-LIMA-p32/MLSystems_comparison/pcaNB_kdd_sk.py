import numpy as np
import scipy.sparse as sparse
import argparse
import sys
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB

no_laplace = 10
X = pd.read_csv("../datasets/KDD_recode_X.csv", delimiter=",", header=None)
y = pd.read_csv("../datasets/KDD_y.csv", delimiter=",", header=None)
median = np.median(y)
y = np.where(y < median, 0, 1)
X = X.to_numpy()

Kc = np.floor(X.shape[1] * 0.1)
Kc = int(Kc)
R = []
# Tune k for PCA
for k in range(Kc, Kc+11):  
  pca = make_pipeline(StandardScaler(), PCA(n_components=k,svd_solver="full"))
  X_dr = pca.fit_transform(X)
  clf = GaussianNB()
  clf.fit(X_dr, y.ravel())
  y_nb = clf.predict(X_dr)
  R = np.concatenate((R, y_nb))

# Tune var_smoothing
for l in np.logspace(0,-9,num=no_laplace):
  pca = make_pipeline(StandardScaler(), PCA(n_components=Kc+9,svd_solver="full"))
  X_dr = pca.fit_transform(X)
  clf = GaussianNB(var_smoothing=l)
  clf.fit(X_dr, y.ravel())
  y_nb = clf.predict(X_dr)
  R = np.concatenate((R, y_nb))

np.savetxt("outpcakmeans.csv", R, delimiter=',');


