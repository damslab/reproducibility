import sys
import time
import numpy as np
import scipy as sp
from scipy.sparse import csr_matrix
import pandas as pd
import dask.dataframe as ddf
from dask.dataframe import from_pandas
from dask_ml.preprocessing import Categorizer, OrdinalEncoder, OneHotEncoder
from dask.distributed import Client, LocalCluster
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
      criteo = ddf.read_csv("../..datasets/criteo_day21_1M", delimiter=",", assume_missing=True, header=None)
    if nRows == 10:
      print("Reading file: criteo_day21_10M")
      criteo = ddf.read_csv("../../datasets/criteo_day21_10M", delimiter=",", assume_missing=True, header=None)
    print(criteo.head())
    # Replace NaNs with backward and forward fill
    criteo = criteo.fillna(method="ffill").fillna(method="bfill").persist().compute()
    print(criteo.head())
    return criteo 

def transformRC(X, cluster):
    with Client(cluster) as client:
        # Seperate categorical features
        cat_ddf = X.select_dtypes(exclude=np.float64)
        pipe = make_pipeline(
                Categorizer(), #build phase
                OrdinalEncoder()) #recoding
        trn = pipe.fit_transform(cat_ddf)
    print(trn.head())
    return trn

def transformDC(X):
    # Use Dask Distributed (local) scheduler
    cluster = LocalCluster()
    with Client(cluster) as client:
        cat_ddf = X.select_dtypes(exclude=np.float64)
        pipe = make_pipeline(
                Categorizer(), #build phase
                OneHotEncoder()) #onehot -> takes 11608sec
        trn = pipe.fit_transform(cat_ddf)
    return trn
 

if __name__ == '__main__':
    X = readNprep(10)

    # Use Dask Distributed (local) scheduler
    cluster = LocalCluster()
    print(cluster)
    totTime = 0
    t1 = time.time()
    X_enc1 = transformRC(X, cluster)
    totTime = totTime + ((time.time() - t1) * 1000) #millisec
    print("Elapsed time for transformations via dask = %s sec" % (time.time() - t1))

    t1 = time.time()
    X_enc2 = transformRC(X, cluster)
    totTime = totTime + ((time.time() - t1) * 1000) #millisec
    print("Elapsed time for transformations via dask = %s sec" % (time.time() - t1))

    t1 = time.time()
    X_enc3 = transformRC(X, cluster)
    totTime = totTime + ((time.time() - t1) * 1000) #millisec
    print("Elapsed time for transformations via dask = %s sec" % (time.time() - t1))

    filename = "Tab3_T3_dask.dat"
    avgTime = round((totTime/3)/1000, 1) #sec
    with open(filename, "w") as file:
        file.write(str(avgTime))

