import sys
import time
import numpy as np
import scipy as sp
from scipy.sparse import csr_matrix
import pandas as pd
import math
import warnings
import os

# Force to CPU (default is GPU)
os.environ["CUDA_VISIBLE_DEVICES"] = ""
import tensorflow as tf
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras import layers

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
warnings.filterwarnings('ignore') #cleaner, but not recommended

def readNprep():
    data1 = pd.read_csv("../../datasets/data1.csv", delimiter=",", header=None)
    data2 = pd.read_csv("../../datasets/data2.csv", delimiter=",", header=None)
    X = pd.concat([data1, data2], axis=1, ignore_index=True)
    num = [*range(0,50)]
    X[num] = X[num].astype(float)
    X = X.iloc[0:100000]
    print(X.head())
    #print(X.info())
    return X

def getCategoricalLayer(X, name, useNumpy):
    # NaN handling. np.nan is a float, which leads to ValueError for str cols
    X[name].fillna('', inplace=True)
    if useNumpy:
      vocab = np.unique(X[name])
      recode = layers.StringLookup(vocabulary=vocab, output_mode="int", num_oov_indices=0, sparse=False)
      # adapt is not required if vocabulary is passed
    else:
      recode = layers.StringLookup(output_mode="int", num_oov_indices=0)
      #df2tf = tf.convert_to_tensor(np.array(X[name], dtype=np.string_))
      recode.adapt(np.array(X[name]))

    #print("#uniques in col ", name, " is ", recode.vocabulary_size())
    return recode 

def getLayers(X):
    # Build a dictionary with symbolic input tensors w/ proper dtype
    inputs = {}
    for name, column in X.items():
      dtype = column.dtype
      if dtype == object:
        dtype = tf.string
      else:
        dtype = tf.float64
      inputs[name] = tf.keras.Input(shape=(1,), dtype=dtype, sparse=False)

    # Seperate out the numeric inputs
    numeric = {name:input for name,input in inputs.items()
      if input.dtype==tf.float64}

    prepro = []
    timers = 0
    # Apply binning on the numeric inputs
    t_f = time.time()
    for name, input in inputs.items():
      if input.dtype == tf.string:
        continue
      t1 = time.time()
      binning = preprocessing.Discretization(num_bins=10, epsilon=0.01) #bin boundaries are unknown
      binning.adapt(np.array(X[name]))
      encoded = binning(input)
      timers = timers + ((time.time() - t1) * 1000) #millisec
      prepro.append(encoded)

    # Recode the string inputs 
    for name, input in inputs.items():
      if input.dtype == tf.float64:
        continue
      t1 = time.time()
      recode = getCategoricalLayer(X, name, True) #use np.unique
      encoded = recode(input)
      timers = timers + ((time.time() - t1) * 1000) #millisec
      # Append to the same list
      prepro.append(encoded)

    print("Elapsed time for adapt = %s sec" % (time.time() - t_f))
    # Concatenate all the preprocessed inputs together,
    # and build a model to apply batch wise later
    cat_layers = layers.Concatenate()(prepro)
    print(cat_layers)
    model_prep = tf.keras.Model(inputs, cat_layers)
    return model_prep, timers

def lazyGraphTransform(X, model, n):
    # This method builds a graph of all the mini-batch transformations
    # by pushing the loop-slicing logic inside a tf.function.
    X_dict = {name: tf.convert_to_tensor(np.array(value)) for name, value in X.items()}
    t1 = time.time()
    res = batchTransform(X_dict, model, X.shape[0])
    timers = (time.time() - t1) * 1000 #millisec
    return res, timers

@tf.function
def batchTransform(X, model_prep, nrow):
    # Batch-wise transformation
    t_t = time.time()
    allRes = []
    bs = 1024;
    ep = 10;
    iter_ep = math.ceil(nrow/bs);
    maxiter = ep * iter_ep;
    print("Total number of iterations: %d" % maxiter) 
    beg = 0;
    iter = 0;
    i = 1
    while iter < maxiter:
        end = beg + bs
        if end > nrow:
            end = nrow
        batch_dict = {name: X[name][beg:end] for name, value in X.items()}
        #X_batch = model_prep(batch_dict)
        X_batch = transform(batch_dict, model_prep)
        X_batch = ((X_batch + X_batch) * i - X_batch) / (i+1)
        X_batch = ((X_batch + X_batch) * i - X_batch) / (i+1)
        X_batch = ((X_batch + X_batch) * i - X_batch) / (i+1)
        X_batch = ((X_batch + X_batch) * i - X_batch) / (i+1)
        X_batch = ((X_batch + X_batch) * i - X_batch) / (i+1)
        X_batch = ((X_batch + X_batch) * i - X_batch) / (i+1)
        X_batch = ((X_batch + X_batch) * i - X_batch) / (i+1)
        X_batch = ((X_batch + X_batch) * i - X_batch) / (i+1)
        X_batch = ((X_batch + X_batch) * i - X_batch) / (i+1)
        X_batch = ((X_batch + X_batch) * i - X_batch) / (i+1)
        #print(X_batch[:1, :]) #print the placeholder
        if X_batch.shape[0] == bs:
            allRes.append(X_batch)
        iter = iter + 1
        if end == nrow:
            beg = 0
            print("Starting next epoch")
        else:
            beg = end
        i = i + 1
    out = tf.stack(allRes, axis=0) #fix rank
    print("Elapsed time for Transform = %s sec" % (time.time() - t_t))
    print(out.shape)
    return out 

# Paritially lazy mode
def batchGraphTransform(X, model, nrow):
    # Batch-wise eager transform to avoid OOM
    beg = 0
    allRes = []
    bs = 1024;
    ep = 10;
    iter_ep = math.ceil(nrow/bs);
    maxiter = ep * iter_ep;
    print("Total number of iterations: %d" % maxiter) 
    beg = 0
    iter = 0
    V = np.random.randint(X.shape[0], size=(X.shape[1], 1))
    tfV = tf.convert_to_tensor(V, dtype=tf.int64)
    i = 1
    timers = 0
    while iter < maxiter:
        end = beg + bs
        if end > nrow:
            end = nrow
        batch_dict = {name: np.array(value)[beg:end] for name, value in X.items()}
        t1 = time.time()
        X_batch = transform(batch_dict, model)
        mx = tf.reduce_max(tf.matmul(X_batch, tfV)) #small operation
        timers = timers + ((time.time() - t1) * 1000) #millisec
        if X_batch.shape[0] == bs:
            allRes.append(X_batch)
        iter = iter + 1
        if end == nrow:
            beg = 0
            print("Starting next epoch")
        else:
            beg = end
        i = i + 1

    out = tf.stack(allRes, axis=0) #fix rank
    print(mx)
    return out, timers


@tf.function
def transform(X_dict, model_prep):
    X_prep = model_prep(X_dict)
    return X_prep


X = readNprep()
timers = np.zeros(3)
for i in range(3):
    t1 = time.time()
    model, etime = getLayers(X)

    # Lazy transform triggers all models togther -- 5x slower than partial lazy mode
    #res, etime = lazyGraphTransform(X, model, X.shape[0]) 

    # Partially lazy mode keeps the minibatch construction outside of tf.function
    out, etime = batchGraphTransform(X, model, X.shape[0])
    timers[i] = timers[i] + ((time.time() - t1) * 1000) #millisec

print(timers)
np.savetxt("batch_keras.dat", timers, delimiter="\t", fmt='%f')


