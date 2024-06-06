# Using TF 2.2 for compatibality with Cuda 10.2 (MEMPHIS/SystemDS needs Cuda 10.2).
# TF 2.2 needs Cuda 10.1. Use soft links to map Cuda 10.1 to Cuda 10.2
# FIXME: GPU is not utilized. Probably due to compatibility issues.
# CPU and GPU are taking the same time

import tensorflow as tf
#tf.config.set_visible_devices([], 'GPU') #hide GPU for CPU-only execution
from tensorflow.keras import layers, models
from tensorflow.keras.applications.vgg16 import VGG16
from keras import backend as K
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
import time
tf.config.threading.set_inter_op_parallelism_threads(1)
K.set_floatx('float64')

def alexnet(input_shape=(224, 224, 3), num_classes=1000):
    model = models.Sequential()
    model.add(layers.Conv2D(96, (11, 11), strides=(4, 4), input_shape=input_shape, activation='relu'))
    model.add(layers.MaxPooling2D((3, 3), strides=(2, 2)))
    model.add(layers.Conv2D(256, (5, 5), padding='same', activation='relu'))
    model.add(layers.MaxPooling2D((3, 3), strides=(2, 2)))
    model.add(layers.Conv2D(384, (3, 3), padding='same', activation='relu'))
    model.add(layers.Conv2D(384, (3, 3), padding='same', activation='relu'))
    model.add(layers.Conv2D(256, (3, 3), padding='same', activation='relu'))
    model.add(layers.MaxPooling2D((3, 3), strides=(2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dense(num_classes, activation='softmax'))
    return model

def resnet18(input_shape=(224, 224, 3), num_classes=1000):
    input_tensor = layers.Input(shape=input_shape)
    x = layers.Conv2D(64, (7, 7), strides=(2, 2), padding='same', activation='relu')(input_tensor)
    x = layers.MaxPooling2D((3, 3), strides=(2, 2), padding='same')(x)

    x = residual_block(x, 64)
    x = residual_block(x, 64)
    x = residual_block(x, 128, downsample=True)
    x = residual_block(x, 128)
    x = residual_block(x, 256, downsample=True)
    x = residual_block(x, 256)
    x = residual_block(x, 512, downsample=True)
    x = residual_block(x, 512)

    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(num_classes, activation='softmax')(x)

    model = models.Model(inputs=input_tensor, outputs=x)
    return model

def residual_block(x, filters, downsample=False):
    identity = x

    x = layers.Conv2D(filters, (3, 3), strides=(1 if not downsample else 2, 1 if not downsample else 2), padding='same', activation='relu')(x)
    x = layers.Conv2D(filters, (3, 3), padding='same', activation='relu')(x)

    if downsample:
        identity = layers.Conv2D(filters, (1, 1), strides=(2, 2), padding='valid', activation='relu')(identity)

    x = layers.add([x, identity])
    return x

def freeze_layers(model, nFreeze):
    # Freeze the weights of the specified #layers
    #weights = model.layers[1].get_weights()
    #print("Model parameters' datatype: ", weights[0].dtype)
    nLayers = len(model.layers)
    for i, layer in enumerate(model.layers):
        if i < nLayers - nFreeze:
            layer.trainable = False
        else:
            layer.trainable = True
    #print("Trainable weights: ",len(model.trainable_weights))
    #print("Non-trainable weights: ",len(model.non_trainable_weights))
    return model

# Define a custom dataset class with random data
class RandomDataset(tf.keras.utils.Sequence):
    def __init__(self, num_samples, batch_size):
        self.num_samples = num_samples
        self.batch_size = batch_size

    def __len__(self):
        return int(np.ceil(self.num_samples / self.batch_size))

    def __getitem__(self, idx):
        # Generate random data with the same size as ImageNet images
        random_data = np.random.randn(self.batch_size, 224, 224, 3)
        random_data = preprocess_input(random_data)
        return random_data

def predict_model(model, dataset, batch_size):
    # Forward pass batch-wise
    Y_pred = []
    t1 = time.time()
    for i in range(len(dataset)):
        mini_batch = dataset[i]
        predictions = model.predict(mini_batch)  #Keras way. Returns numpy array
        #predictions = model(mini_batch, training=False).numpy() #TF way. Returns tensor
        # Get the predicted classes
        predicted_classes = np.argmax(predictions, axis=1)
        Y_pred.append(predicted_classes)
    
    Y_pred_array = np.concatenate(Y_pred)
    print("Predict time for model = %s sec" % (time.time() - t1))
    print("Shape of Predicted Classes Array:", Y_pred_array.shape)
    return Y_pred_array

# Enable memory growth (instead of pre-allocating full memory)
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

# Create random images of ImageNet size
count = 10000 #10000
batch_size = 64 
dataset = RandomDataset(num_samples=count, batch_size=batch_size)

# Freeze and extract top 4 layers of AlexNet
alex = alexnet()
t1 = time.time()
for i in range(1, 5):
    alex = freeze_layers(alex, i)
    Y_pred1 = predict_model(alex, dataset, batch_size)
print(Y_pred1.shape)
print("Total time for AlexNet = %s sec" % (time.time() - t1))

# Freeze and extract top 3 layers of VGG16
vgg16 = VGG16(weights='imagenet')
t1 = time.time()
for i in range(1, 4):
    vgg16 = freeze_layers(vgg16, i)
    Y_pred2 = predict_model(vgg16, dataset, batch_size)
print(Y_pred2.shape)
print("Total time for VGG16 = %s sec" % (time.time() - t1))

# Freeze and extract top 3 layers of ResNet18
resnet = resnet18()
t1 = time.time()
for i in range(1, 4):
    resnet = freeze_layers(resnet, i)
    Y_pred3 = predict_model(resnet, dataset, batch_size)
print(Y_pred3.shape)
print("Total time for ResNet18 = %s sec" % (time.time() - t1))

