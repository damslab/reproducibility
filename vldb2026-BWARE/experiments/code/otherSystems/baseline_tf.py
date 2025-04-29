import warnings
warnings.filterwarnings('ignore') #cleaner, but not recommended
import pandas as pd
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
import tensorflow as tf
import json
import sys
import time 
import numpy as np

tf.config.set_visible_devices([], 'GPU')

t1 = time.time()

data_path = sys.argv[1]
spec_path = sys.argv[2]
header = (int) (sys.argv[3])
delim = sys.argv[4]
if(delim == "t"):
    delim = "\t"
if header == 0:
    header = None

with open(data_path, 'r') as f:
    spec = json.load(f)
print(f"specTime: {time.time() - t1} sec")
data = pd.read_csv(spec_path, header=header, delimiter= delim)
print(f"readTime: {time.time() - t1} sec")

dummy_spec = list(data.columns[[i-1 for i in spec["dummycode"]]])

dummyColumns = data[dummy_spec]

tmp_tensors = []
ones = tf.ones([data.shape[0]], tf.dtypes.float64 )
rows = tf.range(0, data.shape[0], dtype = tf.dtypes.int64)
zeros = tf.zeros(shape =[ data.shape[0]], dtype = tf.dtypes.int64)
zeros = tf.stack([rows, zeros], axis=1)

for col in data.columns:
    if col in dummy_spec:
        recoded, values = pd.factorize(data[col])
        recoded = tf.constant(recoded, shape=[data.shape[0]])
        indices = tf.stack([rows, recoded], axis=1)
        tmp = tf.SparseTensor(indices = indices,
            values=ones, dense_shape=[data.shape[0], len(values)] )
        tmp_tensors.append(tmp)
    else:
        d = tf.constant(data[col], shape=[data.shape[0]], dtype=tf.dtypes.float64)
        tmp = tf.SparseTensor(indices = zeros,
            values=d, dense_shape=[data.shape[0], 1] )
        tmp_tensors.append(tmp)
        
print(f"BeforeCombine: {time.time() - t1} sec")

res = tf.sparse.concat(axis=1, sp_inputs=tmp_tensors)
print(res.shape)

print(f"endTime: {time.time() - t1} sec")