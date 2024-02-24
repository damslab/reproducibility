import sys
import numpy as np
import pandas as pd
import time
import scipy as sp
from scipy.sparse import csr_matrix
import math
import warnings
import string
from random import choice
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import preprocessing

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
warnings.filterwarnings('ignore') #cleaner, but not recommended

def readNprep():
    data1 = pd.read_csv("../datasets/data1.csv", delimiter=",", header=None)
    data2 = pd.read_csv("../datasets/data2.csv", delimiter=",", header=None)
    X = pd.concat([data1, data2], axis=1, ignore_index=True)
    num = [*range(0,50)]
    X[num] = X[num].astype(float)
    X = X.iloc[0:100000]
    print(X.head())
    #print(X.info())
    return X

# Define custom transformer for FeatureUnion
class ColumnSelector(BaseEstimator, TransformerMixin):
    """Select only specified columns."""
    def __init__(self, columns):
        self.columns = columns
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X[self.columns]

def transformFUnion(X):
    # Seperate out the numeric inputs
    numeric = list(X.select_dtypes(include=np.float).columns)
    # Define numerical pipeline (binning)
    binn = preprocessing.KBinsDiscretizer(n_bins=10, strategy='uniform', encode='ordinal')
    num_pipe = Pipeline([
            ('selector', ColumnSelector(numeric)),
            ('biner', binn)
    ])
    # Define categorical pipeline (ordinal/one_hot)
    categorical = list(X.select_dtypes(exclude=np.float).columns)
    # Define categorical pipeline (recoding)
    catenc = preprocessing.OrdinalEncoder()
    cat_pipe = Pipeline([
            ('selector', ColumnSelector(categorical)),
            ('encoder', catenc),
    ])

    # Wrap the pipelines in a FeatureUnion 
    # Note: n_jobs = -1 means 'All CPUs'
    preprocessor = FeatureUnion([
            ('num', num_pipe),
            ('cat', cat_pipe)
    ], n_jobs=1, verbose=True)
    preprocessor.fit(X)

    # Return the model after fit
    return preprocessor

def batch_apply(X_batch, prepro):
    transformed = prepro.transform(X_batch)
    return transformed


X = readNprep()
timeres = np.zeros(1)

t1 = time.time()
prepro = transformFUnion(X)
timeres = timeres + ((time.time() - t1) * 1000) #millisec
bs = 1024;
ep = 5;
nrow = X.shape[0]
iter_ep = math.ceil(nrow/bs);
maxiter = ep * iter_ep;
print("Total number of iterations: %d" % maxiter) 
beg = 0;
iter = 0;
while iter < maxiter:
    end = beg + bs
    if end > nrow:
        end = nrow
    X_batch = X.iloc[beg:end]
    t1 = time.time()
    X_batch_en = batch_apply(X_batch, prepro)
    timeres = timeres + ((time.time() - t1) * 1000) #millisec
    iter = iter + 1
    if end == nrow:
        beg = 0
        print("Starting next epoch")
    else:
        beg = end

print(X_batch_en.shape)
print("Elapsed time for transformations using FeatureUnion in millsec")
print(timeres)

