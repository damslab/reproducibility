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

    # Pandas infer the type of first 14 columns as float and int.
    # SystemDS reads those as STRINGS and apply passthrough FT on those.
    # For a fair comparision, convert those here to str and later back to float
    pt = [*range(0,14)]
    criteo[pt] = criteo[pt].astype(str)

    #print(criteo.info())
    return criteo 

def transformPipe(X):
    # Passh through transformation -- convert to float
    pt = [*range(0,14)]
    X[pt] = X[pt].astype(float)

    # Seperate numeric inputs
    numeric = X.select_dtypes(include=np.float)
    # Define numerical pipeline (binning)
    binft = preprocessing.KBinsDiscretizer(n_bins=10, strategy='uniform', encode='ordinal')
    num_pipe = Pipeline([
            ('biner', binft)
    ], verbose=True)
    enc_num = num_pipe.fit_transform(numeric)

    # Seperate categorical features
    categorical = X.select_dtypes(exclude=np.float).astype(str)
    categorical.fillna('', inplace=True)
    # Define categorical pipeline (recoding)
    recode = preprocessing.OrdinalEncoder()
    cat_pipe = Pipeline([
            ('encoder', recode),
    ], verbose=True)
    enc_cat = cat_pipe.fit_transform(categorical) 

    # Column bind. 
    transformed = np.hstack([enc_num, enc_cat])
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
    pt = [*range(0,14)]
    X[pt] = X[pt].astype(float)

    # Seperate numeric inputs
    numeric = list(X.select_dtypes(include=np.float).columns)

    # Define numerical pipeline (binning)
    binft = preprocessing.KBinsDiscretizer(n_bins=10, strategy='uniform', encode='ordinal')
    num_pipe = Pipeline([
            ('selector', ColumnSelector(numeric)),
            ('biner', binft)
    ])

    # Seperate categorical features (!floats)
    categorical = list(X.select_dtypes(exclude=np.float).columns)
    # Define categorical pipeline (recoding)
    recode = preprocessing.OrdinalEncoder()
    cat_pipe = Pipeline([
            ('selector', ColumnSelector(categorical)),
            ('encoder', recode),
    ])

    # Wrap the pipelines in a FeatureUnion 
    # Note: n_jobs = -1 means 'All CPUs'
    preprocessor = FeatureUnion([
            ('num', num_pipe),
            ('cat', cat_pipe)
    ], n_jobs=1, verbose=True)
    t_f = time.time()
    preprocessor.fit(X)
    print("Elapsed time for Fit = %s sec" % (time.time() - t_f))
    t_t = time.time()
    #encoded = preprocessor.transform(X).toarray()
    transformed = preprocessor.transform(X) #dense
    print("Elapsed time for Transform = %s sec" % (time.time() - t_t))
    print(np.shape(transformed))

    # Return the transformed data
    return transformed 



nRows = int(sys.argv[1])
specId = int(sys.argv[2])
if specId == 1:
  specfile = "criteo_spec1.json"
if specId == 2:
  specfile = "criteo_spec2.json"
if nRows == 1 and specId == 1:
  resfile = "criteo1M_s1_sk.dat"
if nRows == 10 and specId == 1:
  resfile = "criteo10M_s1_sk.dat"
if nRows == 1 and specId == 2:
  resfile = "criteo1M_s2_sk.dat"
if nRows == 10 and specId == 2:
  resfile = "criteo10M_s2_sk.dat"
print(resfile)
X = readNprep(nRows)

X_c = X.copy(deep=True)
t1 = time.time()
#X_prep = transformPipe(X_c)
print("Elapsed time for transformations using plain pipeline = %s sec" % (time.time() - t1))

X_c = X.copy(deep=True)
t2 = time.time()
X_prep = transformFUnion(X_c, specfile, resfile)
print("Elapsed time for transformations using FeatureUnion = %s sec" % (time.time() - t2))
#np.savetxt("X_prep_sk.csv", X_prep, fmt='%1.2f', delimiter=',') #dense
#sp.sparse.save_npz("X_prep_sk.npz", X_prep)  #sparse

