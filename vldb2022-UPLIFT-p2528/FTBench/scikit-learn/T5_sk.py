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
    # Read and isolate target and training data
    train = pd.read_csv("../../datasets/santander.csv", delimiter=",", header=None)
    santander = train.iloc[1:,2:]
    santander.columns = [*range(0,200)] #rename header from 0 to 199
    print(santander.head())
    print(santander.info())
    return santander


X = readNprep()

X_c2 = X.copy(deep=True)
X_prep = transformFUnion(X_c2, "santander_spec2.json", "santander_sk.dat")



