# User guide: This script generate a integer/float/string matrix with
# passed number of rows and distinct values in each column and string length.
# The number of columns can be tuned by the numCol variable.
# The output is cast to string as the use of the script is to pass
# it through recoding and dummycoding transformations.
#
# python dataGen.py #rows #distinct stringlen
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

def partGenDataString(numrows, numcols, numdist, numchar):
    # Generate random strings for a column
    strs = list()
    totDist = numdist * numcols
    for i in range(totDist):
        entry = "".join(random.choices(string.ascii_letters+string.digits, k=numchar))
        strs.append(entry)
    distVals = np.array(strs)
    distVals = np.resize(distVals, [numdist, numcols])

    # allocate the output matrix at once
    dt = '<U' + str(numchar) # <U#numchar
    #distData = np.zeros([numrows, numcols], dtype="<U5") #U5 = U#numChar
    distData = np.zeros([numrows, numcols], dtype=dt) 
    rem = math.floor((numrows - numdist) / numdist)
    for i in range(rem+1):
        rl = i * numdist 
        ru = rl + numdist
        distData[rl:ru,] = distVals

    # Shuffle
    np.random.shuffle(distData)
    # Remove empty rows, if any
    X_part = pd.DataFrame(distData)
    X_part.replace('', np.nan, inplace=True)
    X_part.dropna(inplace=True)
    # Append the partition to the output file
    X_part.to_csv('data.csv', mode='a', index=False, header=False)
    return 


def getDataString():
    # Read the number of rows and distinct values in each column
    # NOTE: #distinct shoule be more than #thread
    rows = int(sys.argv[1]) 
    distinct = int(sys.argv[2]) 
    numChar = int(sys.argv[3])    #num of chars in each cell
    numCol = 100 
    numthread = 16;
    if distinct > rows:
        distinct = rows
    # Remove the old file
    filename = "/home/aphani/vldb_22/data.csv"
    if os.path.exists(filename):
        os.remove(filename)

    # Multithreaded data generation
    blkrow = math.ceil(rows/numthread)
    blkdist = math.ceil(distinct/numthread)
    #seedStart = [*range(1, distinct*numCol, blkdist*numCol)]
    blklist = [(blkrow,blkdist)] * numthread
    _ = Parallel(n_jobs=numthread, verbose=1
            )(delayed(partGenDataString)(
                    blkr,
                    numCol,
                    blkd,
                    numChar
                    ) for blkr,blkd in blklist)
    return


#X = getDataInt()
#X = getDataFloat()
getDataString()

# Write to csv
#print(X)
#X.to_csv('data.csv', index=False, header=False)

