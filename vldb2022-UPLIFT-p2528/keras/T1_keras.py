import sys
import time
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras import layers
import scipy as sp
from scipy.sparse import csr_matrix
import pandas as pd
import math
import warnings

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
warnings.filterwarnings('ignore') #cleaner, but not recommended

def readNprep():
    # Read and isolate target and training data
    adult = pd.read_csv("~/datasets/adult.data", delimiter=",", header=None)
    print(adult.head())

    # Pandas infer the type of a few columns as int64.
    # SystemDS reads those as STRINGS and apply passthrough FT on those.
    # For a fair comparision, convert those here to str and later back to float
    pt = [*range(0,15)]
    adult[pt] = adult[pt].astype(str)
    # convert numerical features to float
    pt = [0, 2, 4, 10, 11, 12]
    adult[pt] = adult[pt].astype(np.float64)
    print(adult.info())
    return adult 

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


def getLayers(X, useNumpy):
    # Build a dictionary with symbolic input tensors w/ proper dtype
    inputs = {}
    for name, column in X.items():
      dtype = column.dtype
      if dtype == object:
        dtype = tf.string
      else:
        dtype = tf.float64
      inputs[name] = tf.keras.Input(shape=(1,), dtype=dtype)

    # Seperate out the numeric inputs
    numeric = {name:input for name,input in inputs.items()
      if input.dtype==tf.float64}

    prepro = []
    # Apply binning on the numeric inputs
    t_f = time.time()
    for name, input in inputs.items():
      if input.dtype == tf.string:
        continue
      binning = preprocessing.Discretization(num_bins=5, epsilon=0.01) #bin boundaries are unknown
      binning.adapt(np.array(X[name]))
      encoded = binning(input)
      prepro.append(tf.cast(encoded, tf.float32)) #cast binned layers to float

    # Concatenate the numeric inputs together and 
    # add to the list of layers as is
    # prepro = [layers.Concatenate()(list(numeric.values()))]

    # Recode and dummycode the string inputs 
    for name, input in inputs.items():
      if input.dtype == tf.float64:
        continue
      onehot = getCategoricalLayer(X, name, useNumpy) #3rd parameter: to use np.unique
      encoded = onehot(input)
      # Append to the same list
      prepro.append(encoded)

    # Concatenate all the preprocessed inputs together,
    # and build a model to apply batch wise later
    cat_layers = layers.Concatenate()(prepro)
    print(cat_layers)
    model_prep = tf.keras.Model(inputs, cat_layers)
    return model_prep

@tf.function
def transform(X_dict, model_prep):
    X_prep = model_prep(X_dict)
    #print(X_prep[:5, :]) #print to verify lazy execution
    print(X_prep.shape)
    return X_prep


X = readNprep()
X_dict = {name: np.array(value)
    for name, value in X.items()}

timeres = np.zeros(3)
timeres_np = np.zeros(3)
for i in range(3):
    # Run 3 times with Keras stringlookup and adapt 
    t1 = time.time()
    model = getLayers(X, False)
    X_prep = transform(X_dict, model)
    timeres[i] = timeres[i] + ((time.time() - t1) * 1000) #millisec

    # Run 3 times with np.unique
    t1 = time.time()
    model = getLayers(X, True)
    X_prep = transform(X_dict, model)
    timeres_np[i] = timeres_np[i] + ((time.time() - t1) * 1000) #millisec

print("Elapsed time for transformations using tf-keras")
print(timeres)
print(timeres_np)

np.savetxt("./results/adult_keras.dat", timeres, delimiter="\t", fmt='%f')
np.savetxt("./results/adult_keras_np.dat", timeres_np, delimiter="\t", fmt='%f')

