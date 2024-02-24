import sys
import time
import os
import string
import numpy as np
import pandas as pd
import math
import warnings
from transformUtils import transformFUnion
from itertools import cycle, chain
from sklearn.feature_extraction.text import CountVectorizer

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
warnings.filterwarnings('ignore') #cleaner, but not recommended

def readNprep():
    # For each enatry, separate the abstract, clean and tokenize
    with open(os.path.join('../../datasets/', 'AminerCitation_small.txt'), 'r') as f:
        abstract_list = []
        c_dict = {}
        sentence = 1;
        for i, line in enumerate(f):
            c_line = line.strip()[1:].strip()
            # Filter out the non-abstract fields
            if len(c_line)<1:
                continue
            if c_line[0] != '!':
                continue
            else:
                # Separate the abstract
                abstract = c_line.strip('!')
                # Remove puncuations
                abstract = abstract.translate(str.maketrans('', '', string.punctuation))
                abstract_list.append(abstract)

    return abstract_list

def getBagOfWords(abstract_list):
    cVect = CountVectorizer(ngram_range = (1, 3), lowercase=True)
    bagfwords = cVect.fit_transform(abstract_list)
    return bagfwords
 

t1 = time.time()
abstract_list = readNprep()
prep_time = time.time() - t1
print("Elapsed time for preparation = %s sec" % prep_time)
timeres = np.zeros(3)
for i in range(3):
    t2 = time.time()
    bfw = getBagOfWords(abstract_list)
    timeres[i] = timeres[i] + ((time.time() - t2) * 1000) #millisec
print("Elapsed time for transformations using FeatureUnion in millsec")
print(timeres)
print(bfw.shape)
resfile = "bagfwords_sk.dat"
np.savetxt(resfile, timeres, delimiter="\t", fmt='%f')

