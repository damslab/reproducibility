import sys
import time
import numpy as np
import scipy as sp
from scipy.sparse import csr_matrix
import scipy
import pandas as pd
import math
import warnings
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction import FeatureHasher
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from transformUtils import transformFUnion

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
warnings.filterwarnings('ignore') #cleaner, but not recommended

def readNprep():
    # Read the dataset
    criteo = pd.read_csv("../../datasets/criteo_day21_5M_cleaned", delimiter=",", header=None)
    print(criteo.head())
    y = criteo.iloc[:, 0]
    y.astype(int)
    #print(criteo.info())
    return criteo, y 

def BinFeaturehash(X):
    pt = [*range(0,14)]
    X[pt] = X[pt].astype(float)
    # Seperate numeric inputs
    t1 = time.time()
    numeric = X.select_dtypes(include=np.float64)
    # Apply numerical pipeline (binning)
    binft = preprocessing.KBinsDiscretizer(n_bins=10, strategy='uniform', encode='ordinal')
    binned = binft.fit_transform(numeric)
    # Seperate categorical features (!floats)
    categorical = X.select_dtypes(exclude=np.float64).astype(str)
    # Apply categorical pipeline
    hasher = FeatureHasher(n_features=1000, input_type='string')
    hashed = hasher.fit_transform(categorical.values)
    print("Elapsed time for Transform = %s sec" % (time.time() - t1))
    return hashed

def applyNaiveBayes(Xdf, ydf):
    data = Xdf[:, 1:]
    X_train, X_test = train_test_split(data, test_size=0.2)
    y_train, y_test = train_test_split(ydf, test_size=0.2)
    gnb = GaussianNB()
    if scipy.sparse.issparse(X_train):
        return
        #X_train = X_train.toarray()
    gnb.fit(X_train, y_train)
    y_nb = gnb.predict(X_test)
    score = accuracy_score(y_test, y_nb)
    print(score)


X, y = readNprep()
timers = np.zeros(6)
ft_time = 0
nb_time = 0
specs = ["criteo_fe1.json","criteo_fe2.json","criteo_fe3.json","criteo_fe4.json","criteo_fe5.json","criteo_fe6.json"]
for i in range(len(specs)):
    spec = specs[i]
    print("Starting transformation")
    if (spec == "criteo_fe3.json" or spec == "criteo_fe5.json"):
        t1 = time.time()
        X_trn = BinFeaturehash(X)
        ft_time = ft_time + ((time.time() - t1) * 1000) #millisec
    else:
        t1 = time.time()
        X_trn = transformFUnion(X, spec, resultfile="tmp", save=False)
        ft_time = ft_time + ((time.time() - t1) * 1000) #millisec
        t2 = time.time()
        score = applyNaiveBayes(X_trn, y)
        nb_time = nb_time + ((time.time() - t2) * 1000) #millisec

timers[:3] = ft_time
timers[3:] = nb_time
resfile = "featureeng_sk.dat"
np.savetxt(resfile, timers, delimiter="\t", fmt='%f')
print(timers)

