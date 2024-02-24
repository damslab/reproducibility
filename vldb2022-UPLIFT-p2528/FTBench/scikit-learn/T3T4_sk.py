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
    # Read the dataset
    print("Reading file: criteo_day21_10M")
    criteo = pd.read_csv("../../datasets/criteo_day21_10M", delimiter=",", header=None)
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


# Arguments 1 and 2 executes T3 and T4 respectively
specId = int(sys.argv[1])
if specId == 1:
  specfile = "criteo_spec1.json"
if specId == 2:
  specfile = "criteo_spec2.json"
if specId == 1:
  resfile = "criteo10M_s1_sk.dat"
if specId == 2:
  resfile = "criteo10M_s2_sk.dat"
print(resfile)
X = readNprep()

X_c = X.copy(deep=True)
t1 = time.time()
#X_prep = transformPipe(X_c)
print("Elapsed time for transformations using plain pipeline = %s sec" % (time.time() - t1))

X_c = X.copy(deep=True)
t2 = time.time()
if specId == 1:
    X_prep = transformFUnion(X_c, specfile, resfile)
    res = pd.read_csv(resfile, header=None)
    avg = res.mean().squeeze()
    avgTime = round(avg/1000, 1) #sec
    filename = "Tab3_T3_sk.dat"
    with open(filename, "w") as file:
        file.write(str(avgTime))
if specId == 2:
    X_prep = transformFUnion(X_c, specfile, resfile, scale=True)
print("Elapsed time for transformations using FeatureUnion = %s sec" % (time.time() - t2))

