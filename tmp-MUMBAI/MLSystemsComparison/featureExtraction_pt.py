# Use double-precision for fairness
# torch.compile decorator on predict_model is significantly slower

import torch
import torch.nn as nn
import pandas as pd
import time
import numpy as np
from torch.utils.data import Dataset
from torchvision import transforms
import torchvision.models as models
device = "cuda" #"cuda" or "cpu"

def freeze_layers(model, num_layers):
    # Freeze the weights of the specified #layers
    for i, param in enumerate(model.parameters()):
        if i < num_layers:
            param.requires_grad = False
        else:
            break
    return model


# Define a custom dataset class with random data
class RandomDataset(Dataset):
    def __init__(self, num_samples, transform=None):
        self.num_samples = num_samples
        self.transform = transform

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        # Generate random data with the same size as ImageNet images
        #random_data = torch.randn(3, 224, 224)                     #single-precision
        random_data = torch.randn(3, 224, 224, dtype=torch.double) #double-precision
        random_data = random_data.to("cuda")
        return random_data

#@torch.compile
def predict_model(model, dataset, batch_size):
    # Forward pass batch-wise 
    Y_pred = []
    t1 = time.time()
    for i in range(0, len(dataset), batch_size):
        beg = i
        end = min(i + batch_size, len(dataset))
        # Get the current mini-batch
        mini_batch = [dataset[j] for j in range(beg, end)]
        mini_batch = torch.stack(mini_batch).to(device)
        predictions = model(mini_batch)
        # Get the predicted classes 
        _, predicted_classes = torch.max(predictions, 1)
        Y_pred.append(predicted_classes)
        del mini_batch, predictions #release memory

    Y_pred_tensor = torch.cat(Y_pred)
    print("Predict time for model = %s sec" % (time.time() - t1))
    print("Shape of Predicted Classes Tensor:", Y_pred_tensor.shape)
    return Y_pred_tensor

# Create random images of imagenet size
count = 10000 #10000
dataset = RandomDataset(num_samples=count, transform=transforms.ToTensor())
batch_size = 64

# Freeze and extract top 3 layers of AlexNet
model = models.alexnet(weights='AlexNet_Weights.DEFAULT').double()
t1 = time.time()
for i in range(1, 5):
    alexnet = freeze_layers(model, i)
    # Move the model to GPU
    alexnet.to(device)
    Y_pred1 = predict_model(alexnet, dataset, batch_size)
    # Copy the results back to host
    Y_np1 = Y_pred1.detach().cpu().numpy()
print(Y_np1.shape)
print(Y_pred1.device)
print("Total time for AlexNet = %s sec" % (time.time() - t1))
# Clear the allocation cache to avoid OOM
torch.cuda.empty_cache()

# Freeze and extract top 3 layers of VGG16
model = models.vgg16(weights='VGG16_Weights.DEFAULT').double()
t1 = time.time()
for i in range(1, 4):
    vgg16 = freeze_layers(model, i)
    # Move the model to GPU
    vgg16.to(device)
    Y_pred2 = predict_model(vgg16, dataset, batch_size)
    # Copy the results back to host
    Y_np2 = Y_pred2.detach().cpu().numpy()
print(Y_np2.shape)
print(Y_pred2.device)
print("Total time for VGG16 = %s sec" % (time.time() - t1))
# Clear the allocation cache to avoid OOM
torch.cuda.empty_cache()

# Freeze and extract top 4 layers of ResNet18

model = models.resnet18(weights='ResNet18_Weights.DEFAULT').double()
t1 = time.time()
for i in range(1, 4):
    resnet18 = freeze_layers(model, i)
    # Move the model to GPU
    device = "cuda" #"cuda" or "cpu"
    resnet18.to(device)
    Y_pred3 = predict_model(resnet18, dataset, batch_size)
    # Copy the results back to host
    Y_np3 = Y_pred3.detach().cpu().numpy()
print(Y_np3.shape)
print(Y_pred3.device)
print("Total time for ResNet18 = %s sec" % (time.time() - t1))

