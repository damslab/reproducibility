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
from transformUtils import transformFUnion

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
warnings.filterwarnings('ignore') #cleaner, but not recommended

def readNprep():
    # Read and isolate target and training data
    kdd = pd.read_csv("../../datasets/KDD98.csv", delimiter=",", header=None)
    print(kdd.head())
    kddX = kdd.iloc[:,0:469]
    kddX = kddX.drop([0], axis=0)
    kddX = kddX.replace(r'\s+',np.nan,regex=True).replace('',np.nan)
    # Replace NAs with before/after entries
    kddX.fillna(method='pad', inplace=True)
    kddX.fillna(method='bfill', inplace=True)

    # Cast categorical columns that have numbers to float first, 
    # to avoid mix of int and float type strings (5, 5.0), which
    # increases # distinct values in a column
    st = [23,24,*range(28,42),195,196,197,*range(362,384),*range(412,434)]
    kddX[st] = kddX[st].astype(float).astype(str)

    # Set dtype float for numeric columns
    # The default dtype for all columns is object at this point 
    #fl = [4,7,16,26,*range(43,50),53,*range(75,195),*range(198,361),407,409,410,411,*range(434,469)]
    #kddX[fl] = kddX[fl].astype(float)
    #cat = kddX.select_dtypes(exclude=np.float).columns
    #kddX[cat] = kddX[cat].astype(str)
    print(kddX.info())
    return kddX

X = readNprep()
X_prep = transformFUnion(X, "kdd_spec1.json", "kdd_sk.dat", scale=True)

res = pd.read_csv("kdd_sk.dat", header=None)
avg = res.mean().squeeze()
avgTime = round(avg/1000, 1) #sec
filename = "Tab3_T2_sk.dat"
with open(filename, "w") as file:
    file.write(str(avgTime))
