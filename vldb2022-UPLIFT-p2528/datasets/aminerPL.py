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

def tokenizeLine(abstract, sentence):
    rows = []
    # Remove puncuations
    abstract = abstract.translate(str.maketrans('', '', string.punctuation))
    # Tokenize
    tokens = nltk.word_tokenize(abstract)
    # Calculate n-grams
    unitokens = [token.lower() for token in tokens if len(token) > 1] #unigram
    bitokens = list(bigrams(unitokens))
    tritokens = list(trigrams(unitokens))
    for item in sorted(set(unitokens)):
        count = unitokens.count(item)
        if count == 0:
            continue
        rows.append((item, sentence, count))
    for item in sorted(set(bitokens)):
        count = bitokens.count(item)
        if count == 0:
            continue
        rows.append((item, sentence, count))
    for item in sorted(set(tritokens)):
        count = tritokens.count(item)
        if count == 0:
            continue
        rows.append((item, sentence, count))

    # Concurrent append to the output file
    writeCSV(rows)
    return

def writeCSV(tokenlist):
    with open('AminerAbstract.csv', 'a') as out:
        csv_out = csv.writer(out)
        csv_out.writerows(tokenlist)

def readNprep():
    # For each enatry, separate the abstract, clean and tokenize
    with open('AminerCitation_small.txt', 'r') as f:
        dict_list = []
        c_dict = {}
        abslist = []
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
                abslist.append((abstract, sentence))
            sentence = sentence + 1

    # Use all physical cores to tokenize and write to disk
    print("Number of abstracts to process: ",len(abslist))
    _= Parallel(n_jobs=16, verbose=1)(delayed(tokenizeLine)(abstract,sentence) for abstract,sentence in abslist)
    return 

#os.remove("AminerAbstract.csv")
t1 = time.time()
readNprep()
print("Elapsed time for Aminar dataset prep for T10 = %s sec" % (time.time() - t1))


