import sys
import time
import numpy as np
import pandas as pd
import math
import warnings
from transformUtils import transformFUnion

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
warnings.filterwarnings('ignore') #cleaner, but not recommended

def readNprep():
    # Read,isolate target and combine training and test data
    train = pd.read_csv("../../datasets/homeCreditTrain.csv", delimiter=",", header=None)
    test = pd.read_csv("../../datasets/homeCreditTest.csv", delimiter=",", header=None)
    train = train.iloc[1:,:] #remove header
    train.drop(1, axis=1, inplace=True); #remove target
    train.columns = [*range(0,121)] #rename header from 0 to 120
    test = test.iloc[1:,:]
    home = pd.concat([train, test])
    # Replace NaNs with before/after entries
    home.fillna(method='pad', inplace=True)
    home.fillna(method='bfill', inplace=True)
    print(home.head())
    print(home.info())
    return home


X = readNprep()

X_c = X.copy(deep=True)
t1 = time.time()
X_prep = transformFUnion(X_c, "homecredit_spec1.json", "homecredit_sk.dat")
#print(X_prep.toarray()[:5, :]) #print first 5 rows
print("Elapsed time for transformations using FeatureUnion = %s sec" % (time.time() - t1))

