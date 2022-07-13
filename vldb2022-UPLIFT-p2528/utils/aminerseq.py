import os
import string
import numpy as np
import warnings
import pandas as pd
import nltk
import time
import csv
from nltk import bigrams, trigrams
from itertools import cycle, chain
from joblib import Parallel, delayed
from multiprocessing import Manager

#os.system("taskset -p 0xff %d" % os.getpid())
# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
warnings.filterwarnings('ignore') #cleaner, but not recommended

manager = Manager()
#rows = manager.list()
maxTokenCount = 0

def findMaxTokenCount(tokenList):
    global maxTokenCount
    if maxTokenCount < len(tokenList):
        maxTokenCount = len(tokenList)
        print("New max token = ",maxTokenCount)

def tokenizeLine(abstract, maxLen):
    rows = []
    #maxLen = 1000
    # Remove puncuations
    abstract = abstract.translate(str.maketrans('', '', string.punctuation))
    # Tokenize
    tokens = nltk.word_tokenize(abstract)
    # Calculate n-grams
    unitokens = [token.lower() for token in tokens if len(token) > 1] #unigram
    for item in unitokens:
        rows.append([item])

    # If #tokens > maxLen, take first maxLen tokens
    if len(rows) > maxLen:
        rows = rows[0:maxLen-1]

    # If #tokens < maxLen, pad with token 'padword' upto maxLen
    for i in range(len(rows), maxLen):
        rows.append(['padword'])

    #findMaxTokenCount(rows) 
    # Concurrent append to the output file
    writeCSV(rows)
    return

def writeCSV(tokenlist):
    with open('/home/aphani/datasets/AminerAbstractSequence.csv', 'a') as out:
        csv_out = csv.writer(out)
        csv_out.writerows(tokenlist)

# Read K abstracts
def readKAbstracts(K):
    # For each entry, separate the abstract, clean and tokenize
    with open(os.path.join('/home/aphani/datasets/', 'AminerCitation_small.txt'), 'r') as f:
        dict_list = []
        c_dict = {}
        abslist = []
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
                abslist.append(abstract)
                if len(abslist) == K:
                    return abslist
    return abslist

def readNprep():
    # Read 100K abstracts
    abslist = readKAbstracts(100000)
    maxLen = 1000
    # Use all physical cores to tokenize and write to disk
    print("Number of abstracts to process: ",len(abslist))
    _= Parallel(n_jobs=16, verbose=1
            )(delayed(tokenizeLine)(
                    abstract, maxLen) for abstract in abslist)
    return 

os.remove("/home/aphani/datasets/AminerAbstractSequence.csv")
t1 = time.time()
readNprep()
print("Elapsed time for Aminar DS preparing for SystemDS = %s sec" % (time.time() - t1))


