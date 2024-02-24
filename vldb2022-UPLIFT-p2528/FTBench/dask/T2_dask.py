import sys
import time
import numpy as np
import pandas as pd
import math
import warnings
import dask
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
    kdd = pd.read_csv("../../datasets/KDD98.csv", delimiter=",", header=None)
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
    cat = kddX.select_dtypes(exclude=np.float64).columns
    kddX[cat] = kddX[cat].astype(str)
    print(kddX.info())

    # Dask fails to convert large Pandas df to dask df via from_pandas
    # Workaround: Write Pandas df to disk, read from disk via dask
    kdd_num = kddX.select_dtypes(include=np.float64)
    #kdd_ddf = ddf.from_pandas(kddX, npartitions=32)
    kdd_num.to_csv("kdd_num")
    kdd_cat = kddX.select_dtypes(exclude=np.float64)
    #cat_ddf = ddf.from_pandas(kdd_cat, npartitions=32)
    kdd_cat.to_csv("kdd_cat")

    # Read the dataframes via dask API
    num_ddf = ddf.read_csv("kdd_num", dtype=float)
    print(num_ddf.head())
    cat_ddf = ddf.read_csv("kdd_cat", dtype=str)
    print(cat_ddf.head())
    print(num_ddf.info())
    return num_ddf, cat_ddf

def transform(cluster, X_num, X_cat):
    X_cat_df = X_cat.persist().compute()
    t1 = time.time()
    # NOTE: dask binning is 30x slower than pd cut
    with Client(cluster) as client:
        X_bin = X_num.apply(pd.cut, axis=1, args=(10,)).compute() #binning
        pipe = make_pipeline(
                Categorizer(), #build phase
                OrdinalEncoder(), #recoding
                StandardScaler()) #scale
        trn = pipe.fit_transform(X_cat_df)
    print(X_bin.head())
    print(trn.head())
    return (time.time() - t1) * 1000


if __name__ == '__main__':
    X_num, X_cat = readNprep()
    # Use Dask Distributed (local) scheduler
    cluster = LocalCluster()
    print(cluster)

    totTime = 0
    timeVal = transform(cluster, X_num, X_cat)
    totTime = totTime + timeVal
    print("Elapsed time for transformations via dask = %s msec" % timeVal)
    timeVal = transform(cluster, X_num, X_cat)
    totTime = totTime + timeVal
    print("Elapsed time for transformations via dask = %s msec" % timeVal)
    timeVal = transform(cluster, X_num, X_cat)
    totTime = totTime + timeVal
    print("Elapsed time for transformations via dask = %s msec" % timeVal)

    filename = "Tab3_T2_dask.dat"
    avgTime = round((totTime/3)/1000, 1) #sec
    with open(filename, "w") as file:
        file.write(str(avgTime))

