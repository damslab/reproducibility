import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import random
import time
device = "cuda" #"cuda" or "cpu"

# Define the scoring feedforward model
class ScoringModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(ScoringModel, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.relu1 = nn.ReLU()
        self.layer2 = nn.Linear(hidden_size, hidden_size)
        self.relu2 = nn.ReLU()
        self.layer3 = nn.Linear(hidden_size, hidden_size)
        self.relu3 = nn.ReLU()
        self.output_layer = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.relu1(self.layer1(x))
        x = self.relu2(self.layer2(x))
        x = self.relu3(self.layer3(x))
        x = self.output_layer(x)
        return x

# Read data
data = pd.read_csv("../datasets/E2G_WMT14.csv", header=None)
#data = data[0:5000:] #subset for testing
nDistincts = 50000    #distinct word count
meta = pd.read_csv("../datasets/words_dictionary2_1.csv", header=None)
meta_ger = pd.read_csv("../datasets/german_vocab2.csv", header=None)
W = pd.read_csv("../datasets/word_embeddings2_1.csv", header=None)

# Initialize weights and biases
input_size = W.shape[1]
hidden_size = 64
output_size = meta_ger.shape[0]

# Create the model
scoring_model = ScoringModel(input_size, hidden_size, output_size).double()
print(scoring_model)
# Move the model to GPU
scoring_model.to(device)
W_gpu = torch.tensor(W.values, dtype=torch.float64).to(device)

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
    # Simulate recode and repetition
    idx = random.randint(0, nDistincts) 

    # Index out the corresponding embedding
    X_batch = W_gpu[idx, :].view(1, -1)
    #print(X_batch[:,0:1])
    X_batch.to(device)

    # Pass the embedding to the feedforward network
    prob_dist = scoring_model(X_batch)

    # Find the most probable German word
    index_ger = torch.argmax(prob_dist, dim=1).cpu().numpy()[0]
    word_ger = meta_ger.iloc[index_ger, 0]

    iter += 1
    beg = end

print(word_ger)
print("Total time for translation = %s sec" % (time.time() - t1))

