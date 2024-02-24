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
    adult = pd.read_csv("../../datasets/adult.data", delimiter=",", header=None)
    print(adult.head())

    # Pandas infer the type of a few columns as int64.
    # SystemDS reads those as STRINGS and apply passthrough FT on those.
    # For a fair comparision, convert those here to str and later back to float
    pt = [*range(0,15)]
    adult[pt] = adult[pt].astype(str)
    #print(adult.info())
    return adult 

X = readNprep()

t1 = time.time()
X_prep = transformFUnion(X, "adult_spec2.json", "adult_sk.dat")
#print(X_prep.toarray()[:5, :]) #print first 5 rows
print("Elapsed time for transformations using FeatureUnion = %s sec" % (time.time() - t1))

