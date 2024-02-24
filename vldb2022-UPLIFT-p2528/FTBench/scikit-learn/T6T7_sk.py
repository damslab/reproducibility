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

def readNprep(scaleFactor=1):
    # Read,isolate target and combine training and test data
    train = pd.read_csv("../../datasets/crypto.csv", delimiter=",", header=None)
    crypto = train.iloc[1:,:] #remove header
    # Replace infinites and NaNs with before/after entries
    crypto.replace([np.inf, -np.inf], np.nan, inplace=True)
    crypto.fillna(method='pad', inplace=True)
    crypto.fillna(method='bfill', inplace=True)
    # Augment by repeating
    trainList = [crypto for i in range(1, scaleFactor+1)]
    crypto = pd.concat(trainList, ignore_index=True)
    print(crypto.head())
    print(crypto.info())
    # This dataset has 1956782 distinct minute timestamps
    return crypto 


# Arguments 1 and 2 executes T6 and T7 respectively
X = readNprep(scaleFactor=2)
specId = int(sys.argv[1])

X_c1 = X.copy(deep=True)
if specId == 1:
  # spec1: Binning, equi-width, large #numbins
  specfile = "crypto_spec1.json"
  resfile = "crypto_s1_sk.dat"
if specId == 2:
  # spec2: Binning, equi-height, large #numbins
  specfile = "crypto_spec2.json"
  resfile = "crypto_s2_sk.dat"

X_prep = transformFUnion(X_c1, specfile, resfile)

