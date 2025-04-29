import argparse
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import tensorflow as tf
from tensorflow.keras import layers
import pandas as pd
import time
import numpy as np


start = time.time()

parser = argparse.ArgumentParser()

parser.add_argument(
    "--abstracts",
    type=str,
    required=True,
    help="an path for csv abstracts ",
)
args = parser.parse_args()

print("ParseTime:       ", (time.time() - start))


words = (int)(args.abstracts.split("embedded_")[1].split("_")[0])
start = time.time()
A = tf.convert_to_tensor(pd.read_csv(args.abstracts, header=0))

print(A.shape)
embedding_layer = tf.keras.layers.Embedding(words+1, 300, dtype=tf.float64)

dense = layers.Dense(
    1000, activation="relu", input_shape=(300 * A.shape[1],), dtype=tf.float64
)


print("embedding Alloc: ", (time.time() - start))

start = time.time()
for i in range(10):
    start = time.time()
    res = embedding_layer(A)
    res2 = tf.reshape(res, [res.shape[0], res.shape[1] * res.shape[2]])
    res3 = dense(res2)
    print("embed:           ", (time.time() - start))
    start = time.time()


colSum = tf.reduce_sum(res3) / np.sum(res3.shape)
print(colSum)
print("colsum           ", (time.time() - start))
start = time.time()
