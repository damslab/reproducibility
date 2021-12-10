

import tensorflow as tf

from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Dropout
from tensorflow.keras import Model

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

batchSize = 128
floatSize = "float64"
EPOCHS = 2
print(x_train.shape)
print("Batch size: " + str(batchSize))
print("floatSize: " + floatSize)
tf.keras.backend.set_floatx(floatSize)

# Add a channels dimension
x_train = x_train[..., tf.newaxis].astype(floatSize)
x_test = x_test[..., tf.newaxis].astype(floatSize)

train_ds = tf.data.Dataset.from_tensor_slices(
    (x_train, y_train)).shuffle(10000).batch(batchSize)

test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(batchSize)


class MyModel(Model):
    # input -> conv1 -> relu1 -> pool1 -> conv2 -> relu2 -> pool2
    # -> affine3 -> relu3 -> affine4 -> softmax
    def __init__(self):
        super(MyModel, self).__init__()
        self.conv1 = Conv2D(32, 5, padding="same", activation='relu')
        self.mp1 = MaxPool2D((2, 2))
        self.conv2 = Conv2D(64, 5, padding="same", activation='relu')
        self.flatten = Flatten()
        self.d1 = Dense(512, activation='relu')
        self.d2 = Dense(10)
        self.dropout_layer = Dropout(rate=0.5)

    def call(self, x, training=None):
        x = self.conv1(x)
        # print(x.shape)
        x = self.mp1(x)
        # print(x.shape)
        x = self.conv2(x)
        # print(x.shape)
        x = self.mp1(x)
        x = self.flatten(x)
        # print(x.shape)
        x = self.d1(x)
        # print(x.shape)
        x = self.dropout_layer(x)
        return self.d2(x)


# Create an instance of the model
model = MyModel()

loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

optimizer = tf.keras.optimizers.Adam()

train_loss = tf.keras.metrics.Mean(name='train_loss')
train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(
    name='train_accuracy')

test_loss = tf.keras.metrics.Mean(name='test_loss')
test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(
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
