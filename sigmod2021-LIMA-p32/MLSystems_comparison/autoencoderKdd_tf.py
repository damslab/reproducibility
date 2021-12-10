import sys
import time
import numpy as np
import pandas as pd
import math
import os

# Force to CPU (default is GPU)
os.environ["CUDA_VISIBLE_DEVICES"] = ""
import tensorflow as tf
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras import layers

# Disable inter-operator parallelism for fairness
tf.config.threading.set_inter_op_parallelism_threads(1)
tf.keras.backend.set_floatx('float64')
# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)

def readNprep():
    # Read and isolate target and training data
    kdd = pd.read_csv("../datasets/KDD98.csv", delimiter=",", header=None)
    print(kdd.head())
    kddX = kdd.iloc[:,0:469]
    kddX = kddX.drop([0], axis=0)

    # Save a all string version, need for string lookup later
    kdd_str = kddX
    kdd_str[[*range(0,468)]] = kddX[[*range(0,468)]].astype(str)

    # Set dtype float for numeric columns
    # The default dtype for all columns is object at this point 
    fl = [4,7,16,26,*range(43,50),53,*range(75,195),*range(198,361),407,409,410,411,*range(434,469)]
    kddX[fl] = kddX[fl].astype(float)
    print(kddX.info())

    # Build a dictionary with symbolic input tensors w/ proper dtype
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
    binning = preprocessing.Discretization(bins=[.1,.2,.3,.4,.5,.6,.7,.8,.9]) #bin boundaries are unknown
    one_hot = preprocessing.CategoryEncoding(max_tokens=10) # #buckets are unknown
    all_bin = binning(x)
    all_bin_inputs = one_hot(all_bin)
    prepro.append(all_bin_inputs)

    # Recode and dummycode the string inputs 
    for name, input in inputs.items():
      if input.dtype == tf.float64:
        continue
      lookup = preprocessing.StringLookup(vocabulary=np.unique(kdd_str[name]))
      one_hot = preprocessing.CategoryEncoding(max_tokens=lookup.vocab_size())
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
    #print(X_prep)
    # Return the data, dictionary and the model
    # The model and the dictiononary are need for batch wise preprocessing
    return X_prep, kddX_dict, kddX_prep


#@tf.function
def func(X):
  Y = (tf.math.exp(2*X) - 1) / (tf.math.exp(2*X) + 1)
  Y_prime = 1 - tf.math.square(Y)
  return Y, Y_prime

#@tf.function
def feedForward(X, W1, b1, W2, b2, W3, b3, W4, b4, Y):
  H1_in = tf.transpose(tf.matmul(W1, X, transpose_b=True) + b1)
  #H1, H1_prime = func(H1_in)
  H1 = (tf.math.exp(2*H1_in) - 1) / (tf.math.exp(2*H1_in) + 1)
  H1_prime = 1 - tf.math.square(H1)

  H2_in = tf.transpose(tf.matmul(W2, H1, transpose_b=True) + b2)
  #H2, H2_prime = func(H2_in)
  H2 = (tf.math.exp(2*H2_in) - 1) / (tf.math.exp(2*H2_in) + 1)
  H2_prime = 1 - tf.math.square(H2)

  H3_in = tf.transpose(tf.matmul(W3, H2, transpose_b=True) + b3)
  #H3, H3_prime = func(H3_in)
  H3 = (tf.math.exp(2*H3_in) - 1) / (tf.math.exp(2*H3_in) + 1)
  H3_prime = 1 - tf.math.square(H3)

  Yhat_in = tf.transpose(tf.matmul(W4, H3, transpose_b=True) + b4)
  #Yhat, Yhat_prime = func(Yhat_in)
  Yhat = (tf.math.exp(2*Yhat_in) - 1) / (tf.math.exp(2*Yhat_in) + 1)
  Yhat_prime = 1 - tf.math.square(Yhat)
  E = Yhat - Y

  return H1, H1_prime, H2, H2_prime, H3, H3_prime, Yhat, Yhat_prime, E

