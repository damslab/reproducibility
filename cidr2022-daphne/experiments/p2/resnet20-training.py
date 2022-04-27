"""
This is a revised implementation from Cifar10 ResNet example in Keras:
(https://github.com/keras-team/keras/blob/master/examples/cifar10_resnet.py)
"""

from __future__ import print_function
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping
from tensorflow.keras.callbacks import ReduceLROnPlateau
import resnet_v2
from utils import lr_schedule
import numpy as np
import os
import h5py
import sys
#jit_scope = tf.xla.experimental.jit_scope 
#tf.config.experimental.enable_mlir_bridge()
#tf.config.experimental.enable_mlir_graph_optimization()

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

# Training parameters
batch_size = 256
epochs = 200 
data_augmentation = False
num_classes = 17
subtract_pixel_mean = True  # Subtracting pixel mean improves accuracy
base_model = 'resnet20'
depth = 20 # For ResNet, specify the depth (e.g. ResNet50: depth=50)
# Choose what attention_module to use: cbam_block / se_block / None
#attention_module = 'cbam_block'
attention_module = None

use_xla = False
if "xla" in sys.argv:
  print("using XLA")
  use_xla = True
  tf.config.optimizer.set_jit(True)
else:
  print("NOT using XLA")
  tf.config.optimizer.set_jit(False)

eager_mode = False
if "eager" in sys.argv:
    print("eager mode selected")
    eager_mode = True
    tf.config.run_functions_eagerly(True)
    #tf.data.experimental.enable_debug_mode()
else:
    print("turning OFF eager mode")
    tf.config.run_functions_eagerly(False)
    
datadir=""
matches = [x for x in sys.argv if x[:8] == "datadir="]
if len(matches) == 1:
    datadir=matches[0][8:]
    print(datadir)
else:
    print("need exactly 1 datadir=<path-to-train/test h5 file> argument")
    sys.exit()

dataset=""
matches = [x for x in sys.argv if x[:8] == "dataset="]
if len(matches) == 1:
    dataset=matches[0][8:]
    print(dataset)
else:
    print("need exactly 1 dataset=<dataset name> argument")
    sys.exit()

last_epoch = 0
model_path = ''
matches = [x for x in sys.argv if x[:6] == "model="]
if len(matches) == 1:
    model_path=matches[0][6:]
    print(model_path)
    last_epoch = int(model_path[-6:-3])
    print("Continuing training at epoch " + str(last_epoch))
     
model_type = base_model if attention_module==None else base_model+'_'+attention_module

training_file = datadir + '/training.h5'
fid1 = h5py.File(training_file,'r')

y_train_1hot = np.array(fid1['label'])
x_train = np.array(fid1[dataset])
y_train = (np.argmax(y_train_1hot, axis=1)).reshape(y_train_1hot.shape[0], 1)

validation_file = datadir + '/validation.h5'
fid2 = h5py.File(validation_file,'r')
x_val = np.array(fid2[dataset])
y_val_1hot = np.array(fid2['label'])
y_val = (np.argmax(y_val_1hot, axis=1)).reshape(y_val_1hot.shape[0], 1)

# If subtract pixel mean is enabled
if subtract_pixel_mean:
    x_train_mean = np.mean(x_train, axis=0)
    x_train -= x_train_mean
    x_val_mean = np.mean(x_val, axis=0)
    x_val -= x_val_mean

print('x_train shape:', x_train.shape)
print('y_train shape:', y_train.shape)
print('x_val shape:', x_val.shape)
print('y_val shape:', y_val.shape)


# Convert class vectors to binary class matrices.
y_train = keras.utils.to_categorical(y_train, num_classes)
y_val = keras.utils.to_categorical(y_val, num_classes)

train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(batch_size)
val_dataset = tf.data.Dataset.from_tensor_slices((x_val, y_val)).batch(batch_size)

# Open a strategy scope.
#@tf.function(jit_compile=True)
def xla_training(input_shape, depth, attention_module, num_classes):
    #with jit_scope():
        model = resnet_v2.resnet_v2(input_shape=input_shape, depth=depth, attention_module=attention_module, num_classes=num_classes)   
        model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=lr_schedule(0)), metrics=['accuracy'])
        model.summary()
        return model
    

if(model_path == ''):
    model = xla_training(x_train.shape[1:], depth, attention_module, num_classes)
else:
    model = tf.keras.models.load_model(model_path)

# Prepare model model saving directory.
save_dir = os.path.join(os.getcwd(), 'saved_models')
model_name = dataset + '_%s_model.{epoch:03d}.h5' % model_type
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)
filepath = os.path.join(save_dir, model_name)

# Prepare callbacks for model saving and for learning rate adjustment.
checkpoint = ModelCheckpoint(filepath=filepath, monitor='val_accuracy', verbose=1, save_best_only=True)
earlystopping = EarlyStopping(monitor='val_accuracy', baseline=0.8, patience=5, verbose=1)
lr_scheduler = LearningRateScheduler(lr_schedule)
lr_reducer = ReduceLROnPlateau(factor=np.sqrt(0.1), cooldown=0, patience=5, min_lr=0.5e-6)
#callbacks = [checkpoint, lr_reducer, lr_scheduler, earlystopping]
callbacks = [checkpoint, lr_reducer, lr_scheduler]

# model.fit(x_train, y_train,
model.fit(train_dataset,
    batch_size=batch_size,
    epochs=epochs,
    # validation_data=(x_val, y_val),
    validation_data=val_dataset,
    shuffle=True,
    callbacks=callbacks,
    initial_epoch=last_epoch)

#print(xla_training.experimental_get_compiler_ir(x_train, y_train)(stage='hlo'))
