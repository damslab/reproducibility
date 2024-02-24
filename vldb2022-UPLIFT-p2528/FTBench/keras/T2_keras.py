import tensorflow as tf
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras import layers
import sys
import time
import numpy as np
import pandas as pd
import math
#tf.get_logger().setLevel('ERROR')
tf.config.threading.set_inter_op_parallelism_threads(1)
tf.keras.backend.set_floatx('float64')
# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)

#@tf.function - Fails due to use of numpy in one-hot vocabs
def readNprep():
    # Read and isolate target and training data
    kdd = pd.read_csv("../../datasets/KDD98.csv", delimiter=",", header=None)
    print(kdd.head())
    kddX = kdd.iloc[:,0:469]
    kdd = kdd.drop([0], axis=0)
    kddX = kddX.drop([0], axis=0)
    kddX = kddX.replace(r'\s+',np.nan,regex=True).replace('',np.nan)
    # Replace NAs with before/after entries
    kddX.fillna(method='pad', inplace=True)
    kddX.fillna(method='bfill', inplace=True)

    # Save a all string version, need for string lookup later
    kdd_str = kddX
    # Cast all numeric columns to float first, to avoid 
    # mix of int and float type strings (5, 5.0), which
    # increases # distinct values in a column
    st = [23,24,*range(28,42),195,196,197,*range(362,384),*range(412,434)]
    kdd_str[st] = kdd_str[st].astype(float)
    # Then cast all to string
    kdd_str[[*range(0,468)]] = kddX[[*range(0,468)]].astype(str)

    # Set dtype float for numeric columns
    # The default dtype for all columns is object at this point 
    fl = [4,7,16,26,*range(43,50),53,*range(75,195),*range(198,361),407,409,410,411,*range(434,469)]
    kddX[fl] = kddX[fl].astype(float)
    print(kddX.info())

    # Build a dictionary with symbolic input tensors w/ proper dtype
    t2 = time.time()
    inputs = {}
    for name, column in kddX.items():
      dtype = column.dtype
      if dtype == object:
        dtype = tf.string
      else:
        dtype = tf.float64
      inputs[name] = tf.keras.Input(shape=(1,), dtype=dtype)

    # Seperate out the numeric inputs
    numeric = {name:input for name,input in inputs.items()
      if input.dtype==tf.float64}

    # Concatenate the numeric inputs together and 
    # run them through normalization, binning + one_hot layers 
    x = layers.Concatenate()(list(numeric.values()))
    norm = preprocessing.Normalization()
    norm.adapt(np.array(kddX[numeric.keys()]))
    all_numeric = norm(x)

    # Collect all the symbolic results in a list
    prepro = [all_numeric]

    # Binning + one_hot
    x = layers.Concatenate()(list(numeric.values()))
    #binning = preprocessing.Discretization(bins=[.1,.2,.3,.4,.5,.6,.7,.8,.9]) #bin boundaries are unknown
    binning = preprocessing.Discretization(bins=[-.4,-.3,-.2,-.1,0,.1,.2,.3,.4]) #bin boundaries are unknown
    one_hot = preprocessing.CategoryEncoding(num_tokens=10) # #buckets are unknown
    all_bin = binning(x)
    all_bin_inputs = one_hot(all_bin)
    prepro.append(all_bin_inputs)

    # Recode and dummycode the string inputs 
    for name, input in inputs.items():
      if input.dtype == tf.float64:
        continue
      lookup = preprocessing.StringLookup(vocabulary=np.unique(kdd_str[name]))
      #print("name = ", name, np.unique(kdd_str[name]).shape[0])
      one_hot = preprocessing.CategoryEncoding(num_tokens=lookup.vocabulary_size())
      x = lookup(input)
      x = one_hot(x)
      # Append to the same list
      prepro.append(x)

    # Concatenate all the preprocessed inputs together,
    # and build a model to apply batch wise later
    prepro_cat = layers.Concatenate()(prepro)
    print(prepro_cat)
    kddX_prep = tf.keras.Model(inputs, prepro_cat)
    # Convert the input df to a dictionary of tensors
    kddX_dict = {name: np.array(value)
        for name, value in kddX.items()}
    # Apply the model to get the preprocessed data
    X_prep = kddX_prep(kddX_dict)
    print("Transformation time = %s sec" % (time.time() - t2))
    print(X_prep)
    # Return the data, dictionary and the model
    # The model and the dictiononary are need for batch wise preprocessing
    return X_prep, kddX_dict, kddX_prep


#Xrandom = np.random.uniform(low=0, high=1, size=(100000,1000))
#X = tf.convert_to_tensor(Xrandom, tf.float64)
t1 = time.time()
X, X_dict, prep = readNprep()
print("Read and preprocess time = %s sec" % (time.time() - t1))

#np.savetxt("X_prep.csv", X.numpy(), delimiter=',')
