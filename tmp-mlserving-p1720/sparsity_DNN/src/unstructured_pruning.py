from transformers import AutoImageProcessor, ResNetForImageClassification
import torch
from PIL import Image
import torch 
import os
import numpy as np
import pickle
import torch.nn.utils.prune as prune
import torch.nn as nn
import random
from imagenet_classes import IMAGENET2012_CLASSES
from torchvision import datasets
from torch.utils.data import DataLoader, ConcatDataset, SubsetRandomSampler
from tqdm import tqdm
import time
from copy import deepcopy
import pandas as pd
import statistics
import heapq

class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, img_dir, transform=None):
        self.img_labels = os.listdir(img_dir)
        self.img_dir = img_dir
        self.transform = transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels[idx])
        
        image = Image.open(img_path)
        if image.mode != 'RGB':
            image = image.convert("RGB")
        true_class = img_path.split(sep='_')[-1].split(sep='.')[0]
        label = list(IMAGENET2012_CLASSES.keys()).index(true_class)
        if self.transform:
            image = self.transform(image, return_tensors="pt")
        return image["pixel_values"], label

class TrainingSampler:

    def __init__(self, imagenet_folder, sample_percentage, workers) -> None:
        self.sample_percentage = sample_percentage
        self.preprocessor = AutoImageProcessor.from_pretrained("microsoft/resnet-50")
        # Paths to the folders containing ImageNet samples
        self.imagenet_folder = imagenet_folder
        
        self.folders = [
            os.path.join(os.path.expanduser(self.imagenet_folder), 'train_images_0'),
            os.path.join(os.path.expanduser(self.imagenet_folder), 'train_images_1'),
            os.path.join(os.path.expanduser(self.imagenet_folder), 'train_images_2'),
            os.path.join(os.path.expanduser(self.imagenet_folder), 'train_images_3'),
            os.path.join(os.path.expanduser(self.imagenet_folder), 'train_images_4')
        ]
        self.workers = workers

    def sample(self, batch_size):

        # Load datasets from each folder and concatenate them
        datasets_list = []
        for folder in self.folders:
            datasets_list.append(CustomDataset(img_dir=folder, transform=self.preprocessor))

        # Combine all datasets
        combined_dataset = ConcatDataset(datasets_list)

        if self.sample_percentage < 1:
            # Total number of samples
            dataset_size = len(combined_dataset)

            # Define the x% size
            subset_size = int(self.sample_percentage * dataset_size)

            # Randomly shuffle indices
            indices = np.random.permutation(dataset_size)

            # Take the first subset_size indices for sampling
            subset_indices = indices[:subset_size]

            # Create the sampler
            sampler = SubsetRandomSampler(subset_indices)

            train_loader = DataLoader(
                combined_dataset,
                batch_size=batch_size,
                sampler=sampler,  # Use sampler instead of shuffle=True
                num_workers=self.workers
            )
        else:
            train_loader = DataLoader(
                combined_dataset,
                batch_size=batch_size,
                shuffle=True,  # Shuffles the combined dataset
                num_workers=self.workers
            )

        return train_loader


