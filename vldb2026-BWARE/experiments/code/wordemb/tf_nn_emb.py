import argparse
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import tensorflow as tf
from tensorflow.keras import layers
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

parser.add_argument(
    "--abstractlength",
      type=int,
    required=True,
    help="an integer for how long abstracts are",
)
args = parser.parse_args()
tf.random.set_seed(
    32
)


print("ParseTime:       ", (time.time() - start))
start = time.time()
A = tf.random.uniform(
    shape=(args.abstracts, args.abstractlength), minval=1, maxval=args.words, dtype=tf.int32
)

embedding_layer = layers.Embedding(args.words, 300, dtype=tf.float64)
dense = layers.Dense(
    1000, activation="relu", input_shape=(300 * args.abstractlength,), dtype=tf.float64
)

print("embedding Alloc: ", (time.time() - start))
start = time.time()
for i in range(10):
    start = time.time()
    res = embedding_layer(A)
    res = tf.reshape(res, [args.abstracts, args.abstractlength * 300])
    print(res.shape)
    res2 = dense(res)
    print(res2.shape)
    print("embed:           ", (time.time() - start))
    start = time.time()


colSum = tf.reduce_sum(res) / sum(res.shape)
print(colSum)
print("average           ", (time.time() - start))
start = time.time()
