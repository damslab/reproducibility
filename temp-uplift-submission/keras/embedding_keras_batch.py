import sys
import time
import os
import string
import nltk
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.preprocessing import text
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

# Read count abstracts with #tokens <= 300
def readNprep(count):
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
                tokens = nltk.word_tokenize(abstract)
                #if len(tokens) <= 300:
                #    abstract_list.append(abstract)
                abstract_list.append(abstract)

                if len(abstract_list) == count:
                    return abstract_list

    return abstract_list

def getLayers(abstract_list, wikidata):
    maxAbstractLen = 1000
    # Transform each abstract to an int array padded to max length
    text_dataset = tf.data.Dataset.from_tensor_slices(abstract_list)
    vocabPath = "/home/aphani/datasets/wiki_embeddings/wiki.en.vec.dict"
    vectorize_layer = tf.keras.layers.TextVectorization(
            standardize='lower_and_strip_punctuation', 
            split='whitespace',
            vocabulary=vocabPath,
            output_sequence_length=maxAbstractLen) #max abstract length
    # Vectorize_layer produces output of shape (#abstracts X maxAbstractlen)
    #t1 = time.time()
    # Adapt is not needed as an external vocabulary is passed
    #vectorize_layer.adapt(text_dataset.batch(64)) 
    #print("TextVectorization adapt takes: %s sec" % (time.time() - t1))
    # Get the numpy pre-trained word embeddings
    embedding_matrix = wikidata.to_numpy()
    print(np.shape(embedding_matrix))

    # Build a Embedding layer & initialize with the pre-trained embeddings
    embedding_layer = tf.keras.layers.Embedding(
            input_dim = np.shape(embedding_matrix)[0],
            output_dim = 300, #embedding_dim
            embeddings_initializer=tf.keras.initializers.Constant(embedding_matrix),
            input_length=maxAbstractLen, #max abstract length
            trainable=False)

    # Build a sequential model with both the layers
    model = tf.keras.models.Sequential()
    model.add(tf.keras.Input(shape=(1,), dtype=tf.string))
    model.add(vectorize_layer)
    model.add(embedding_layer)
    return model

#RuntimeError: Detected a call to `Model.predict` inside a `tf.function`. 
#`Model.predict is a high-level endpoint that manages its own `tf.function`. 
#Please move the call to `Model.predict` outside of all enclosing `tf.function`s. 
#@tf.function
def transform(model, abstract_list):
    embedded = model.predict(abstract_list)
    embedded = tf.cast(embedded, tf.float64) #fair comparison
    embedded = tf.reshape(embedded, [10000, 300000])
    print(embedded.shape)
    #print(embedded.dtype)

def batchEmbedding(abstract_list, model):
    batchSize = 10000
    maxiter = math.ceil(len(abstract_list)/batchSize)
    iter = 0
    beg = 0
    timer = 0
    while iter < maxiter:
        end = beg + batchSize
        batch = abstract_list[beg:end]
        t1 = time.time()
        transform(model, batch)
        timer = timer + (time.time() - t1)
        iter = iter + 1
        beg = end
    print("Apply all batches took: %s sec" % timer)


toProcess = 100000; #number of abstracts to embedd
abstracts = readNprep(toProcess)
print("Number of abstracts to process: ",len(abstracts))
# Read the pre-trained word embeddings
wikidata = pd.read_csv("~/datasets/wiki_embeddings/wiki_csv", delimiter=",", header=None)
t1 = time.time()
model = getLayers(abstracts, wikidata)
batchEmbedding(abstracts, model)
print("total time: %s sec" % ((time.time() - t1) * 1000)) #millisec

#np.savetxt("./results/embedding_keras.dat", timeres, delimiter="\t", fmt='%f')