#@tf.function
def grad(X, H1, H1_prime, H2, H2_prime, H3, H3_prime, Yhat_prime, E, W1, W2, W3, W4):
  #backprop
  delta4 = E * Yhat_prime
  delta3 = H3_prime * tf.matmul(delta4, W4)
  delta2 = H2_prime * tf.matmul(delta3, W3)
  delta1 = H1_prime * tf.matmul(delta2, W2)

  #compute gradients
  b4_grad = tf.transpose(tf.reduce_sum(delta4, 0))
  b3_grad = tf.transpose(tf.reduce_sum(delta3, 0))
  b2_grad = tf.transpose(tf.reduce_sum(delta2, 0))
  b1_grad = tf.transpose(tf.reduce_sum(delta1, 0))

  W4_grad = tf.matmul(delta4, H3, transpose_a=True)
  W3_grad = tf.matmul(delta3, H2, transpose_a=True)
  W2_grad = tf.matmul(delta2, H1, transpose_a=True)
  W1_grad = tf.matmul(delta1, X, transpose_a=True)

  return W1_grad, b1_grad, W2_grad, b2_grad, W3_grad, b3_grad, W4_grad, b4_grad

#@tf.function
def calc_grad(X, W1, b1, W2, b2, W3, b3, W4, b4, Y):
  H1_in = tf.transpose(tf.matmul(W1, X, transpose_b=True) + b1)
  #H1, H1_prime = func(H1_in)
  H1 = (tf.math.exp(2*H1_in) - 1) / (tf.math.exp(2*H1_in) + 1)
  H1_prime = 1 - tf.math.square(H1)

  H2_in = tf.transpose(tf.matmul(W2, H1, transpose_b=True) + b2)
  #H2, H2_prime = func(H2_in)
  H2 = (tf.math.exp(2*H2_in) - 1) / (tf.math.exp(2*H2_in) + 1)
  H2_prime = 1 - tf.math.square(H2)

  H3_in = tf.transpose(tf.matmul(W3, H2, transpose_b=True) + b3)
  #H3, H3_prime = func(H3_in)
  H3 = (tf.math.exp(2*H3_in) - 1) / (tf.math.exp(2*H3_in) + 1)
  H3_prime = 1 - tf.math.square(H3)

  Yhat_in = tf.transpose(tf.matmul(W4, H3, transpose_b=True) + b4)
  #Yhat, Yhat_prime = func(Yhat_in)
  Yhat = (tf.math.exp(2*Yhat_in) - 1) / (tf.math.exp(2*Yhat_in) + 1)
  Yhat_prime = 1 - tf.math.square(Yhat)
  E = Yhat - Y

  #backprop
  delta4 = E * Yhat_prime
  delta3 = H3_prime * tf.matmul(delta4, W4)
  delta2 = H2_prime * tf.matmul(delta3, W3)
  delta1 = H1_prime * tf.matmul(delta2, W2)

  #compute gradients
  b4_grad = tf.transpose(tf.reduce_sum(delta4, 0))
  b3_grad = tf.transpose(tf.reduce_sum(delta3, 0))
  b2_grad = tf.transpose(tf.reduce_sum(delta2, 0))
  b1_grad = tf.transpose(tf.reduce_sum(delta1, 0))

  W4_grad = tf.matmul(delta4, H3, transpose_a=True)
  W3_grad = tf.matmul(delta3, H2, transpose_a=True)
  W2_grad = tf.matmul(delta2, H1, transpose_a=True)
  W1_grad = tf.matmul(delta1, X, transpose_a=True)

  return W1_grad, b1_grad, W2_grad, b2_grad, W3_grad, b3_grad, W4_grad, b4_grad, E

#@tf.function
def obj(E):
  val = 0.5 * tf.reduce_sum(tf.math.square(E))
  return val

