import sys
import time
import numpy as np
import scipy as sp
from scipy.sparse import csr_matrix
import pandas as pd
import math
import warnings
import dask.dataframe as ddf
from dask.dataframe import from_pandas
from dask_ml.preprocessing import Categorizer, OrdinalEncoder, OneHotEncoder, StandardScaler
from dask.distributed import Client, LocalCluster
from sklearn.pipeline import make_pipeline
from sklearn.pipeline import Pipeline, FeatureUnion

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
warnings.filterwarnings('ignore') #cleaner, but not recommended

def readNprep():
    # Read and isolate target and training data
    kdd = pd.read_csv("~/datasets/KDD98.csv", delimiter=",", header=None)
    print(kdd.head())
    print(kdd.shape)
    kddX = kdd.iloc[:,0:469]
    kddX = kddX.drop([0], axis=0)
    kddX = kddX.replace(r'\s+',np.nan,regex=True).replace('',np.nan)
    # Replace NAs with before/after entries
    kddX = kddX.fillna(method="ffill").fillna(method="bfill")

    # Cast categorical columns to str, 
    #st = [23,24,*range(28,42),195,196,197,*range(362,384),*range(412,434)]
    #kddX[st] = kddX[st].astype(str)

    # Set dtype float for numeric columns
    # The default dtype for all columns is object at this point 
    fl = [4,7,16,26,*range(43,50),53,*range(75,195),*range(198,361),407,409,410,411,*range(434,469)]
    kddX[fl] = kddX[fl].astype(float)
    cat = kddX.select_dtypes(exclude=np.float).columns
    kddX[cat] = kddX[cat].astype(str)
    print(kddX.info())

    t1 = time.time()
    pd_num = kddX.select_dtypes(include=np.float)
    pd_bin = pd_num.apply(pd.cut, bins=10)
    print(pd_bin.head())
    print("Elapsed time for transformations via pandas = %s sec" % (time.time() - t1))

    kdd_ddf = ddf.from_pandas(kddX, npartitions=32)
    kdd_cat = kddX.select_dtypes(exclude=np.float)
    cat_ddf = ddf.from_pandas(kdd_cat, npartitions=32)
    #print(kdd_ddf.head())
    print(kdd_ddf.info())
    return kdd_ddf, cat_ddf

def transform(X, X_cat):
    # Use Dask Distributed (local) scheduler
    cluster = LocalCluster()
    print(cluster)
    X_cat_df = X_cat.persist().compute()
    t1 = time.time()
    # NOTE: dask binning is 30x slower than pd cut
    with Client(cluster) as client:
        numeric = X.select_dtypes(include=np.float)
        X_bin = numeric.apply(pd.cut, axis=1, args=(10,)).compute() #binning
        #X_cat = X.select_dtypes(exclude=['float64'])
        pipe = make_pipeline(
                Categorizer(), #build phase
                OneHotEncoder(), #onehot
                StandardScaler()) #scale
        trn = pipe.fit_transform(X_cat_df)
    print("Elapsed time for transformations via dask = %s sec" % (time.time() - t1))
    print(X_bin.head())
    return trn


if __name__ == '__main__':
    X, X_cat = readNprep()
    X_enc1 = transform(X, X_cat)
    X_enc2 = transform(X, X_cat)
    X_enc3 = transform(X, X_cat)

