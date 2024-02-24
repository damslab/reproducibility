# Notes:
# 1. adapt() is way slower than np.unique -- takes forever for 1M, hangs for 10M
# 2. TF returns error if adapt is inside tf.function. adapt uses graph inside anyway
# 3. OOM in batch mode during sparse_to_dense despite of seting sparse in keras
# 4. Always replace NaNs in string cols as np.nan is float
# 5. Full graph mode lazily triggers all models together -- produce OOM
# 6. Partial graph mode sequentially execute graph-models
# TODO1: all sparse intermediates, including the outputs
# TODO2: Tune mini-batch size for best performance

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

def readNprep(nRows):
    # Read the 1M or the 10M dataset
    if nRows == 1:
      print("Reading file: criteo_day21_1M")
      criteo = pd.read_csv("../../datasets/criteo_day21_1M", delimiter=",", header=None)
    else:
      print("Reading file: criteo_day21_10M")
      criteo = pd.read_csv("../../datasets/criteo_day21_10M", delimiter=",", header=None)
    print(criteo.head())
    # Replace NaNs with 0 for numeric and empty string for categorical
    criteo = criteo.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc' else x.fillna(''))

    # Pandas infer the type of first 14 columns as float and int.
    # SystemDS reads those as STRINGS and apply passthrough FT on those.
    # For a fair comparision, convert those here to str and later back to float
    pt = [*range(0,14)]
    criteo[pt] = criteo[pt].astype(str)
    #print(criteo.info())
    return criteo 

def getCategoricalLayer(X, name, useNumpy):
    # NaN handling. np.nan is a float, which leads to ValueError for str cols
    X[name].fillna('', inplace=True)
    if useNumpy:
      vocab = np.unique(X[name].astype(np.string_))
      onehot = layers.StringLookup(vocabulary=vocab, output_mode="multi_hot", num_oov_indices=0, sparse=True)
      # adapt is not required if vocabulary is passed
    else:
      onehot = layers.StringLookup(output_mode="multi_hot", num_oov_indices=0)
      df2tf = tf.convert_to_tensor(np.array(X[name], dtype=np.string_))
      onehot.adapt(df2tf)

    #print("#uniques in col ", name, " is ", onehot.vocabulary_size())
    return onehot

def getLayers(X):
    # Passh through transformation -- convert to float
    pt = [*range(0,14)]
    X[pt] = X[pt].astype(np.float64)

    # Build a dictionary with symbolic input tensors w/ proper dtype
    inputs = {}
    for name, column in X.items():
      dtype = column.dtype
      if dtype == object:
        dtype = tf.string
      else:
        dtype = tf.float64
      inputs[name] = tf.keras.Input(shape=(1,), dtype=dtype, sparse=True)

    # Seperate out the numeric inputs
    numeric = {name:input for name,input in inputs.items()
      if input.dtype==tf.float64}

    # Concatenate the numeric inputs together and 
    # add to the list of layers as is
    prepro = [layers.Concatenate()(list(numeric.values()))]

    # Recode and dummycode the string inputs 
    for name, input in inputs.items():
      if input.dtype == tf.float64:
        continue
      onehot = getCategoricalLayer(X, name, True) #use np.unique
      encoded = onehot(input)
      # Append to the same list
      prepro.append(encoded)

    # Concatenate all the preprocessed inputs together,
    # and build a model to apply batch wise later
    cat_layers = layers.Concatenate()(prepro)
    print(cat_layers)
    model_prep = tf.keras.Model(inputs, cat_layers)
    return model_prep

def lazyGraphTransform(X, model, n, isSmall):
    # This method builds a graph of all the mini-batch transformations
    # by pushing the loop-slicing logic inside a tf.function.
    # However, lazily triggering all the models produce OOM
    X_dict = {name: tf.convert_to_tensor(np.array(value)) for name, value in X.items()}
    res = batchTransform(X_dict, model, X.shape[0], isSmall)

@tf.function
def batchTransform(X, model_prep, n, isSmall):
    # Batch-wise transform to avoid OOM
    # 10k/1.5k: best performance within memory budget
    batch_size = 10000 if isSmall==1 else 1500
    beg = 0
    allRes = []
    while beg < n:
      end = beg + batch_size
      if end > n:
        end = n
      batch_dict = {name: X[name][beg:end] for name, value in X.items()}
      X_batch = model_prep(batch_dict)
      print(X_batch[:1, :]) #print the placeholder
      allRes.append(X_batch)
      if end == n:
        break
      else:
        beg = end
    out = tf.stack(allRes, axis=0) #fix rank
    print(out.shape)
    return out 

def batchGraphTransform(X, model, n, isSmall):
    # Batch-wise eager transform to avoid OOM
    # 10k/1.5k: best performance within memory budget
    batch_size = 10000 if isSmall==1 else 1500
    beg = 0
    while beg < n:
      end = beg + batch_size
      if end > n:
        end = n
      batch_dict = {name: np.array(value)[beg:end] for name, value in X.items()}
      X_batch = transform(batch_dict, model)
      # Don't stack the results to avoid OOM
      print(X_batch[:1, :]) #print first 1 row
      if end == n:
        break
      else:
        beg = end


@tf.function
def transform(X_dict, model_prep):
    X_prep = model_prep(X_dict)
    #print(X_prep[:5, :]) #print to verify lazy execution
    return X_prep


isSmall = int(sys.argv[1]) #1M vs 10M subset of Criteo
X = readNprep(isSmall)
t1 = time.time()
model = getLayers(X)

# Lazy transform triggers all models togther -- produce OOM
#res = lazyGraphTransform(X, model, X.shape[0], isSmall)

# Partially lazy mode keeps the slicing outside of tf.function
batchGraphTransform(X, model, X.shape[0], isSmall)

print("Elapsed time for transformations using tf-keras = %s sec" % (time.time() - t1))

#np.savetxt("X_prep_sk.csv", X_prep, fmt='%1.2f', delimiter=',') #dense
#sp.sparse.save_npz("X_prep_sk.npz", X_prep)  #sparse

