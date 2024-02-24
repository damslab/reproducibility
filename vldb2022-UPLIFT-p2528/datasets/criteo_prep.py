import sys
import time
import numpy as np
import scipy as sp
from scipy.sparse import csr_matrix
import pandas as pd
import math
import warnings
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import preprocessing

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
warnings.filterwarnings('ignore') #cleaner, but not recommended

def readNprep(nRows):
    # Read the 1M or the 10M dataset
    if nRows == 1:
      print("Reading file: criteo_day21_1M")
      criteo = pd.read_csv("criteo_day21_1M", delimiter=",", header=None)
    if nRows == 10:
      print("Reading file: criteo_day21_10M")
      criteo = pd.read_csv("criteo_day21_10M", delimiter=",", header=None)
    if nRows == 5:
      print("Reading file: criteo_day21_5M")
      criteo = pd.read_csv("criteo_day21_5M", delimiter=",", header=None)
    print(criteo.head())

    # Replace NaNs 
    #criteo = criteo.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc' else x.fillna(''))
    criteo = criteo.fillna(method="ffill")
    criteo = criteo.fillna(method="bfill")
    print(criteo.head())

    return criteo 

nRows = int(sys.argv[1])
X = readNprep(nRows)
if nRows == 1:
  X.to_csv("criteo_day21_1M_cleaned", header=None, index=False)
if nRows == 10:
  X.to_csv("criteo_day21_10M_cleaned", header=None, index=False)
if nRows == 5:
  X.to_csv("criteo_day21_5M_cleaned", header=None, index=False)

#np.savetxt("X_prep_sk.csv", X_prep, fmt='%1.2f', delimiter=',') #dense
#sp.sparse.save_npz("X_prep_sk.npz", X_prep)  #sparse

