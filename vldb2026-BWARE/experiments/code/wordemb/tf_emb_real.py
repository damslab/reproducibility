import argparse
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import tensorflow as tf
import pandas as pd
import time


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
embedding_layer = tf.keras.layers.Embedding(words+1, 300, dtype=tf.float64)
print(words)

print("embedding Alloc: ", (time.time() - start))

start = time.time()
for i in range(10):
    start = time.time()
    res = embedding_layer(A)
    print("embed:           ", (time.time() - start))
    start = time.time()


colSum = tf.reduce_sum(res, 1) / res.shape[0]
print(colSum)
print("colsum           ", (time.time() - start))
start = time.time()
