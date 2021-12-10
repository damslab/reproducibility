import numpy as np
import scipy.sparse as sparse
import argparse
import sys
import time
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB

M = int(sys.argv[1])
nc = 21
no_laplace = 10
X = np.random.uniform(low=0, high=1, size=(M,1000))
y = np.random.uniform(low=0, high=nc, size=(M,1))
y = np.ceil(y)

Kc = np.floor(X.shape[1] * 0.1)
Kc = int(Kc)
R = []
t1 = time.time()
# Tune for k for PCA
for k in range(Kc, Kc+11):  
  pca = make_pipeline(StandardScaler(), PCA(n_components=k,svd_solver="full"))
  X_dr = pca.fit_transform(X)
  clf = GaussianNB()
  clf.fit(X_dr, y.ravel())
  y_nb = clf.predict(X_dr)
  R = np.concatenate((R, y_nb))

print("Time spent on PCA = %s sec" % (time.time() - t1))

# Tune var_smoothing
t1 = time.time()
for l in np.logspace(0,-9,num=no_laplace):
  pca = make_pipeline(StandardScaler(), PCA(n_components=Kc+9,svd_solver="full"))
  X_dr = pca.fit_transform(X)
  clf = GaussianNB(var_smoothing=l)
  clf.fit(X_dr, y.ravel())
  y_nb = clf.predict(X_dr)
  R = np.concatenate((R, y_nb))

print("Time spent on NB = %s sec" % (time.time() - t1))

np.savetxt("outpcakmeans.csv", R, delimiter=',');


