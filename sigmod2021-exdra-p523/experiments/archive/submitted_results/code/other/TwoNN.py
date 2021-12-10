

import tensorflow as tf

from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPool2D
from tensorflow.keras import Model
from sklearn.model_selection import train_test_split
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-x', '--datapath', type=str, required=True)
parser.add_argument('-y', '--labels', type=str, required=True)
parser.add_argument('-v', '--verbose', type=bool,   default=False)
parser.add_argument('-o', '--outputpath', type=str,  required=True)
args = parser.parse_args()

X = np.load(args.datapath, allow_pickle=True)
Y = np.load(args.labels, allow_pickle=True)


# Add a channels dimension
X = X[..., tf.newaxis].astype("float32")
Y = Y[..., tf.newaxis].astype("float32")

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=42)


train_ds = tf.data.Dataset.from_tensor_slices(
    (X_train, y_train)).shuffle(10000).batch(128)

test_ds = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(128)

class MyModel(Model):
    # input -> affine1 -> relu1 -> affine2 -> relu2 -> affine3 -> softmax
    def __init__(self):
        super(MyModel, self).__init__()
        self.flatten = Flatten()
        self.d1 = Dense(200, activation='relu')
        self.d2 = Dense(200, activation='relu')
        self.d3 = Dense(1)

    def call(self, x, training=None):
        x = self.flatten(x)
        x = self.d1(x)
        x = self.d2(x)
        return self.d3(x)


# Create an instance of the model
model = MyModel()

loss_object = tf.keras.losses.MeanAbsoluteError()

optimizer = tf.keras.optimizers.SGD()

train_loss = tf.keras.metrics.Mean(name='train_loss')
train_accuracy = tf.keras.metrics.MeanAbsoluteError(
    name='train_accuracy')

test_loss = tf.keras.metrics.Mean(name='test_loss')
test_accuracy = tf.keras.metrics.MeanAbsoluteError(
    name='test_accuracy')


@tf.function
def train_step(images, labels):
    with tf.GradientTape() as tape:
        # training=True is only needed if there are layers with different
        # behavior during training versus inference (e.g. Dropout).
        predictions = model(images, training=True)
        loss = loss_object(labels, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    train_loss(loss)
    train_accuracy(labels, predictions)


@tf.function
def test_step(images, labels):
    # training=False is only needed if there are layers with different
    # behavior during training versus inference (e.g. Dropout).
    predictions = model(images, training=False)
    t_loss = loss_object(labels, predictions)

    test_loss(t_loss)
    test_accuracy(labels, predictions)


EPOCHS = 5

for epoch in range(EPOCHS):
    # Reset the metrics at the start of the next epoch
    train_loss.reset_states()
    train_accuracy.reset_states()
    test_loss.reset_states()
    test_accuracy.reset_states()

    for images, labels in train_ds:
        train_step(images, labels)

    for test_images, test_labels in test_ds:
        test_step(test_images, test_labels)

    print(
        f'Epoch {epoch + 1}, '
        f'Loss: {train_loss.result()}, '
        f'Accuracy: {train_accuracy.result() * 100}, '
        f'Test Loss: {test_loss.result()}, '
        f'Test Accuracy: {test_accuracy.result() * 100}'
    )
