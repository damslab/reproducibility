# This NimbusML script runs into performance issues (single-threaded
# and timed-out after long runtime).
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
from nimbusml.feature_extraction.categorical import OneHotVectorizer

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
warnings.filterwarnings('ignore') #cleaner, but not recommended

def readNprep(nRows):
    # Read the 1M or the 10M dataset
    if nRows == 1:
      print("Reading file: criteo_day21_1M")
      criteo = pd.read_csv("~/datasets/criteo_day21_1M", delimiter=",", header=None)
    if nRows == 10:
      print("Reading file: criteo_day21_10M")
      criteo = pd.read_csv("~/datasets/criteo_day21_10M", delimiter=",", header=None)
    print(criteo.head())
    # Replace NaNs with 0 for numeric and empty string for categorical
    criteo = criteo.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc' else x.fillna(''))

    pt = [*range(0,14)]
    criteo[pt] = criteo[pt].astype(float)
    pt = [*range(14,40)]
    criteo[pt] = criteo[pt].astype(str)

    #print(criteo.info())
    return criteo 

def transform(X):
    # Seperate categorical features
    print(X.columns)
    cat = list(X.columns[14:40])
    # Rename columns from number to alpha-numeric
    all_cols = list(X.columns[0:40])
    new_cols = ['C' + str(i) for i in all_cols]
    X.columns = new_cols
    print(X.head())
    cat_cols = ['C' + str(i) for i in cat]
    # Execute OneHot on all categorical columns
    # NOTE: the fit_transform call never completes. Killed after long time.
    t_t = time.time()
    #xf = OneHotVectorizer() << ['C35']
    xf = OneHotVectorizer() << cat_cols
    print(xf.fit_transform(X))
    print("Elapsed time for Transform = %s sec" % (time.time() - t_t))


X = readNprep(1)

t2 = time.time()
transform(X)
print("Elapsed time for transformations using mlnet = %s sec" % (time.time() - t2))

