import tensorflow as tf
import sys
import numpy as np
import scipy.sparse as sparse
import pandas as pd
import math
tf.config.threading.set_inter_op_parallelism_threads(1)

@tf.function
def scale(X):
  X -= tf.reduce_mean(X, axis=0) 
  X_std = tf.math.reduce_std(X, axis=0)
  X_norm = X/X_std
  return X_norm

@tf.function
def pca(X, k):
  # perform z-scoring
  X_norm = scale(X)

  # co-variance matrix
  N = X_norm.get_shape()[0]
  mu = tf.reduce_sum(X_norm, 0)/N
  mu = tf.reshape(mu, [1,mu.get_shape()[0]])
  C = tf.matmul(X_norm, X_norm, transpose_a=True)/(N-1) - (N/(N-1))*tf.matmul(mu, mu, transpose_a=True)

  # compute eigen vectors and values
  eigen_values, eigen_vectors = tf.linalg.eigh(C)

  indices = tf.range(0, k)
  evec_dominant = tf.gather(eigen_vectors, indices, axis=1)
  X_new = tf.matmul(X_norm, evec_dominant)
  return X_new

@tf.function
@tf.autograph.experimental.do_not_convert
def crossV(X, y, lamda, k):
  dataset_X = []
  dataset_y = []
  nrow = X.get_shape()[0]
  fs = math.ceil(nrow/k) #calculate fold size
  train_rows = fs * (k-1)
  off = fs - 1;
  for i in range(k):  #part X and y into lists of k matrices
    dataset_X.append(X[i*fs : min((i+1)*fs, nrow),])
    dataset_y.append(y[i*fs : min((i+1)*fs, nrow),])

  beta_list = []
  for i in range(k):
    tmpX = dataset_X.copy()
    tmpy = dataset_y.copy()
    testX = tmpX.pop(i) #remove ith fold and use as test data
    testy = tmpy.pop(i)
    trainX = tf.concat(tmpX, 0) #rbind k-1 matrices
    trainy = tf.concat(tmpy, 0)
    beta = lmDS(trainX, trainy, lamda, 0)
    beta_list.append(tf.reshape(beta, [-1]))   #'-1' is to flatten beta
  R = tf.stack(beta_list) #R has k number of rows
  R_sum = tf.transpose(tf.reduce_sum(R, 0, keepdims=True))
  return R_sum

@tf.function
def lmDS(X, y, reg, icpt):
  n = X.get_shape()[0]
  m = X.get_shape()[1]
  ones_n = np.ones((n,1))
  m_ext = m
  X_l = X
  if icpt == 1:
    X_l = tf.concat([X, ones_n], 1)
    m_ext = X_l.get_shape()[1]
  
  scale_lambda = np.ones((m_ext,1), dtype=float)
  if icpt == 1:
    scale_lambda[m_ext-1,0] = 0
  
  scale_lambda = scale_lambda * reg
  lamda = tf.constant(scale_lambda, dtype=tf.float64, shape=[m_ext])
  A1 = tf.matmul(X_l, X_l, transpose_a=True)
  b = tf.matmul(X_l, y, transpose_a=True)
  A1 = A1 + tf.linalg.diag(lamda)
  beta_unscaled = tf.linalg.solve(A1, b)
  beta = beta_unscaled
  return beta

@tf.function
def lmpredict(X, w, icpt):
  if icpt == 0:
    y = tf.matmul(X, w)
  else: #icpt=1
    ones_n = np.ones((X.get_shape()[0], 1))
    X = tf.concat([X, ones_n], 1)
    y = tf.matmul(X, w)
  return y

@tf.function
def checkR2(X, y, y_p, beta, icpt):
  n = tf.cast(X.get_shape()[0], tf.float64)
  m = X.get_shape()[1]
  m_ext = m
  if icpt == 1:
    m_ext = m + 1
  avg_tot = tf.divide(tf.reduce_sum(y), n)
  ss_tot = tf.reduce_sum(tf.square(y))
  ss_avg_tot = tf.subtract(ss_tot, tf.multiply(n, tf.square(avg_tot)))
  y_res = tf.subtract(y, y_p)
  avg_res = tf.divide(tf.reduce_sum(y_res), n)
  ss_res = tf.reduce_sum(tf.square(y_res))
  R2 = tf.subtract(tf.cast(1, tf.float64), tf.divide(ss_res, ss_avg_tot))
  dispersion = tf.divide(ss_res, tf.cast(tf.subtract(n, m_ext), tf.float64))
  R2_ad = tf.subtract(tf.cast(1,tf.float64), tf.divide(dispersion, \
                                    tf.divide(ss_avg_tot, tf.subtract(n,1))))
  return R2_ad


@tf.function
def pipeline(A, y):
  Kc = np.floor(A.shape[1] * 0.8)
  Kc = int(Kc)
  Kc_lim = Kc + 10
  step = 1
  R2list = []
  R2_ad1 = tf.zeros([1,1], tf.float64)
  A_t = tf.convert_to_tensor(A, dtype=tf.float64)
  y_t = tf.convert_to_tensor(y, dtype=tf.float64)
  j = tf.constant(1)
  # Find the best k
  while Kc < Kc_lim:
    newA1 = pca(X=A_t, k=Kc)
    beta1 = crossV(X=newA1, y=y_t, lamda=0.0001, k=32)
    y_predict1 = lmpredict(newA1, beta1, icpt=0)
    R2_ad1 = checkR2(newA1, y_t, y_predict1, beta1, icpt=0)
    R2list.append(R2_ad1)
    Kc = Kc + step
  
  # Tune regularization parameter
  reg = 0.0001
  reg_lim = 0.001
  step = (reg_lim - reg)/10
  while reg < reg_lim:
    newA3 = pca(A_t, k=Kc_lim)
    beta3 = crossV(newA3, y_t, lamda=reg, k=32)
    y_predict3 = lmpredict(newA3, beta3, icpt=0)
    R2_ad3 = checkR2(newA3, y_t, y_predict3, beta3, icpt=0)
    R2list.append(R2_ad3)
    reg = reg + step


  return R2list

# Create the datasets
M = int(sys.argv[1])
Xrandom = np.random.uniform(low=0, high=1, size=(M,1000))
yrandom = np.random.uniform(low=0, high=1, size=(M,1))
# Call the pipeline
R2list = pipeline(Xrandom, yrandom)
R = tf.stack(R2list)
np.savetxt("outtf.csv", R.numpy(), delimiter=',')
