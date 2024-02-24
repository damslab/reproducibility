import sys
import time
import numpy as np
import pandas as pd
import math
import warnings
import sklearn
from sklearn.feature_extraction import FeatureHasher
from transformUtils import transformFUnion

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
warnings.filterwarnings('ignore') #cleaner, but not recommended

def readNprep(scaleFactor=1):
    # Read,isolate target and combine training and test data
    train = pd.read_csv("../../datasets/catindattrain.csv", delimiter=",", header=None)
    train = train.iloc[1:,:] #remove header
    train.drop(24, axis=1, inplace=True); #remove target
    # Augment by repeating
    trainList = [train for i in range(1, scaleFactor+1)]
    catindat = pd.concat(trainList, ignore_index=True)
    print(catindat.head())
    print(catindat.info())
    return catindat 

def featureHashing(X, ncol, resultfile):
    timeres = np.zeros(3)
    # ncol is #cols in the output. Best case is sum(#distinct of all cols)
    hasher = FeatureHasher(n_features=ncol, input_type='string')
    print(hasher)
    X_str = X.astype(str)
    # Run fit_transform 3 times and record time
    for i in range(3):
        t1 = time.time()
        transformed = hasher.fit_transform(X_str.values)
        timeres[i] = timeres[i] + ((time.time() - t1) * 1000) #millisec

    print(np.shape(transformed))
    print("Elapsed time for transformations using FeatureUnion in millsec")
    print(timeres)
    resfile = resultfile
    np.savetxt(resfile, timeres, delimiter="\t", fmt='%f')
    return transformed

X = readNprep(scaleFactor=10)
X_prep = featureHashing(X, 24000, "catindat_sk.dat") #spec3

res = pd.read_csv("catindat_sk.dat", header=None)
avg = res.mean().squeeze()
avgTime = round(avg/1000, 1) #sec
filename = "Tab3_T9_sk.dat"
with open(filename, "w") as file:
    file.write(str(avgTime))
