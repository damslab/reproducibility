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

def readNprep():
    # Read the dataset
    adult = pd.read_csv("../../datasets/adult.data", delimiter=",", header=None)
    print(adult.head())
    print(adult.info())
    adult_ddf = ddf.from_pandas(adult, npartitions=32)
    adult_cat = adult.select_dtypes(exclude=['int'])
    cat_ddf = ddf.from_pandas(adult_cat, npartitions=32)
    return adult_ddf, cat_ddf

def transform(adult, X_cat, cluster):
    X_bin = adult.select_dtypes(include=np.float64)
    X_cat_df = X_cat.persist().compute()
    with Client(cluster) as client:
        binned = X_bin.apply(pd.cut, axis=1, args=(10,)).compute() #binning
        pipe = make_pipeline(
                Categorizer(), #build phase
                OneHotEncoder()) #onehot
        trn = pipe.fit_transform(X_cat_df)
    #print(binned.head())
    print(trn.head())
    return trn


if __name__ == '__main__':
    X, X_cat = readNprep()

    timers = np.zeros(3)
    # Use Dask Distributed (local) scheduler
    cluster = LocalCluster()
    print(cluster)

    t1 = time.time()
    X_enc1 = transform(X, X_cat, cluster)
    timers[0] = timers[0] + ((time.time() - t1) * 1000) #millisec
    t1 = time.time()
    X_enc2 = transform(X, X_cat, cluster)
    timers[1] = timers[1] + ((time.time() - t1) * 1000) #millisec
    t1 = time.time()
    X_enc3= transform(X, X_cat, cluster)
    timers[2] = timers[2] + ((time.time() - t1) * 1000) #millisec

    print(timers)
    np.savetxt("adult_dask.dat", timers, delimiter="\t", fmt='%f')