class Pruner:
    
    def __init__(self, model_name, percentage, model, training_sample, cores, batch_size, write_path, imagenet_path) -> None:
        self.percentage = percentage
        self.prunned_model = deepcopy(model)
        self.original_model = deepcopy(model)
        self.training_sample = training_sample
        self.cores = cores
        self.batch_size = batch_size
        self.write_path = write_path
        self.imagenet_path = imagenet_path
        self.model_name = model_name
    
    # Define a function for global unstructured pruning
    def global_unstructured_pruning(self):
        # Collect all prunable parameters (weights in Conv2d and Linear layers)
        prunable_params = []
        for name, module in self.prunned_model.named_modules():
            if isinstance(module, (torch.nn.Conv2d, torch.nn.Linear)):
                prunable_params.append((module, "weight"))
        
        # Apply global unstructured pruning
        prune.global_unstructured(
            parameters=prunable_params,
            pruning_method=prune.L1Unstructured,
            amount=self.percentage,  # Fraction of total weights to prune globally
        )

        # Remove pruning reparameterization to make pruning permanent
        for name, module in self.prunned_model.named_modules():
            if isinstance(module, (torch.nn.Conv2d, torch.nn.Linear)):
                prune.remove(module, "weight")

    # Step 2: Define a function to prune all layers
    # def prune_model(self):
        
    #     for name, module in self.prunned_model.named_modules():
    #         # Prune only for layers with weights
    #         if isinstance(module, (nn.Conv2d, nn.Linear)):
    #             prune.l1_unstructured(module, name="weight", amount=self.percentage)
    #             prune.remove(module, name="weight")  # Make pruning permanent
        
    def retrain_pruned_model(self):

        training_sampler = TrainingSampler(self.imagenet_path, self.training_sample, self.cores)
        # Step 5: Define loss function and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(self.prunned_model.parameters(), lr=0.01, momentum=0.9, weight_decay=5e-4)

        # Step 6: Fine-tune the pruned model
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.prunned_model.to(device)

        #Training loop
        for epoch in range(2):  # Train for 10 epochs
            self.prunned_model.train()
            running_loss = 0.0
            train_loader = training_sampler.sample(self.batch_size)
            for images, labels in tqdm(train_loader):
                images = images.squeeze(1)
                images, labels = images.to(device), labels.to(device)
                optimizer.zero_grad()
                outputs = self.prunned_model(images)
                # Extract the logits (assuming logits are present in the model's output)
                logits = outputs.logits  # `logits` is the tensor you need for cross-entropy loss
                loss = criterion(logits, labels)
                loss.backward()
                optimizer.step()
                
                running_loss += loss.item()
            print(f"Epoch [{epoch+1}/10], Loss: {running_loss / len(train_loader)}") 
    
    def main(self):

        self.global_unstructured_pruning()
        self.retrain_pruned_model()
        # Step 7: Save the pruned and fine-tuned model
        file_name = 'resnet50_u_prunned_' + str(self.percentage) + '.pth'
        write_path = os.path.join(self.write_path, file_name)
        torch.save(self.prunned_model.state_dict(), write_path)
    
    
    def evaluate_prunning(self, dataloader):
        
        self.prunned_model.eval()
        
        prunned_correct = 0
        total = 0
        latency = []
        with torch.no_grad():
            for inputs, labels in tqdm(dataloader):
                inputs = inputs.squeeze(1)
                start_time = time.time()
                prunned_outputs = self.prunned_model(inputs)
                end_time = time.time() - start_time
                prunned_logits = prunned_outputs.logits
                
                prunned_, prunned_predicted = torch.max(prunned_logits.data, 1)
                total += labels.size(0)
                
                prunned_correct += (prunned_predicted == labels).sum().item()
                latency.append(end_time)
        
        prunned_accuracy = 100 * prunned_correct / total

        
        prunned_results = [self.model_name + '_prunned', 'unstructured', self.percentage, prunned_accuracy, self.batch_size, statistics.mean(latency)]
        
        # prunned_results.append(self.evaluate_batch_latency_prunned(dataloader))

        return prunned_results
    
    def evaluate_original(self, dataloader):

        self.original_model.eval()
        
        original_correct = 0
        total = 0
        latency = []
        with torch.no_grad():
            for inputs, labels in tqdm(dataloader):
                inputs = inputs.squeeze(1)
                start_time = time.time()
                original_outputs = self.original_model(inputs)
                end_time = time.time() - start_time
                latency.append(end_time)
                original_logits = original_outputs.logits
                
                original_, original_predicted = torch.max(original_logits.data, 1)
                
                total += labels.size(0)
                original_correct += (original_predicted == labels).sum().item()
        
        original_accuracy = 100 * original_correct / total

        original_results = [self.model_name + '_original', 'unstructured', self.percentage, original_accuracy, self.batch_size, statistics.mean(latency)]
        
        # original_results.append(self.evaluate_batch_latency_original(dataloader))
        
        
        return original_results
    
if __name__ == '__main__':
    
    # Step 1:Load the ResNet50 model from Hugging Face
    model = ResNetForImageClassification.from_pretrained("microsoft/resnet-50")

    preprocessor = AutoImageProcessor.from_pretrained("microsoft/resnet-50")
    cores = torch.get_num_threads()
    # global_path =  "~/llm_adapt_serving"
    #imagenet_path = "~/inferdb-unstructured/data"
    imagenet_path = "/app/llm_adapt_serving/data"
    global_folder_path = "/app/llm_adapt_serving"
    write_path = os.path.join(os.path.expanduser(global_folder_path), 'data/artifacts')
    test_set = CustomDataset(img_dir=os.path.join(os.path.expanduser(imagenet_path), 'val_images'), 
                             transform=preprocessor)
    test_loader = DataLoader(
                test_set,
                batch_size=cores*16,
                shuffle=True,  # Use sampler instead of shuffle=True
                num_workers=cores
            )
    
    results = []
    for p in np.arange(0.1, 1.1, 0.2):
        my_pruner = Pruner('resnet50', p, model, 0.1, cores, cores*16, write_path, imagenet_path)
        my_pruner.main()
        
        evaluation_results = my_pruner.evaluate_prunning(test_loader)

        results.append(evaluation_results)
    
    original_results = my_pruner.evaluate_original(test_loader)
    results.append(original_results)
    
    results_df = pd.DataFrame(results, columns=['model name', 'prunning type', 'prunning percentage', 'accuracy', 'batch size', 'latency'])

    results_df.to_csv(os.path.join(os.path.expanduser(write_path), 'u_prunning_results.csv'), index=False)
    