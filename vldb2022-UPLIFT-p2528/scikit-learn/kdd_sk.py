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
    kdd = pd.read_csv("~/datasets/KDD98.csv", delimiter=",", header=None)
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

def transform(kddX):
    # Seperate out the numeric inputs
    numeric = kddX.select_dtypes(include=np.float)

    # Concatenate the numeric inputs together and 
    # run them through normalization, binning + one_hot layers 
    norm = preprocessing.Normalizer(norm='l2').fit_transform(numeric)
    one_hot_bin = preprocessing.KBinsDiscretizer(n_bins=10, encode='onehot').fit(norm)
    binned = one_hot_bin.transform(norm)
    #print(np.shape(binned))

    # Recode and dummycode the categorical features
    strings = kddX.select_dtypes(exclude=np.float).astype(str)
    one_hot = preprocessing.OneHotEncoder().fit(strings)
    encoded = one_hot.transform(strings)
    #print(np.shape(encoded))

    # Column bind. 
    transformed = sp.sparse.hstack([binned, encoded]).toarray()
    print(np.shape(transformed))

    # Return the transformed data
    return transformed 

def transformPipe(kddX):
    # Seperate numeric inputs
    numeric = kddX.select_dtypes(include=np.float)
    # Define numerical pipeline (normalize, binning + one_hot)
    norm = preprocessing.Normalizer(norm='l2')
    one_hot_bin = preprocessing.KBinsDiscretizer(n_bins=10, encode='onehot')
    num_pipe = Pipeline([
            ('normalizer', norm),
            ('biner', one_hot_bin)
    ], verbose=True)
    binned = num_pipe.fit_transform(numeric)

    # Seperate categorical features
    categorical = kddX.select_dtypes(exclude=np.float).astype(str)
    # Define categorical pipeline (one_hot)
    one_hot = preprocessing.OneHotEncoder()
    cat_pipe = Pipeline([
            ('encoder', one_hot),
    ], verbose=True)
    encoded = cat_pipe.fit_transform(categorical) 

    # Column bind. 
    transformed = sp.sparse.hstack([binned, encoded]).toarray()
    print(np.shape(transformed))

    # Return the transformed data
    return transformed 

def transformParPipe(kddX):
    # Seperate numeric inputs
    numeric = list(kddX.select_dtypes(include=np.float).columns)
    # Define numerical pipeline (normalize, binning + one_hot)
    norm = preprocessing.Normalizer(norm='l2')
    one_hot_bin = preprocessing.KBinsDiscretizer(n_bins=10, encode='onehot')
    num_pipe = Pipeline([
            ('normalizer', norm),
            ('biner', one_hot_bin)
    ])

    # Seperate categorical features
    categorical = list(kddX.select_dtypes(exclude=np.float).columns)
    # Define categorical pipeline (one_hot)
    one_hot = preprocessing.OneHotEncoder()
    cat_pipe = Pipeline([
            ('encoder', one_hot),
    ])

    # Wrap the pipelines in a ColumnTransformer
    # Note: n_jobs = -1 means 'All CPUs'
    preprocessor = ColumnTransformer([
            ('num', num_pipe, numeric),
            ('cat', cat_pipe, categorical)
    ], n_jobs=1, verbose=True)

    # Apply the transformations (concurrently) on the dataset
    preprocessor.fit(kddX)
    transformed = preprocessor.transform(kddX).toarray()
    print(np.shape(transformed))

    # Return the transformed data
    return transformed 


# Define custom transformer for FeatureUnion
class ColumnSelector(BaseEstimator, TransformerMixin):
    """Select only specified columns."""
    def __init__(self, columns):
        self.columns = columns
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X[self.columns]

def transformFUnion_backup(kddX):
    # Seperate numeric inputs
    numeric = list(kddX.select_dtypes(include=np.float).columns)
    # Define numerical pipeline (normalize, binning + one_hot)
    norm = preprocessing.Normalizer(norm='l2')
    one_hot_bin = preprocessing.KBinsDiscretizer(n_bins=10, encode='onehot')
    num_pipe = Pipeline([
            ('selector', ColumnSelector(numeric)),
            ('normalizer', norm),
            ('biner', one_hot_bin)
    ])

    # Seperate categorical features
    categorical = list(kddX.select_dtypes(exclude=np.float).columns)
    # Define categorical pipeline (one_hot)
    one_hot = preprocessing.OneHotEncoder()
    cat_pipe = Pipeline([
            ('selector', ColumnSelector(categorical)),
            ('encoder', one_hot),
    ])

    # Wrap the pipelines in a FeatureUnion 
    # Note: n_jobs = -1 means 'All CPUs'
    preprocessor = FeatureUnion([
            ('num', num_pipe),
            ('cat', cat_pipe)
    ], n_jobs=1, verbose=True)
    preprocessor.fit(kddX)
    transformed = preprocessor.transform(kddX).toarray()
    print(np.shape(transformed))

    # Return the transformed data
    return transformed 



#Xrandom = np.random.uniform(low=0, high=1, size=(100000,1000))
X = readNprep()

#X_c = X.copy(deep=True)
t1 = time.time()
#X_prep = transform(X_c)
#print(X_prep[:5, :]) #print first 5 rows
print("Elapsed time for transformations = %s sec" % (time.time() - t1))

#X_c = X.copy(deep=True)
t1 = time.time()
#X_prep = transformPipe(X_c)
#print(X_prep[:5, :]) #print first 5 rows
print("Elapsed time for transformations using plain pipeline = %s sec" % (time.time() - t1))

#X_c = X.copy(deep=True)
t1 = time.time()
#X_prep = transformParPipe(X_c)
#print(X_prep[:5, :]) #print first 5 rows
print("Elapsed time for transformations using ColumnTransformer = %s sec" % (time.time() - t1))

X_c = X.copy(deep=True)
X_prep = transformFUnion(X_c, "kdd_spec1.json", "kdd_sk.dat", scale=True)

#np.savetxt("X_prep_sk.csv", X_prep, fmt='%1.2f', delimiter=',')
