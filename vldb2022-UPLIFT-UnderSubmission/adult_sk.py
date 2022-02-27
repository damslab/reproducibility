import sys
import time
import json
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
    adult = pd.read_csv("~/datasets/adult.data", delimiter=",", header=None)
    print(adult.head())

    # Pandas infer the type of a few columns as int64.
    # SystemDS reads those as STRINGS and apply passthrough FT on those.
    # For a fair comparision, convert those here to str and later back to float
    pt = [*range(0,15)]
    adult[pt] = adult[pt].astype(str)
    #print(adult.info())
    return adult 

def getSpec(X):
    pt, cat, bins = getTransformSpec(X, "adult_spec2.json")
    print(cat)
    print(pt)
    print(bins)

def transformPipe(X):
    # Passthrough transformation -- convert to float
    pt = [0, 2, 4, 10, 11, 12]
    X[pt] = X[pt].astype(float)

    # Seperate numeric inputs
    numeric = X.select_dtypes(include=np.float)
    # Binning followed by DC for numeric inputs
    one_hot_bin = preprocessing.KBinsDiscretizer(n_bins=5, strategy='uniform', encode='onehot')
    num_pipe = Pipeline([
            ('binner', one_hot_bin)
    ], verbose=True)
    binned = num_pipe.fit_transform(numeric)

    # Seperate categorical features
    categorical = X.select_dtypes(exclude=np.float).astype(str)
    # Define categorical pipeline (one_hot)
    one_hot = preprocessing.OneHotEncoder()
    cat_pipe = Pipeline([
            ('encoder', one_hot),
    ], verbose=True)
    encoded = cat_pipe.fit_transform(categorical) 

    # Column bind. 
    transformed = sp.sparse.hstack([binned, encoded])
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

def transformFUnion_backup(X):
    # Passh through transformation -- convert to float
    pt = [0, 2, 4, 10, 11, 12]
    X[pt] = X[pt].astype(float)

    # Seperate numeric inputs
    numeric = list(X.select_dtypes(include=np.float).columns)
    # Binning followed by DC for numeric inputs
    one_hot_bin = preprocessing.KBinsDiscretizer(n_bins=5, strategy='uniform', encode='onehot')
    num_pipe = Pipeline([
            ('selector', ColumnSelector(numeric)),
            ('biner', one_hot_bin)
    ])

    # Seperate categorical features (not floats)
    categorical = list(X.select_dtypes(exclude=np.float).columns)
    # Define categorical pipeline (one_hot)
    one_hot = preprocessing.OneHotEncoder()
    cat_pipe = Pipeline([
            ('selector', ColumnSelector(categorical)),
            ('encoder', one_hot),
    ])

    # Wrap the pipelines in a FeatureUnion 
    # Note: n_jobs = -1 means 'All CPUs'
    # FIXME: hangs with n_jobs = -1
    preprocessor = FeatureUnion([
            ('num', num_pipe),
            ('cat', cat_pipe)
    ], n_jobs=1, verbose=True)
    preprocessor.fit(X)
    transformed = preprocessor.transform(X) #sparse
    print(np.shape(transformed))

    # Return the transformed data
    return transformed 



X = readNprep()

X_c = X.copy(deep=True)
t1 = time.time()
X_prep = transformPipe(X_c)
print("Elapsed time for transformations using plain pipeline = %s sec" % (time.time() - t1))

X_c = X.copy(deep=True)
t1 = time.time()
X_prep = transformFUnion(X_c, "adult_spec2.json", "adult_sk.dat")
#print(X_prep.toarray()[:5, :]) #print first 5 rows
print("Elapsed time for transformations using FeatureUnion = %s sec" % (time.time() - t1))

#np.savetxt("X_prep_sk.csv", X_prep, fmt='%1.2f', delimiter=',') #dense
#sp.sparse.save_npz("X_prep_sk.npz", X_prep)  #sparse

