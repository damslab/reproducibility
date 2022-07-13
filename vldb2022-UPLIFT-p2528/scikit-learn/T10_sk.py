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
    with open(os.path.join('/home/aphani/datasets/', 'AminerCitation_small.txt'), 'r') as f:
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
bfw = getBagOfWords(abstract_list)
print("Elapsed time for bag-of-words using sklearn = %s sec" % (time.time() - t1))
print(bfw.shape)