#@tf.function
def autoencoder(X, X_dict, num_hidden1, num_hidden2, max_epochs, num_batch, prep):
  batch_size = num_batch
  mu = 0.9
  step = 1e-5
  decay = 0.95
  
  n = X.shape[0]
  m = X.shape[1]
  
  W1 = tf.math.sqrt(tf.cast(6.0, tf.float64)) \
  / tf.math.sqrt(tf.cast((m + num_hidden1), tf.float64)) \
    * np.random.uniform(low=-1, high=1, size=(num_hidden1,m))
  b1 = tf.constant(0, dtype=tf.float64, shape=(num_hidden1, 1))
  W2 = tf.math.sqrt(tf.cast(6.0, tf.float64)) \
  / tf.math.sqrt(tf.cast((num_hidden1 + num_hidden2), tf.float64)) \
    * np.random.uniform(low=-1, high=1, size=(num_hidden2,num_hidden1))
  b2 = tf.constant(0, dtype=tf.float64, shape=(num_hidden2, 1))
  W3 = tf.math.sqrt(tf.cast(6.0, tf.float64)) \
  / tf.math.sqrt(tf.cast((num_hidden2 + num_hidden1), tf.float64)) \
    * np.random.uniform(low=-1, high=1, size=(num_hidden1,num_hidden2))
  b3 = tf.constant(0, dtype=tf.float64, shape=(num_hidden1, 1))
  W4 = tf.math.sqrt(tf.cast(6.0, tf.float64)) \
  / tf.math.sqrt(tf.cast((num_hidden2 + m), tf.float64)) \
    * np.random.uniform(low=-1, high=1, size=(m,num_hidden1))
  b4 = tf.constant(0, dtype=tf.float64, shape=(m, 1))
  
  upd_W1 = tf.constant(0, dtype=tf.float64, shape=W1.get_shape())
  upd_b1 = tf.constant(0, dtype=tf.float64, shape=b1.get_shape())
  upd_W2 = tf.constant(0, dtype=tf.float64, shape=W2.get_shape())
  upd_b2 = tf.constant(0, dtype=tf.float64, shape=b2.get_shape())
  upd_W3 = tf.constant(0, dtype=tf.float64, shape=W3.get_shape())
  upd_b3 = tf.constant(0, dtype=tf.float64, shape=b3.get_shape())
  upd_W4 = tf.constant(0, dtype=tf.float64, shape=W4.get_shape())
  upd_b4 = tf.constant(0, dtype=tf.float64, shape=b4.get_shape())

  iter = 0
  num_iters_per_epoch = math.ceil(n/batch_size)
  max_iterations = max_epochs * num_iters_per_epoch
  print('max_iterations = ',max_iterations)
  beg = 0 
  for iter in tf.range(max_iterations):
    end = beg + batch_size
    if end > n:
      end = n
    batch_dict = {name:values[beg:end] for name, values in X_dict.items()}
    X_batch = prep(batch_dict)
    X_batch = tf.where(tf.math.is_nan(X_batch), tf.zeros_like(X_batch), X_batch)
    X_batch = tf.where(tf.math.is_inf(X_batch), tf.ones_like(X_batch), X_batch)

    W1_grad, b1_grad, W2_grad, b2_grad, W3_grad, b3_grad, \
        W4_grad, b4_grad, E = calc_grad(X_batch, W1, b1, W2, b2, 
                W3, b3, W4, b4, X_batch)
    o = obj(E)
  
    #Debug print
    # python print only executes once while tracing, but not during
    # execution as that doesn't get a node in the graph
    #tf.print('iter=',iter,' beg=',beg,' end=',end,' obj=',o)
  
    #update
    local_step = step / X_batch.get_shape()[1]
    upd_W1 = mu * upd_W1 - local_step * W1_grad
    upd_b1 = mu * upd_b1 - local_step * b1
    upd_W2 = mu * upd_W2 - local_step * W2_grad
    upd_b2 = mu * upd_b2 - local_step * b2
    upd_W3 = mu * upd_W3 - local_step * W3_grad
    upd_b3 = mu * upd_b3 - local_step * b3
    upd_W4 = mu * upd_W4 - local_step * W4_grad
    upd_b4 = mu * upd_b4 - local_step * b4

    W1 = W1 + upd_W1
    b1 = b1 + upd_b1
    W2 = W2 + upd_W2
    b2 = b2 + upd_b2
    W3 = W3 + upd_W3
    b3 = b3 + upd_b3
    W4 = W4 + upd_W4
    b4 = b4 + upd_b4
  
    if end == n:
      beg = 0 
    else:
      beg = end 

  return W1, b1, W2, b2, W3, b3, W4, b4
  
#########################################################

t1 = time.time()
X, X_dict, prep = readNprep()
print("Read and preprocess time = %s sec" % (time.time() - t1))

# Read the inputs
num_hidden1 = int(sys.argv[1])
num_hidden2 = int(sys.argv[2])
max_epochs = int(sys.argv[3]) 
num_batch = int(sys.argv[4])

# Call the training method
W1, b1, W2, b2, W3, \
        b3, W4, b4 = autoencoder(X, X_dict, num_hidden1, 
                num_hidden2, max_epochs, num_batch, prep)

# Save the model
np.savetxt("W1out_tf.csv", W1.numpy(), delimiter=',')
np.savetxt("b1out_tf.csv", b1.numpy(), delimiter=',')
np.savetxt("W2out_tf.csv", W2.numpy(), delimiter=',')
np.savetxt("b2out_tf.csv", b2.numpy(), delimiter=',')
np.savetxt("W3out_tf.csv", W3.numpy(), delimiter=',')
np.savetxt("b3out_tf.csv", b3.numpy(), delimiter=',')
np.savetxt("W4out_tf.csv", W4.numpy(), delimiter=',')
np.savetxt("b4out_tf.csv", b4.numpy(), delimiter=',')
