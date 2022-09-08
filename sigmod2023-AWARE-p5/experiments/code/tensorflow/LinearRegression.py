import argparse
import os
import sys
import time

import numpy as np
import pandas as pd

import tensorflow as tf
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


parser = argparse.ArgumentParser()
parser.add_argument("-x", "--X", required=True)
parser.add_argument("-y", "--Y", required=True)
parser.add_argument("-i", "--iterations", required =True, type=int)
args = parser.parse_args()

print("tensorflow version:" + str(tf.__version__))


def readCSV(path):
    if os.path.isdir(path):
        csv_folder = path
        files = os.listdir(path)
        df_parts = []
        for f in files:
            csv_file = csv_folder + "/" + f
            df_parts.append(pd.read_csv(csv_file, header=None))

        df = pd.concat(df_parts, ignore_index=True)
    else:
        df = pd.read_csv(path, header=None)

    data = tf.constant(df.values, dtype=np.float64)
    return data

time_start = time.time()

X = readCSV(args.X)
Y = readCSV(args.Y)

time_end = time.time()
print("IO Time: " + str(time_end - time_start))

max_iterations = args.iterations
tf.print("Sum of X: ",tf.reduce_sum(X))
tf.print("Sum of Y: ",tf.reduce_sum(Y))

eps = tf.constant( 0.00001, dtype=np.float64)
W = tf.zeros([tf.shape(X)[1], 1], dtype=np.float64)

rowSum = tf.reduce_sum(X, 0)
rowMean = tf.multiply(rowSum, 1.0 / X.get_shape()[0])
X = X - rowMean

i = 0

p = tf.matmul(X, Y, transpose_a=True)
r = tf.multiply(-1, p)
norm_r2 = tf.reduce_sum(tf.multiply(r,r))
tf.print("InitNorm:", norm_r2)

for i in range(max_iterations):
    Xp = tf.matmul(X, p)
    XtXp = tf.matmul(X, Xp, transpose_a=True)
    q = tf.add(XtXp, tf.multiply(eps, p))
    alpha = tf.divide(norm_r2, tf.matmul(p,q,transpose_a=True))
    W = tf.add(W, tf.multiply(alpha , p))
    old_norm_r2 = norm_r2
    r = tf.add(r,tf.multiply(alpha, q))
    norm_r2 = tf.reduce_sum(tf.multiply(r,r))
    tf.print(i, " : norm_r2 : ", norm_r2)
    beta = tf.divide( norm_r2 , old_norm_r2)
    p = tf.add(tf.negative(r), tf.multiply(beta, p))


np.savetxt("code/tensorflow/tensorflowModel.csv", W, delimiter=",")
