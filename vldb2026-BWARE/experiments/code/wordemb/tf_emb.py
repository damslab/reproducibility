import argparse
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import tensorflow as tf
import time


start = time.time()

parser = argparse.ArgumentParser()
parser.add_argument(
    "--words", type=int, required=True, help="an integer for how many words to use"
)
parser.add_argument(
    "--abstracts",
    type=int,
    required=True,
    help="an integer for how many abstracts to use",
)
args = parser.parse_args()

print("ParseTime:       ", (time.time() - start))
start = time.time()
A = tf.random.uniform(
    shape=(args.abstracts, args.abstractlength), minval=1, maxval=args.words, dtype=tf.int32
)
embedding_layer = tf.keras.layers.Embedding(args.words, 300, dtype=tf.float64)
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
