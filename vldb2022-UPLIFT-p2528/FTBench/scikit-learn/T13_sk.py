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
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline as Pipeline_sk
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import preprocessing

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
warnings.filterwarnings('ignore') #cleaner, but not recommended

def readNprep():
    X = pd.read_csv("data.csv", delimiter=",", header=None)
    print(X.head())
    print(X.info())
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
    # Define categorical pipeline (ordinal/one_hot)
    categorical = list(X.columns)
    #catenc = preprocessing.OneHotEncoder()
    catenc = preprocessing.OrdinalEncoder()
    cat_pipe = Pipeline_sk([
            ('selector', ColumnSelector(categorical)),
            ('encoder', catenc),
    ])
    print(cat_pipe)

    # Wrap the pipelines in a FeatureUnion 
    # Note: n_jobs = -1 means 'All CPUs'
    preprocessor = FeatureUnion([
            ('cat', cat_pipe)
    ], n_jobs=1, verbose=True)

    # Run fit_transform 3 times and record time
    timeres = np.zeros(3)
    for i in range(3):
        t1 = time.time()
        transformed = preprocessor.fit_transform(X) 
        timeres[i] = timeres[i] + ((time.time() - t1) * 1000) #millisec
    print(np.shape(transformed))

    print(timeres)
    resultfile = "stringlen_sk.dat"
    resfile = resultfile
    np.savetxt(resfile, timeres, delimiter="\t", fmt='%f')

    # Return the transformed data
    return transformed 


X = readNprep()
X_prep = transformFUnion(X)

