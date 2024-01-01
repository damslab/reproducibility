# Using TF 2.2 for compatibality with Cuda 10.2 (MUMBAI/SystemDS needs Cuda 10.2).
# TF 2.2 needs Cuda 10.1. Use soft links to map Cuda 10.1 to Cuda 10.2
# FIXME: GPU is not utilized. Probably due to compatibility issues.
# CPU and GPU are taking the same time. 10 hours for 200K words

import tensorflow as tf
#tf.config.set_visible_devices([], 'GPU') #hide GPU for CPU-only execution
from tensorflow.keras import layers, models
import pandas as pd
import numpy as np
import time

# Enable memory growth (instead of pre-allocating full memory)
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

# Define the scoring feedforward function
def build_scoring_model(input_size, hidden_size, output_size):
    model = models.Sequential([
        layers.Dense(hidden_size, activation='relu', input_shape=(input_size,), dtype='float64'),
        layers.Dense(hidden_size, activation='relu', dtype='float64'),
        layers.Dense(hidden_size, activation='relu', dtype='float64'),
        layers.Dense(output_size, dtype='float64')
    ])

    return model

# Read data
data = pd.read_csv("../datasets/E2G_WMT14.csv", header=None)
#data = data[0:1000:]
meta = pd.read_csv("../datasets/words_dictionary2_1.csv", header=None)
meta_ger = pd.read_csv("../datasets/german_vocab2.csv", header=None)
W = pd.read_csv("../datasets/word_embeddings2_1.csv", header=None)

# Initialize weights and biases
input_size = W.shape[1]
hidden_size = 64
output_size = meta_ger.shape[0]
# Create the model
scoring_model = build_scoring_model(input_size, hidden_size, output_size)
print(scoring_model.summary())

# Mini-batch processing
batch_size = 1
nrow_data = data.shape[0]
num_iters = int(np.ceil(nrow_data / batch_size))
beg = 0

# Loop through mini-batches
iter = 0
print("Starting scoring iteration")
t1 = time.time()
while iter < num_iters:
    end = beg + batch_size
    if end > nrow_data:
        end = nrow_data
    batch = data.iloc[beg:end, :]

    # Get the recoded value for this word
    #idx = batch[0].apply(lambda x: meta[1][x - 1])
    #idx = idx.replace(np.nan, 6537)  # Replace NaN with 6537
    idx = 5

    # Index out the corresponding embedding
    X_batch = W.iloc[idx,:].values.reshape(1, -1)
    #print(X_batch[:,0:1])

    # Pass the embedding to the feedforward network
    prob_dist = scoring_model.predict(X_batch)

    # Find the most probable German word
    index_ger = tf.argmax(prob_dist, axis=1).numpy()[0]
    word_ger = meta_ger.iloc[index_ger, 0]

    iter += 1
    beg = end

print(word_ger)
print("Total time for translation = %s sec" % (time.time() - t1))

