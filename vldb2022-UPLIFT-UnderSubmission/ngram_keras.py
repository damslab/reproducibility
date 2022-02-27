import sys
import time
import os
import string
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras import layers
import scipy as sp
from scipy.sparse import csr_matrix
import pandas as pd
import math
from itertools import cycle, chain
import warnings

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


def getLayers(abstract_list):
    text_dataset = tf.data.Dataset.from_tensor_slices(abstract_list)
    vectorize_layer = tf.keras.layers.TextVectorization(
            standardize='lower_and_strip_punctuation',
            split='whitespace',
            output_mode='count',
            ngrams=3,
            sparse=True)
    t1 = time.time()
    # Adapt tokenize, n-gram and build the vocab with distinct tokens
    vectorize_layer.adapt(text_dataset.batch(64)) #vocab size ~25M 
    print("TextVectorization adapt takes: %s sec" % (time.time() - t1))
    model = tf.keras.models.Sequential()
    model.add(tf.keras.Input(shape=(1,), dtype=tf.string))
    model.add(vectorize_layer)
    return model

#RuntimeError: Detected a call to `Model.predict` inside a `tf.function`. 
#`Model.predict is a high-level endpoint that manages its own `tf.function`. 
#Please move the call to `Model.predict` outside of all enclosing `tf.function`s. 
#@tf.function
def transform(model, abstract_list):
    bow = model.predict(abstract_list)
    print(bow.shape)
    print(bow)


timeres = np.zeros(3)
for i in range(1):
    t1 = time.time()
    abstracts = readNprep()
    model = getLayers(abstracts)
    transform(model, abstracts)
    timeres[i] = timeres[i] + ((time.time() - t1) * 1000) #millisec

print("Elapsed time for transformations using tf-keras")
print(timeres)
#np.savetxt("./results/bagfwords_keras.dat", timeres, delimiter="\t", fmt='%f')

