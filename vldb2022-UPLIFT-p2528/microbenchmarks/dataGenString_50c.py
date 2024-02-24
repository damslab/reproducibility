# User guide: This script generate a string csv file with
# passed number of rows, distinct values in each column and string length.
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
    X_part.to_csv('data2.csv', mode='a', index=False, header=False)
    return 


def getDataString():
    # Read the number of rows and distinct values in each column
    # NOTE: #distinct shoule be more than #thread
    rows = int(sys.argv[1]) 
    distinct = int(sys.argv[2]) 
    numChar = int(sys.argv[3])    #num of chars in each cell
    numCol = 50 
    numthread = 16
    if distinct > rows:
        distinct = rows
    # Remove the old file
    filename = "data2.csv"
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


getDataString()

