# User guide: This script generate a integer/float/string matrix with
# passed number of rows and distinct values in each column.
# The number of columns can be tuned by the numCol variable.
# The output is cast to string as the use of the script is to pass
# it through recoding and dummycoding transformations.
#
# python dataGen.py #rows #distinct
import sys
import time
import math
import warnings
import string
import random
from random import choice
import numpy as np
import pandas as pd

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
warnings.filterwarnings('ignore') #cleaner, but not recommended

def getDataInt():
    # Read the number of rows and distinct values in each column
    rows = int(sys.argv[1]) 
    distinct = int(sys.argv[2]) 
    numCol =5 
    # Derive the ranges for all the columns (fixed lower bounds)
    ranges = np.array([[10,10+distinct]])
    for i in range(1, numCol):
        start = 10 + (i * 100)
        ranges = np.concatenate((ranges, np.array([[start,start+distinct]])), axis=0)
    # Generate a matrix
    data = np.random.randint(low=ranges[:,0], high=ranges[:,1], size=(rows,ranges.shape[0]))
    X = pd.DataFrame(data).astype(str) #convert to string
    return X

def getDataFloat():
    # Read the number of rows and distinct values in each column
    rows = int(sys.argv[1]) 
    distinct = int(sys.argv[2]) 
    numCol = 100 
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


def getDataString():
    # Read the number of rows and distinct values in each column
    rows = int(sys.argv[1]) 
    distinct = int(sys.argv[2]) 
    numChar = int(sys.argv[3])    #num of chars in each cell
    numCol = 10 
    strs = list()

    # Generate all distinct strings for all the columns
    totDist = distinct * numCol
    for i in range(totDist):
        entry = "".join(random.choices(string.ascii_letters+string.digits, k=numChar))
        strs.append(entry)
    distVals = np.array(strs)
    distVals = np.resize(distVals, [distinct, numCol])

    # allocate the output matrix at once
    dt = '<U' + str(numChar) # <U#numchar
    distData = np.zeros([rows, numCol], dtype=dt) 
    rem = math.floor((rows - distinct) / distinct)
    for i in range(rem+1):
        rl = i * distinct
        ru = rl + distinct
        distData[rl:ru,] = distVals

    # rbind in a loop till the required number of rows
    #rem = math.floor((rows - distinct) / distinct)
    #distData = distVals
    #for i in range(rem):
    #    distData = np.concatenate((distData, distVals), axis=0)


    # Shuffle each column
    np.random.shuffle(distData)
    X = pd.DataFrame(distData)
    return X


#X = getDataInt()
X = getDataFloat()
#X = getDataString()

# Write to csv
#print(X)
X.to_csv('data.csv', index=False, header=False)

