import argparse
import os
import sys
import time

import numpy as np
import pandas as pd

import tensorflow as tf
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

tf.config.threading.set_inter_op_parallelism_threads(32)
tf.config.threading.set_intra_op_parallelism_threads(32)


parser = argparse.ArgumentParser()
parser.add_argument("-x", "--X", required=True)
parser.add_argument("-y", "--Y", required=True)
parser.add_argument("-i", "--iterations", required=True, type=int)
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

    data = tf.convert_to_tensor(df, dtype=tf.bfloat16)
    
    return data


@tf.function
def iteration(it, p, norm_r2, W, X, r):

    eps = tf.constant(0.00001, dtype=tf.bfloat16)
    Xp = tf.matmul(X, p)
    XtXp = tf.matmul(X, Xp, transpose_a=True)
    q = tf.add(XtXp, tf.multiply(eps, p))
    alpha = tf.divide(norm_r2, tf.matmul(p, q, transpose_a=True))
    W = tf.add(W, tf.multiply(alpha, p))
    old_norm_r2 = norm_r2
    r = tf.add(r, tf.multiply(alpha, q))
    norm_r2 = tf.reduce_sum(tf.multiply(r, r))
    tf.print(it, " : norm_r2 : ", norm_r2)
    # print(norm_r2)
    beta = tf.divide(norm_r2, old_norm_r2)
    p = tf.add(tf.negative(r), tf.multiply(beta, p))
    return it + 1, p, norm_r2, W, X, r


@tf.function
def exec(X, Y):
    # Normalize X
    rowSum = tf.reduce_sum(X, 0)
    rowMean = tf.multiply(rowSum, 1.0 / X.get_shape()[0])
    X = X - rowMean
    
    max_iterations = args.iterations
    W = tf.zeros([tf.shape(X)[1], 1], dtype=tf.bfloat16)
    i = 0
    p = tf.matmul(X, Y, transpose_a=True)
    # min1 = tf.constant(-1, dtype=tf.bfloat16)
    # r = tf.multiply(min1, p)
    r = tf.negative(p)
    norm_r2 = tf.reduce_sum(tf.multiply(r, r))
    tf.print("InitNorm:", norm_r2)

    i0 = tf.constant(0)

    def condition(it, p, norm_r2, W, X, r):
        return it < max_iterations

    [i, p, norm_r2, W, X, r] = tf.while_loop(
        condition, iteration, loop_vars=[i0, p, norm_r2, W, X, r]
    )
    return W


time_start = time.time()
X = readCSV(args.X)
Y = readCSV(args.Y)
# tf.print(Y)
time_end = time.time()
print("IO Time: " + str(time_end - time_start))

tf.print("Sum of X: ", tf.reduce_sum(X))
tf.print("Sum of Y: ", tf.reduce_sum(Y))

np.savetxt("code/tensorflow/tensorflowModelGraph.csv", exec(X, Y), delimiter=",")
