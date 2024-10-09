# Call: python featureExtraction.py imagenet (or cifar)
# Double-precision is 19x slower than single-precision
# torch.compile decorator on predict_model slows down ~10x and causes OOM

import torch
import torch.nn as nn
import pandas as pd
import time
import sys
import numpy as np
from torch.utils.data import Dataset
from torchvision import transforms
import torchvision.models as models

# Define AlexNet for CIFAR-10 (32x32 images)
class AlexNetCIFAR(nn.Module):
    def __init__(self, num_classes=10):
        super(AlexNetCIFAR, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(64, 192, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(192, 384, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(256 * 4 * 4, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), 256 * 4 * 4)
        x = self.classifier(x)
        return x

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
    def __init__(self, num_samples, transform, setName):
        self.num_samples = num_samples
        self.transform = transform
        self.setName = setName

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        # Generate random data with the same size as ImageNet images
        #random_data = torch.randn(3, 224, 224)                     #single-precision
        if setName == 'cifar':
            random_data = torch.randn(3, 32, 32, dtype=torch.double) #double-precision
        if setName == 'imagenet':
            random_data = torch.randn(3, 224, 224, dtype=torch.double) #double-precision
        random_data = random_data.to("cuda")
        return random_data

@torch.compile
def predict_model(model, dataset, batch_size):
    # Forward pass batch-wise 
    Y_pred = []
    device = "cuda" #"cuda" or "cpu"
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

# Get the dataset name to be used
setName = sys.argv[1] #cifar or imagenet

# Create random images of imagenet size
count = 10000 #10000
dataset = RandomDataset(num_samples=count, transform=transforms.ToTensor(), setName=setName)
batch_size = 64

# Freeze and extract top 3 layers of AlexNet
if setName == 'cifar':
    model = AlexNetCIFAR().double()
if setName == 'imagenet':
    model = models.alexnet(weights='AlexNet_Weights.DEFAULT').double()
t1 = time.time()
for i in range(1, 5):
    alexnet = freeze_layers(model, i)
    # Move the model to GPU
    device = "cuda" #"cuda" or "cpu"
    alexnet.to(device)
    Y_pred1 = predict_model(alexnet, dataset, batch_size)
    # Copy the results back to host
    Y_np1 = Y_pred1.detach().cpu().numpy()
print(Y_np1.shape)
print(Y_pred1.device)
print("Total time for AlexNet = %s sec" % (time.time() - t1))

# Freeze and extract top 3 layers of VGG16
model = models.vgg16(weights='VGG16_Weights.DEFAULT').double()
t1 = time.time()
for i in range(1, 4):
    vgg16 = freeze_layers(model, i)
    # Move the model to GPU
    device = "cuda" #"cuda" or "cpu"
    vgg16.to(device)
    Y_pred2 = predict_model(vgg16, dataset, batch_size)
    # Copy the results back to host
    Y_np2 = Y_pred2.detach().cpu().numpy()
print(Y_np2.shape)
print(Y_pred2.device)
print("Total time for VGG16 = %s sec" % (time.time() - t1))

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

