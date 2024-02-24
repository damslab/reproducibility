# Usage: python dataGen.py #rows #distinct 
import sys
import time
import math
import warnings
import string
import random
import os
import numpy as np
import pandas as pd
from joblib import Parallel, delayed

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
warnings.filterwarnings('ignore') #cleaner, but not recommended

def getDataFloat():
    # Read the number of rows and distinct values in each column
    rows = int(sys.argv[1]) 
    distinct = int(sys.argv[2]) 
    numCol = 50
    distVals = np.random.uniform(low=1, high=100, size=(distinct, numCol))

    # rbind in a loop till the required number of rows
    rem = math.floor((rows - distinct) / distinct)
    distData = distVals
    for i in range(rem):
        distData = np.concatenate((distData, distVals), axis=0)

    # Shuffle each column
    if rows != distinct:
        np.random.shuffle(distData)
    X = pd.DataFrame(distData).astype(str) #convert to string
    X = pd.DataFrame(distData)
    return X


X = getDataFloat()

# Write to csv
X.to_csv('data1.csv', index=False, header=False)

