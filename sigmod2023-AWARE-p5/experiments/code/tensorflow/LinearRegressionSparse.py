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
    data = tf.convert_to_tensor(df, dtype=np.float64)
    return data


def readSparse(path):
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
    df = np.array(df, dtype=np.float64)
    data = tf.sparse.from_dense(df)
    return data


@tf.function
def iteration(
    it, p, norm_r2, W, X_idx, X_val, X_dense_shape, Xt_idx, Xt_val, Xt_dense_shape, r
):

    eps = tf.constant(0.00001, dtype=np.float64)
    X = tf.SparseTensor(X_idx, X_val, X_dense_shape)
    Xt = tf.SparseTensor(Xt_idx, Xt_val, Xt_dense_shape)

    Xp = tf.sparse.sparse_dense_matmul(X, p)
    XtXp = tf.sparse.sparse_dense_matmul(Xt, Xp)
    q = tf.add(XtXp, tf.multiply(eps, p))
    alpha = tf.divide(norm_r2, tf.matmul(p, q, transpose_a=True))
    W = tf.add(W, tf.multiply(alpha, p))
    old_norm_r2 = norm_r2
    r = tf.add(r, tf.multiply(alpha, q))
    norm_r2 = tf.reduce_sum(tf.multiply(r, r))
    tf.print(it, " : norm_r2 : ", norm_r2)
    beta = tf.divide(norm_r2, old_norm_r2)
    p = tf.add(tf.negative(r), tf.multiply(beta, p))
    return (
        it + 1,
        p,
        norm_r2,
        W,
        X_idx,
        X_val,
        X_dense_shape,
        Xt_idx,
        Xt_val,
        Xt_dense_shape,
        r,
    )


@tf.function
def exec():
    X = readSparse(args.X)
    Y = readCSV(args.Y)
    max_iterations = args.iterations

    W = tf.zeros([tf.shape(X)[1], 1], dtype=np.float64)

    i = 0

    X_idx = X.indices
    X_val = X.values
    X_dense_shape = X.dense_shape

    Xt = tf.sparse.transpose(X)
    Xt_idx = Xt.indices
    Xt_val = Xt.values
    Xt_dense_shape = Xt.dense_shape

    p = tf.sparse.sparse_dense_matmul(Xt, Y)

    min1 = tf.constant(-1, dtype=np.float64)
    r = tf.multiply(min1, p)
    norm_r2 = tf.reduce_sum(tf.multiply(r, r))

    i0 = tf.constant(0)

    def condition(
        it,
        p,
        norm_r2,
        W,
        X_idx,
        X_val,
        X_dense_shape,
        Xt_idx,
        Xt_val,
        Xt_dense_shape,
        r,
    ):
        return it < max_iterations

    [
        i0,
        p,
        norm_r2,
        W,
        X_idx,
        X_val,
        X_dense_shape,
        Xt_idx,
        Xt_val,
        Xt_dense_shape,
        r,
    ] = tf.while_loop(
        condition,
        iteration,
        loop_vars=[
            i0,
            p,
            norm_r2,
            W,
            X_idx,
            X_val,
            X_dense_shape,
            Xt_idx,
            Xt_val,
            Xt_dense_shape,
            r,
        ],
    )
    return W


np.savetxt("code/tensorflow/tensorflowModelSparse.csv", exec(), delimiter=",")
