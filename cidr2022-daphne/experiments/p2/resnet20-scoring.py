"""
This is a revised implementation from Cifar10 ResNet example in Keras:
(https://github.com/keras-team/keras/blob/master/examples/cifar10_resnet.py)
"""

from __future__ import print_function
import tensorflow as tf
#import keras
import tensorflow.keras as keras
from tensorflow.keras.layers import Dense, Conv2D, BatchNormalization, Activation
from tensorflow.keras.layers import AveragePooling2D, Input, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, LearningRateScheduler
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.regularizers import l2
from tensorflow.keras import backend as K
from tensorflow.keras.models import Model

import resnet_v2
import numpy as np
import pandas as pd
import os
import h5py
import sys
import time

if len(sys.argv) < 3:
    print("usage: " + sys.argv[0] + " <images=fname> <labels=fname> <model=fname> [xla] [eager]")
    sys.exit()

use_xla = False
if "xla" in sys.argv:
  print("using XLA")
  use_xla = True
  tf.config.optimizer.set_jit(True)
else:
  print("NOT using XLA")
      
eager_mode = False
if "eager" in sys.argv:
    #print("eager mode selected")
    eager_mode = True
    #tf.config.run_functions_eagerly(True)
    #tf.data.experimental.enable_debug_mode()
else:
    #tf.config.run_functions_eagerly(False)
    tf.compat.v1.disable_eager_execution()    
    #print("turning OFF eager mode")
print("Eager execution is ", end="")
print("ON" if tf.executing_eagerly() else "OFF")
batch_size = 128
matches = [x for x in sys.argv if x[:11] == "batch_size="]
if len(matches) == 1:
    batch_size=int(matches[0][11:])
    print("Setting batch size to " + str(batch_size))

images= ""
matches = [x for x in sys.argv if x[:7] == "images="]
if len(matches) == 1:
    images=matches[0][7:]
    print(images)
else:
    print("need exactly 1 images=<path-to-csv-file> argument")
    sys.exit()

labels= ""
matches = [x for x in sys.argv if x[:7] == "labels="]
if len(matches) == 1:
    labels=matches[0][7:]
    print(labels)
else:
    print("need exactly 1 labels=<path-to-csv-file> argument")
    sys.exit()
    
model_path = ''
matches = [x for x in sys.argv if x[:6] == "model="]
if len(matches) == 1:
    model_path=matches[0][6:]
    print(model_path)
else:
    print("need exactly 1 model=<path-to-h5-file> argument")
    sys.exit()
    
model = tf.keras.models.load_model(model_path)

# timed data loading
t_start = time.perf_counter_ns()

# prepare images
dfx=pd.read_csv(images, low_memory=False, memory_map=True, engine='c', dtype=np.float32)
dfy=pd.read_csv(labels, low_memory=False, memory_map=True, engine='c', dtype=np.float32)

#x_test = np.moveaxis(dfx.values, -1, 1).reshape(-1,32,32,10) # TF wants NHWC
x_test = dfx.values.reshape(-1,32,32,10)
keras.backend.set_image_data_format('channels_first')
# prepare labels

y_test_1hot = dfy.values.reshape(-1,17)
num_classes = y_test_1hot.shape[1]
y_test = (np.argmax(y_test_1hot, axis=1)).reshape(y_test_1hot.shape[0], 1)
y_test = keras.utils.to_categorical(y_test, num_classes)
test_dataset = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(batch_size)
t_load_end = time.perf_counter_ns() 
duration = t_load_end - t_start

print("Data load duration=" + str(duration) + "ns")
print('x_test shape:', x_test.shape)
print('y_test shape:', y_test.shape)

# perform scoring
start = time.perf_counter_ns()

#ds_end = time.perf_counter_ns()
scores = model.evaluate(test_dataset, verbose=0)
#scores = model.evaluate(x_test, y_test, verbose=0)
duration = time.perf_counter_ns() - start
#print("dataset building duration=" + str(ds_end - start) + "ns")
print("inference duration=" + str(duration) + "ns")
print('Loss:', scores[0])
print('Accuracy:', scores[1])
