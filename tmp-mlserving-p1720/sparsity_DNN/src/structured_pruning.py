from transformers import AutoImageProcessor, ResNetForImageClassification
import torch
# from PIL import Image
import torch 
import os
import numpy as np
import torch.nn.utils.prune as prune
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, ConcatDataset, SubsetRandomSampler
from tqdm import tqdm
import time
from copy import deepcopy
import pandas as pd
import statistics
import heapq
from custom_dataset import CustomDataset
from torch.quantization import quantize_dynamic
import torch.nn.utils.weight_norm as remove_weight_norm
import sys
from onnxruntime.quantization import quantize_dynamic, quantize_static, QuantType, CalibrationDataReader, QuantFormat
import onnxruntime as ort
import torch.nn.functional as F
import subprocess
from onnxruntime.tools import convert_onnx_models_to_ort
from onnxruntime.tools.convert_onnx_models_to_ort import OptimizationStyle
from pathlib import Path
import onnx
import torch
import torch.nn as nn
import torch.fx as fx
import torch.nn.utils.prune as prune
import pprint
from onnxoptimizer import optimize
from extract_imagenet_subclasses import get_subset_labels
from sklearn.preprocessing import LabelEncoder
from imagenet_classes import IMAGENET2012_CLASSES

class Sampler:

    def __init__(self, imagenet_folder, train_sample_percentage, test_sample_percentage, workers, imagenet_subset=None) -> None:
        self.train_sample_percentage = train_sample_percentage
        self.test_sample_percentage = test_sample_percentage
        self.preprocessor = AutoImageProcessor.from_pretrained("microsoft/resnet-50")
        # Paths to the folders containing ImageNet samples
        self.imagenet_folder = imagenet_folder
        self.imagenet_subset = imagenet_subset
        
        self.train_folders = [
            os.path.join(os.path.expanduser(self.imagenet_folder), 'train_images_0'),
            os.path.join(os.path.expanduser(self.imagenet_folder), 'train_images_1'),
            os.path.join(os.path.expanduser(self.imagenet_folder), 'train_images_2'),
            os.path.join(os.path.expanduser(self.imagenet_folder), 'train_images_3'),
            os.path.join(os.path.expanduser(self.imagenet_folder), 'train_images_4')
        ]

        self.val_folder = os.path.join(os.path.expanduser(self.imagenet_folder), 'val_images')
        self.workers = workers

    def train_sample(self, batch_size):

        # Load datasets from each folder and concatenate them
        datasets_list = []
        for folder in self.train_folders:
            datasets_list.append(CustomDataset(img_dir=folder, subset=self.imagenet_subset, transform=self.preprocessor))

        # Combine all datasets
        combined_dataset = ConcatDataset(datasets_list)

        if self.train_sample_percentage < 1:
            # Total number of samples
            dataset_size = len(combined_dataset)

            # Define the x% size
            subset_size = int(self.train_sample_percentage * dataset_size)

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
                num_workers=self.workers,
                pin_memory=True
            )
        else:
            train_loader = DataLoader(
                combined_dataset,
                batch_size=batch_size,
                shuffle=True,  # Shuffles the combined dataset
                num_workers=self.workers,
                pin_memory=True
            )

        return train_loader
    
    def calibration_sample(self, batch_size=1):

        # Load datasets from each folder and concatenate them
        datasets_list = []
        for folder in self.train_folders:
            datasets_list.append(CustomDataset(img_dir=folder, subset=self.imagenet_subset, transform=self.preprocessor))

        # Combine all datasets
        combined_dataset = ConcatDataset(datasets_list)

        # Total number of samples
        dataset_size = len(combined_dataset)

        # Define the x% size
        subset_size = batch_size

        # Randomly shuffle indices
        indices = np.random.permutation(dataset_size)

        # Take the first subset_size indices for sampling
        subset_indices = indices[:subset_size]

        # Create the sampler
        sampler = SubsetRandomSampler(subset_indices)

        calibration_loader = DataLoader(
            combined_dataset,
            batch_size=batch_size,
            sampler=sampler,  # Use sampler instead of shuffle=True
            num_workers=self.workers,
            pin_memory=True
        )
        

        return calibration_loader

    def test_sample(self, batch_size):

        test_set = CustomDataset(img_dir=self.val_folder, subset=self.imagenet_subset, transform=self.preprocessor)

        if self.test_sample_percentage < 1:
            # Total number of samples
            dataset_size = len(test_set)

            # Define the x% size
            subset_size = int(self.test_sample_percentage * dataset_size)

            # Randomly shuffle indices
            indices = np.random.permutation(dataset_size)

            # Take the first subset_size indices for sampling
            subset_indices = indices[:subset_size]

            # Create the sampler
            sampler = SubsetRandomSampler(subset_indices)

            test_loader = DataLoader(
                test_set,
                batch_size=batch_size,
                sampler=sampler,  # Use sampler instead of shuffle=True
                num_workers=self.workers,
                pin_memory=True
            )
        else:
            test_loader = DataLoader(
                test_set,
                batch_size=batch_size,
                shuffle=True,  # Shuffles the combined dataset
                num_workers=self.workers,
                pin_memory=True
            )

        return test_loader

# 4. Prepare a DataReader for calibration (required for static quantization)
class ImageDataReader(CalibrationDataReader):
    def __init__(self, dataloader):
        self.dataloader = dataloader
        self.data_iter = iter(dataloader)
        self.input_name = "input"  # Match the ONNX model input name

    def get_next(self):
        try:
            data = next(self.data_iter)
            inputs = data[0]
            inputs = inputs.squeeze(1)
            return {self.input_name: inputs.numpy()}  # Convert tensor to NumPy
        except StopIteration:
            return None

class ModifiedConv2d(nn.Module):
    def __init__(self, original_conv:nn.Module, out_indices=list, in_indices=list, modify_in=False, modify_out=False, new_in_channels=int, new_out_channels=int):
        super(ModifiedConv2d, self).__init__()

        if modify_in:
            in_channels = new_in_channels
        else:
            in_channels = original_conv.in_channels
        
        if modify_out:
            out_channels = new_out_channels
        else:
            out_channels = original_conv.out_channels
            
        
        # Inherit all parameters except for the input channels
        self.conv = nn.Conv2d(in_channels,
                              out_channels,
                              kernel_size=original_conv.kernel_size,
                              stride=original_conv.stride,
                              padding=original_conv.padding,
                              dilation=original_conv.dilation,
                              groups=original_conv.groups,
                              bias=original_conv.bias is not None)
        
        # if modify_in and modify_out:
        #     self.conv.weight.data = original_conv.weight.data[out_indices][:, in_indices, :, :]
        #     if original_conv.bias is not None:
        #         self.conv.bias.data = original_conv.bias.data[out_indices]
        
        if modify_out == True:
            self.conv.weight.data = original_conv.weight.data[out_indices]
            if original_conv.bias is not None:
                self.conv.bias.data = original_conv.bias.data[out_indices]
        if modify_in == True:
            self.conv.weight.data = original_conv.weight.data[:, in_indices, :, :]
            if original_conv.bias is not None:
                self.conv.bias.data = original_conv.bias.data


    def forward(self, x):
        return self.conv(x)

class ModifiedBatchNorm2d(nn.Module):
    def __init__(self, original_bn, new_input_channels, indices):
        super(ModifiedBatchNorm2d, self).__init__()
        
        # Inherit all parameters except for the input channels
        self.bn = nn.BatchNorm2d(new_input_channels,
                                 eps=original_bn.eps,
                                 momentum=original_bn.momentum,
                                 affine=original_bn.affine,
                                 track_running_stats=original_bn.track_running_stats)
        
        self.bn.weight.data = original_bn.weight.data[indices]
        self.bn.bias.data = original_bn.bias.data[indices]
        self.bn.running_mean.data = original_bn.running_mean.data[indices]
        self.bn.running_var.data = original_bn.running_var.data[indices]

    def forward(self, x):
        return self.bn(x)

class ModifiedLinear(nn.Module):
    def __init__(self, original_linear, indices, out_classes, out_indices):
        super(ModifiedLinear, self).__init__()
        
        new_in_features = len(indices)  # Infer new input size from indices

        # Ensure indices are valid
        assert max(indices) < original_linear.in_features, "Indices exceed original in_features"

        # Create new Linear layer with modified in_features
        self.linear = nn.Linear(new_in_features, out_features=out_classes, bias=original_linear.bias is not None)

        # Copy only the selected input weights
        with torch.no_grad():
            

            # Copy bias if it exists
            if original_linear.bias is not None:
                if out_indices is not None and len(out_indices) > 0:
                    self.linear.weight.data = original_linear.weight.data[out_indices][:, indices]
                    self.linear.bias.data.copy_(original_linear.bias.data[out_indices])
                else:
                    self.linear.weight.data = original_linear.weight.data[:, indices]
                    self.linear.bias.data.copy_(original_linear.bias.data)

    def forward(self, x):
        return self.linear(x)


class StructuredPruning:
    def __init__(self, model, percentage=0.2, train_loader=Sampler.train_sample, subset=None):
        self.model = deepcopy(model)
        self.percentage = percentage
        self.get_total_filter_count()
        self.structure = self.get_encoder_structure()  # Track layer dependencies
        self.filters_to_prune = round(self.filter_count * self.percentage)
        print(f'filters_to_prune: {self.filters_to_prune}')
        print(f'filter count: {self.filter_count}')
        self.train_loader = train_loader
        self.subset=subset
        if self.subset:
            self.subset_labels = get_subset_labels(self.subset)
            self.true_subset_labels  = np.array([list(IMAGENET2012_CLASSES.keys()).index(i) for i in self.subset_labels])
        
        # print(self.model)

        # print(self.filter_count)
    
    

    def pretty_print_dict(self, d, indent=0):
        """Recursively prints a nested dictionary with indentation, handling nn.Modules properly."""
        for key, value in d.items():
            if isinstance(value, dict):  # If value is a nested dictionary, recurse
                print(" " * indent + str(key) + ":")
                self.pretty_print_dict(value, indent + 4)
            else:  # Print other values normally
                print(" " * indent + str(key) + ": " + str(value))


    def get_encoder_structure(self):
        """
        Build a mapping from each module to its dependent modules.
        This assumes layers are sequentially connected.
        """
        dependency_map = {}
        
        stages = [int(name) for name, children in self.model.resnet.encoder.stages.named_children()]

        dependency_map['stages'] = {}

        for stage in stages:

            obj = getattr(self.model.resnet.encoder.stages, str(stage))
            for layer_name, children in obj.named_children():
                layers = [int(name) for name, children in children.named_children()]
                
                dependency_map['stages'][stage] = {}
                dependency_map['stages'][stage]['layers'] = len(layers)

        return dependency_map
    
    
    def get_total_filter_count(self):

        prunable_params = []
        # Step 1: Collect all Conv2d layers and their filter norms
        self.shares_dict = {}
        self.shares_dict['step'] = {}
        self.shares_dict['step']['embedder'] = 0
        self.shares_dict['step']['encoder'] = {}
        self.shares_dict['step']['encoder'][0] = 0
        self.shares_dict['step']['encoder'][1] = 0
        self.shares_dict['step']['encoder'][2] = 0
        self.shares_dict['step']['encoder'][3] = 0
        
        for name, module in self.model.named_modules():
            if isinstance(module, torch.nn.Conv2d):
                if 'shortcut' not in name:
                    splited_name = name.split('.')
                    if 'embedder' not in name:
                        block = splited_name[7]
                        stage = splited_name[3]
                        weight = module.weight.detach()  # Get weights
                        norms = torch.norm(weight, p=2, dim=(1, 2, 3))  # L2 norm for filters
                        prunable_params.append((name, module, norms.shape[0]))
                        self.shares_dict['step']['encoder'][int(stage)] += norms.shape[0]
                    else:
                        weight = module.weight.detach()  # Get weights
                        norms = torch.norm(weight, p=2, dim=(1, 2, 3))  # L2 norm for filters
                        prunable_params.append((name, module, norms.shape[0]))
                        self.shares_dict['step']['embedder'] += norms.shape[0]
                        
        self.filter_count = sum([num_filters for stage, module, num_filters in prunable_params])
        self.pretty_print_dict(self.shares_dict)
    
    def analyze_layers(self, module):
        weight = module.weight.detach()
        norms = torch.norm(weight, p=2, dim=(1, 2, 3))  # Compute filter norms
        num_filters = norms.shape[0]

        return norms, num_filters
    
    def set_nested_attr(self, obj, attr_path, value):
        """Recursively set a nested attribute given a dot-separated string."""
        attrs = attr_path.split(".")
        sub_obj = obj
        for attr in attrs[:-1]:  # Traverse to the parent of the last attribute
            sub_obj = getattr(sub_obj, attr)
        
        setattr(sub_obj, attrs[-1], value)  # Set the final attribute


    def prune_modules(self):
        """ Analyzes filters from a given Conv2D layer. """
        pruned_dependencies = {}  # Store the number of filters pruned per layer
        # print(self.model)
        for name, module in self.model.named_modules():
            if isinstance(module, nn.Conv2d):
                # print(name, module)
                splited_name = name.split('.')
                step = splited_name[1]
                stage = splited_name[3]
                norms, num_filters = self.analyze_layers(module)

                distribution_dict = {}
                distribution_dict['step'] = {}
                distribution_dict['step']['embedder'] = 0
                distribution_dict['step']['encoder'] = {}
                distribution_dict['step']['encoder'][0] = 0
                distribution_dict['step']['encoder'][1] = 0
                distribution_dict['step']['encoder'][2] = 0.4
                distribution_dict['step']['encoder'][3] = 0.6
                
                # if 'shortcut' not in name:
                #     if step == 'embedder':
                #         prune_amount = round(distribution_dict['step']['embedder'] * self.filters_to_prune)
                #     elif step == 'encoder':
                #         prune_amount = round((norms.shape[0]/self.shares_dict['step']['encoder'][int(stage)]) * self.filters_to_prune * distribution_dict['step']['encoder'][int(stage)])
                #         # print(name, prune_amount)
                # else:
                #     prune_amount = 0
                
                
                if step == 'embedder':
                    # prune_amount = round(self.shares_dict['step']['embedder']/self.filter_count * self.filters_to_prune)
                    prune_amount = 0
                elif step == 'encoder':
                    # if int(stage) > 1:
                    #     prune_amount = round((norms.shape[0]/self.shares_dict['step']['encoder'][int(stage)]) * self.filters_to_prune * self.shares_dict['step']['encoder'][int(stage)]/self.filter_count)
                    # else:
                    #     prune_amount = 0
                    prune_amount = round((norms.shape[0]/self.shares_dict['step']['encoder'][int(stage)]) * self.filters_to_prune * self.shares_dict['step']['encoder'][int(stage)]/self.filter_count)
                
                
                if step == 'embedder': 
                    
                    # print(name)
                    # Identify filters to keep
                    if prune_amount > 0:
                        indices = torch.argsort(norms)[prune_amount:]  # Keep highest norm filters
                        new_nn = ModifiedConv2d(module, out_indices=indices, modify_out=True, new_out_channels=len(indices))
                        pruned_dependencies[name] = {}
                        pruned_dependencies[name]['new_module'] = new_nn.conv
                        pruned_dependencies[name]['dependent_names'] = []
                        pruned_dependencies[name]['new_dependent_modules'] = []
                        pruned_dependencies[name]['indices'] = indices
                        # pruned_dependencies[name]['dependent_names'].append(name)
                        # pruned_dependencies[name]['new_dependent_modules'].append(new_nn.conv)

                        embedder_first_batch_norm = self.model.resnet.embedder.embedder.normalization
                        embedder_first_batch_norm_name = 'resnet.embedder.embedder.normalization'
                        new_bn = ModifiedBatchNorm2d(embedder_first_batch_norm, new_input_channels=len(indices), indices=indices)
                        pruned_dependencies[name]['dependent_names'].append(embedder_first_batch_norm_name)
                        pruned_dependencies[name]['new_dependent_modules'].append(new_bn.bn)
  
                    else:
                        pruned_dependencies[name] = {}
                        pruned_dependencies[name]['indices'] = []
                elif step == 'encoder':
                    layer = splited_name[5]
                    block = splited_name[7]
                    # if 'shortcut' not in name and int(block) == 2:
                    #     prune_amount = 0 
                    if prune_amount > 0:
                        indices = torch.argsort(norms)[prune_amount:]  # Keep highest norm filters
                        
                        ###### First change the conv2 and batch norm
                        new_nn = ModifiedConv2d(module, out_indices=indices, modify_out=True, new_out_channels=len(indices))
                        pruned_dependencies[name] = {}
                        pruned_dependencies[name]['new_module'] = new_nn.conv
                        pruned_dependencies[name]['dependent_names'] = []
                        pruned_dependencies[name]['new_dependent_modules'] = []
                        pruned_dependencies[name]['indices'] = indices
                        if 'shortcut' not in name:
                            # change batch normalization in the same block
                            normalization = getattr(self.model.resnet.encoder.stages[int(stage)].layers[int(layer)].layer[int(block)], 'normalization')
                            norm_name = f'resnet.encoder.stages.{stage}.layers.{layer}.layer.{block}.normalization'
                        else:
                            normalization = getattr(self.model.resnet.encoder.stages[int(stage)].layers[int(layer)].shortcut, 'normalization')
                            norm_name = f'resnet.encoder.stages.{stage}.layers.{layer}.shortcut.normalization'
                        new_bn = ModifiedBatchNorm2d(normalization, new_input_channels=len(indices), indices=indices)
                        pruned_dependencies[name]['dependent_names'].append(norm_name)
                        pruned_dependencies[name]['new_dependent_modules'].append(new_bn.bn)
                    else:
                        pruned_dependencies[name] = {}
                        pruned_dependencies[name]['indices'] = []
        
        for name, dict in pruned_dependencies.items():
            
            if len(dict['indices']) > 0:
                self.set_nested_attr(self.model, name, dict['new_module'])
                for id, dependency_name in enumerate(dict['dependent_names']):
                    self.set_nested_attr(self.model, dependency_name, dict['new_dependent_modules'][id])
        
        ####### Now modify the input channels:
        for stage in list(self.structure['stages']):

            if stage == 0:
                # Stage 0 inherits the dimensions from the embedder. Change the input, output channels of shortcut convolution and batch normalization
                ###### first the shortcut conv
                shortcut_conv2d = self.model.resnet.encoder.stages[stage].layers[0].shortcut.convolution
                # out_indices = pruned_dependencies['resnet.encoder.stages.0.layers.0.layer.2.convolution']['indices']
                # out_channels = len(out_indices)
                in_indices = pruned_dependencies['resnet.embedder.embedder.convolution']['indices']
                in_channels = len(in_indices)
                if in_channels > 0:
                    new_nn = ModifiedConv2d(shortcut_conv2d, modify_in=True, new_in_channels=in_channels, in_indices=in_indices)
                    sub_obj = getattr(self.model.resnet.encoder.stages[0].layers[0], 'shortcut')
                    setattr(sub_obj, 'convolution', new_nn.conv)
                    
                    
                ###### Now first conv
                for layer in range(self.structure['stages'][stage]['layers']):
                    if layer == 0:
                        for block in [0, 1, 2]:
                            if block == 0:
                                first_conv2d = self.model.resnet.encoder.stages[stage].layers[layer].layer[block].convolution
                                in_indices = pruned_dependencies['resnet.embedder.embedder.convolution']['indices']
                                new_in_channels = len(in_indices)
                                if new_in_channels > 0:
                                    new_nn = ModifiedConv2d(first_conv2d, modify_in=True, new_in_channels=new_in_channels, in_indices=in_indices)
                                    sub_obj = getattr(self.model.resnet.encoder.stages[stage].layers[layer].layer, str(block))
                                    setattr(sub_obj, 'convolution', new_nn.conv)
                            else:
                                conv2d = self.model.resnet.encoder.stages[stage].layers[layer].layer[block].convolution
                                in_indices = pruned_dependencies[f'resnet.encoder.stages.{stage}.layers.{layer}.layer.{block-1}.convolution']['indices']
                                new_in_channels = len(in_indices)
                                if new_in_channels > 0:
                                    new_nn = ModifiedConv2d(conv2d, modify_in=True, new_in_channels=new_in_channels, in_indices=in_indices)
                                    sub_obj = getattr(self.model.resnet.encoder.stages[stage].layers[layer].layer, str(block))
                                    setattr(sub_obj, 'convolution', new_nn.conv)
                    else:
                        for block in [0, 1, 2]:
                            if block == 0:
                                ###### Now first conv
                                conv2d = self.model.resnet.encoder.stages[stage].layers[layer].layer[block].convolution
                                in_indices = pruned_dependencies[f'resnet.encoder.stages.{stage}.layers.{layer-1}.layer.2.convolution']['indices']
                                new_in_channels = len(in_indices)
                                if new_in_channels > 0:
                                    new_nn = ModifiedConv2d(conv2d, modify_in=True, new_in_channels=new_in_channels, in_indices=in_indices)
                                    sub_obj = getattr(self.model.resnet.encoder.stages[stage].layers[layer].layer, str(block))
                                    setattr(sub_obj, 'convolution', new_nn.conv)
                            else:
                                conv2d = self.model.resnet.encoder.stages[stage].layers[layer].layer[block].convolution
                                in_indices = pruned_dependencies[f'resnet.encoder.stages.{stage}.layers.{layer}.layer.{block-1}.convolution']['indices']
                                new_in_channels = len(in_indices)
                                if new_in_channels > 0:
                                    new_nn = ModifiedConv2d(conv2d, modify_in=True, new_in_channels=new_in_channels, in_indices=in_indices)
                                    sub_obj = getattr(self.model.resnet.encoder.stages[stage].layers[layer].layer, str(block))
                                    setattr(sub_obj, 'convolution', new_nn.conv)
            else:
                for layer in range(self.structure['stages'][stage]['layers']):
                    if layer == 0:
                        old_conv2d = self.model.resnet.encoder.stages[stage].layers[layer].shortcut.convolution
                        # out_indices = pruned_dependencies[f'resnet.encoder.stages.{stage}.layers.{layer}.layer.2.convolution']['indices']
                        # new_out_channels = len(out_indices)
                        previous_layers = self.structure['stages'][int(stage) - 1]['layers'] - 1
                        in_indices = pruned_dependencies[f'resnet.encoder.stages.{stage-1}.layers.{previous_layers}.layer.2.convolution']['indices']
                        new_in_channels = len(in_indices)
                        if new_in_channels > 0:
                            new_nn = ModifiedConv2d(old_conv2d, modify_in=True, new_in_channels=new_in_channels, in_indices=in_indices)
                            sub_obj = getattr(self.model.resnet.encoder.stages[stage].layers[0], 'shortcut')
                            setattr(sub_obj, 'convolution', new_nn.conv)
                            

                        for block in [0, 1, 2]:
                            if block == 0:
                                ###### Now first conv
                                first_conv2d = self.model.resnet.encoder.stages[stage].layers[layer].layer[block].convolution
                                previous_layers = self.structure['stages'][int(stage) - 1]['layers'] - 1
                                in_indices = pruned_dependencies[f'resnet.encoder.stages.{stage-1}.layers.{previous_layers}.layer.2.convolution']['indices']
                                new_in_channels = len(in_indices)
                                if new_in_channels > 0:
                                    new_nn = ModifiedConv2d(first_conv2d, modify_in=True, new_in_channels=new_in_channels, in_indices=in_indices)
                                    sub_obj = getattr(self.model.resnet.encoder.stages[stage].layers[layer].layer, '0')
                                    setattr(sub_obj, 'convolution', new_nn.conv)
                            else:
                                conv2d = self.model.resnet.encoder.stages[stage].layers[layer].layer[block].convolution
                                in_indices = pruned_dependencies[f'resnet.encoder.stages.{stage}.layers.{layer}.layer.{block-1}.convolution']['indices']
                                new_in_channels = len(in_indices)
                                if new_in_channels > 0:
                                    new_nn = ModifiedConv2d(conv2d, modify_in=True, new_in_channels=new_in_channels, in_indices=in_indices)
                                    sub_obj = getattr(self.model.resnet.encoder.stages[stage].layers[layer].layer, str(block))
                                    setattr(sub_obj, 'convolution', new_nn.conv)   
                    else:
                        for block in [0, 1, 2]:

                            if block == 0:
                                ###### Now first conv
                                conv2d = self.model.resnet.encoder.stages[stage].layers[layer].layer[block].convolution
                                in_indices = pruned_dependencies[f'resnet.encoder.stages.{stage}.layers.{layer-1}.layer.2.convolution']['indices']
                                new_in_channels = len(in_indices)
                                if new_in_channels > 0:
                                    new_nn = ModifiedConv2d(conv2d, modify_in=True, new_in_channels=new_in_channels, in_indices=in_indices)
                                    sub_obj = getattr(self.model.resnet.encoder.stages[stage].layers[layer].layer, str(block))
                                    setattr(sub_obj, 'convolution', new_nn.conv)
                            else:
                                conv2d = self.model.resnet.encoder.stages[stage].layers[layer].layer[block].convolution
                                in_indices = pruned_dependencies[f'resnet.encoder.stages.{stage}.layers.{layer}.layer.{block-1}.convolution']['indices']
                                new_in_channels = len(in_indices)
                                if new_in_channels > 0:
                                    new_nn = ModifiedConv2d(conv2d, modify_in=True, new_in_channels=new_in_channels, in_indices=in_indices)
                                    sub_obj = getattr(self.model.resnet.encoder.stages[stage].layers[layer].layer, str(block))
                                    setattr(sub_obj, 'convolution', new_nn.conv)
        
        classifier = getattr(self.model.classifier, '1')
        last_stage_layers = self.structure['stages'][3]['layers']
        classifier_indices = pruned_dependencies[f'resnet.encoder.stages.3.layers.{last_stage_layers-1}.layer.2.convolution']['indices']
        if len(classifier_indices) > 0:
            out_classes = 1000 if self.subset == None else len(self.subset_labels)
            out_labels = self.true_subset_labels if self.subset != None else None
            new_classifier = ModifiedLinear(classifier, classifier_indices, out_classes, out_labels)
            sub_obj = getattr(self.model, 'classifier')
            setattr(sub_obj, '1', new_classifier.linear)
    
    def update_bn_statistics(self):
        """Updates BatchNorm running statistics by forwarding data through the model."""
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Move the model to the device
        self.model = self.model.to(device)
        
        self.model.train()  # BN layers will update their running stats
        with torch.no_grad():  # No gradients needed
            for inputs, _ in tqdm(self.train_loader):  # Iterate over some batches
                inputs = inputs.squeeze(1)
                inputs, _ = inputs.to(device, non_blocking=True), _.to(device, non_blocking=True)
                _ = self.model(inputs)  # Forward pass updates BN stats



    def prune_model(self):
        """ Performs structured pruning while updating dependent layers. """
        self.prune_modules()
        # print(self.model)
        # self.update_bn_statistics()
       

        return self.model


class Pruner:
    
    def __init__(self, type, model_name, percentage, model, training_sample, test_sample, cores, batch_size, write_path, imagenet_path, target_platform, quantize=False, optimization_level='disable', imagenet_subset=None) -> None:
        self.percentage = percentage
        self.prunned_model = deepcopy(model)
        self.original_model = deepcopy(model)
        self.training_sample = training_sample
        self.test_sample = test_sample
        self.cores = cores
        self.batch_size = batch_size
        self.write_path = write_path
        self.imagenet_path = imagenet_path
        self.model_name = model_name
        self.subset = imagenet_subset
        self.sampler = Sampler(self.imagenet_path, self.training_sample, self.test_sample, self.cores, self.subset)
        self.test_loader = self.sampler.test_sample(self.batch_size)
        self.train_loader = self.sampler.train_sample(self.batch_size)
        self.type = type
        self.quantize = quantize
        self.target_platform = target_platform
        self.optimization_level = optimization_level
        if self.subset:
            self.subset_labels = get_subset_labels(self.subset)
            self.label_encoder = LabelEncoder()
            self.true_subset_labels  = np.array([list(IMAGENET2012_CLASSES.keys()).index(i) for i in self.subset_labels])
            self.label_encoder.fit(self.true_subset_labels)

    
    # Function to globally prune filters (out_channels) based on L2 norm
    def global_masked_pruning(self):
        prunable_params = []
        filter_norms = []

        # Step 1: Collect all Conv2d layers and their filter norms
        for name, module in self.prunned_model.named_modules():
            if isinstance(module, torch.nn.Conv2d):
                weight = module.weight.detach()  # Get weights
                norms = torch.norm(weight, p=2, dim=(1, 2, 3))  # L2 norm for filters
                prunable_params.append((name, module, "weight", norms))
                filter_norms.extend(norms.tolist())  # Add norms to global list

        # Step 2: Determine the global pruning threshold
        num_filters_to_prune = int(self.percentage * len(filter_norms))
        threshold = heapq.nsmallest(num_filters_to_prune, filter_norms)[-1]  # Smallest norms

        # Step 3: Prune filters with norms below the threshold
        for stage, module, name, norms in prunable_params:
            if "stages.2" in stage or "stages.3" in stage:
                important_filters = (norms >= threshold).nonzero(as_tuple=True)[0]  # Indices of important filters
                nonimportant_filters = (norms < threshold).nonzero(as_tuple=True)[0]
                mask = torch.zeros_like(module.weight)  # Create mask with the same shape as weights
                mask[important_filters, :, :, :] = 1.0  # Set important filters to 1
                prune.custom_from_mask(module, name, mask)  # Apply custom mask
                prune.remove(module, "weight") ##Remove prunning parametrization
                # if nonimportant_filters.shape[0] > 0 :
                #     self.retrain_pruned_model(0.01, 0.01)

    def global_structured_pruning(self):
        prunable_params = []

        # Step 1: Collect all Conv2d layers and their filter norms
        filter_count = 0
        for name, module in self.prunned_model.named_modules():
            if isinstance(module, torch.nn.Conv2d):
                weight = module.weight.detach()  # Get weights
                norms = torch.norm(weight, p=2, dim=(1, 2, 3))  # L2 norm for filters
                prunable_params.append((name, module, norms.shape[0]))

        filter_count = sum([num_filters for stage, module, num_filters in prunable_params])

        for stage, module, num_filters in prunable_params:
            
            prune.ln_structured(
                module=module,  # Target module
                name="weight",                 # Target parameter (weights)
                amount = (num_filters / filter_count) * self.percentage,                    # Proportion of filters to prune
                n=1,                           # L1 norm criterion
                dim=0                          # Prune entire filters (dimension 0 for filters)
            )
            prune.remove(module, "weight") ##Remove prunning parametrization
        
        # If weight normalization is applied, remove it
        # for name, module in self.prunned_model.named_modules():
        #     if isinstance(module, (torch.nn.Conv2d, torch.nn.Linear)):
        #         module = remove_weight_norm(module)
    
    def global_structured_removal(self):

        remover = StructuredPruning(self.prunned_model, self.percentage, self.train_loader, self.subset)
        self.prunned_model = remover.prune_model()
        # print(self.prunned_model)
        

    
    def global_unstructured_pruning(self):
        # Collect all prunable parameters (weights in Conv2d and Linear layers)
        prunable_params = []
        for name, module in self.prunned_model.named_modules():
            if isinstance(module, (torch.nn.Conv2d, torch.nn.Linear)):
                # if "stages.2" in name or "stages.3" in name:
                prunable_params.append((module, "weight"))
        
        
        # Apply global unstructured pruning
        prune.global_unstructured(
            parameters=prunable_params,
            pruning_method=prune.L1Unstructured,
            amount=self.percentage,  # Fraction of total weights to prune globally
        )
        prune.remove(module, "weight") ##Remove prunning parametrization

        # If weight normalization is applied, remove it
        # for name, module in self.prunned_model.named_modules():
        #     if isinstance(module, (torch.nn.Conv2d, torch.nn.Linear)):
        #         module = remove_weight_norm(module)
    

    def optimize_onnx_model(self, input_path: str, output_path: str):
        """
        Optimizes an ONNX model using onnxruntime's preprocessing utility.
        
        Args:
            input_path (str): Path to the input ONNX model.
            output_path (str): Path to save the optimized ONNX model.
        
        Raises:
            subprocess.CalledProcessError: If the subprocess command fails.
        """
        try:
            subprocess.run(
                [
                    "python", 
                    "-m", 
                    "onnxruntime.quantization.preprocess", 
                    "--input", input_path, 
                    "--output", output_path
                ],
                check=True
            )
            print(f"Optimized model saved to: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during ONNX model optimization: {e}")
            raise
    
    def export_models(self):

        # Generate file names for pruned and quantized models
        file_name_original = (
            f'resnet50_{self.type}_original_{self.subset}_{self.percentage}.onnx'
            if self.subset else f'resnet50_{self.type}_original_{self.percentage}.onnx'
        )
        file_name_prunned = (
            f'resnet50_{self.type}_prunned_{self.subset}_{self.percentage}.onnx'
            if self.subset else f'resnet50_{self.type}_prunned_{self.percentage}.onnx'
        )
        
        write_path_original = os.path.join(self.write_path, file_name_original)
        self.write_path_prunned = os.path.join(self.write_path, file_name_prunned)

        # Select device (GPU if available, otherwise CPU)
        device = torch.device( "cpu")

        # Move the model to the device
        self.prunned_model = self.prunned_model.to(device)

        # Create dummy input on the same device as the model
        dummy_input = torch.randn(self.batch_size, 3, 224, 224, device=device)

        # Export pruned model to ONNX
        torch.onnx.export(
            self.prunned_model,
            dummy_input,
            self.write_path_prunned,
            opset_version=13,  # Use a compatible ONNX opset version
            input_names=["input"],  # The input tensor's name (you can change this depending on your model)
            output_names=["output"],
            do_constant_folding=True
            # dynamic_axes={
            # "input": {0: "batch_size"},  # Dynamic batch size for the input
            # "output": {0: "batch_size"}  # Dynamic batch size for the output
            # }
        )

        # Move the model to the device
        self.original_model = self.original_model.to(device)

        # Export original model to ONNX
        torch.onnx.export(
            self.original_model,
            dummy_input,
            write_path_original,
            opset_version=13,  # Use a compatible ONNX opset version
            input_names=["input"],  # The input tensor's name (you can change this depending on your model)
            output_names=["output"],
            do_constant_folding=True
            # dynamic_axes={
            # "input": {0: "batch_size"},  # Dynamic batch size for the input
            # "output": {0: "batch_size"}  # Dynamic batch size for the output
            # }
        )

    # Quantize the weights and activations of linear and convolutional layers to INT8 for CPU optimization
    def quantize_model(self):

        self.export_models()

        file_name_prunned_optimized = (
            f'resnet50_{self.type}_prunned_optimized_{self.subset}_{self.percentage}.onnx'
            if self.subset else f'resnet50_{self.type}_prunned_optimized_{self.percentage}.onnx'
        )
        file_name_quantized = (
            f'resnet50_{self.type}_quantized_{self.subset}_{self.percentage}.onnx'
            if self.subset else f'resnet50_{self.type}_quantized_{self.percentage}.onnx'
        )
        file_name_quantized_optimized = (
            f'resnet50_{self.type}_quantized_optimized_{self.subset}_{self.percentage}'
            if self.subset else f'resnet50_{self.type}_quantized_optimized_{self.percentage}'
        )

        write_path_prunned_optimized = os.path.join(self.write_path, file_name_prunned_optimized)
        write_path_quantized = os.path.join(self.write_path, file_name_quantized) #### skip quantization if running on cpus
        write_path_quantized_optimized = os.path.join(self.write_path, file_name_quantized_optimized)
        

        if self.quantize:

            model_path = self.write_path_prunned
            model = onnx.load(model_path)
            if onnx.checker.check_model(model, full_check=True) == None:

                self.optimize_onnx_model(self.write_path_prunned, write_path_prunned_optimized)

                calibration_loader = self.sampler.calibration_sample(self.batch_size)

                quantize_static(
                    write_path_prunned_optimized,
                    write_path_quantized,
                    calibration_data_reader=ImageDataReader(calibration_loader),
                    quant_format=QuantFormat.QDQ,
                    activation_type=QuantType.QInt8,  # Use int8 quantization
                    weight_type=QuantType.QInt8,
                    per_channel=True,  # Enable per-channel quantization
                )

                os.environ["ORT_CONVERT_ONNX_MODELS_TO_ORT_OPTIMIZATION_LEVEL"] = self.optimization_level
                convert_onnx_models_to_ort.convert_onnx_models_to_ort(
                Path(write_path_quantized),
                output_dir=Path(write_path_quantized_optimized),
                optimization_styles=[OptimizationStyle.Fixed],
                target_platform=self.target_platform, ##### Depends on the target architecture
                save_optimized_onnx_model=True,
                enable_type_reduction=True
                )
            else:
                self.export_models()
                self.optimize_onnx_model(self.write_path_prunned, write_path_prunned_optimized)

                calibration_loader = self.sampler.calibration_sample(self.batch_size)

                quantize_static(
                    write_path_prunned_optimized,
                    write_path_quantized,
                    calibration_data_reader=ImageDataReader(calibration_loader),
                    quant_format=QuantFormat.QDQ,
                    activation_type=QuantType.QInt8,  # Use int8 quantization
                    weight_type=QuantType.QInt8,
                    per_channel=True,  # Enable per-channel quantization
                )

                os.environ["ORT_CONVERT_ONNX_MODELS_TO_ORT_OPTIMIZATION_LEVEL"] = self.optimization_level
                convert_onnx_models_to_ort.convert_onnx_models_to_ort(
                Path(write_path_quantized),
                output_dir=Path(write_path_quantized_optimized),
                optimization_styles=[OptimizationStyle.Fixed],
                target_platform=self.target_platform, ##### Depends on the target architecture
                save_optimized_onnx_model=True,
                enable_type_reduction=True
                )
        else:
            dir_name_prunned = (
            f'resnet50_{self.type}_prunned_{self.subset}_{self.percentage}'
            if self.subset else f'resnet50_{self.type}_prunned_{self.percentage}'
            )
            write_path_dir_name_prunned = os.path.join(self.write_path, dir_name_prunned)
            model_path = self.write_path_prunned
            model = onnx.load(model_path)
            passes = ["eliminate_identity", "eliminate_nop_dropout", "eliminate_nop_transpose"]
            optimized_model = optimize(model, passes)
            onnx.save(optimized_model, Path(self.write_path_prunned))
            if onnx.checker.check_model(model, full_check=True) == None:
                os.environ["ORT_CONVERT_ONNX_MODELS_TO_ORT_OPTIMIZATION_LEVEL"] = self.optimization_level
                convert_onnx_models_to_ort.convert_onnx_models_to_ort(
                Path(self.write_path_prunned),
                output_dir=Path(write_path_dir_name_prunned),
                optimization_styles=[OptimizationStyle.Fixed],
                target_platform=self.target_platform, ##### Depends on the target architecture
                save_optimized_onnx_model=True,
                # enable_type_reduction=True
                )

        
    def retrain_pruned_model(self):

        # Freeze all parameters except for the classifier
        for param in self.prunned_model.parameters():
            param.requires_grad = True
        # for param in self.prunned_model.classifier.parameters():
        #     param.requires_grad = True
        # for param in self.prunned_model.resnet.encoder.stages[2].parameters():
        #     param.requires_grad = True
        # for param in self.prunned_model.resnet.encoder.stages[3].parameters():
        #     param.requires_grad = True
        
        # Collect all trainable parameters
        trainable_params = filter(lambda p: p.requires_grad, self.prunned_model.parameters())

        # Initialize the optimizer with all trainable parameters
        optimizer = torch.optim.Adam(trainable_params, lr=0.001)
        # Gamma is the decay factor; here it's set to 0.9, which means the learning rate will decay by 10% every epoch.
        # scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.95)
        
        # Define loss function and optimizer
        criterion = nn.CrossEntropyLoss()
        # optimizer = torch.optim.Adam(self.prunned_model.classifier.parameters(), lr=0.001)

        # Training loop
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.prunned_model = self.prunned_model.to(device)

        self.prunned_model.train()
        epochs = 100
        improvement_threshold = 0.999  # A loss that is x% better than the best loss
        best_loss = np.inf  # Initialize with a large value
        print('retraining:')
        for epoch in range(epochs):
            total_loss = 0
            for inputs, labels in tqdm(self.train_loader):
                inputs = inputs.squeeze(1)
                if self.subset:
                    numpy_labels = labels.numpy()
                    encoded_numpy_labels = self.label_encoder.transform(numpy_labels)
                    encoded_tensor = torch.from_numpy(encoded_numpy_labels)
                    inputs, labels = inputs.to(device, non_blocking=True), encoded_tensor.to(device, non_blocking=True)
                else:
                    inputs, labels = inputs.to(device, non_blocking=True), labels.to(device, non_blocking=True)

                # Forward pass
                optimizer.zero_grad()
                outputs = self.prunned_model(inputs).logits  # Access logits from Hugging Face output
                loss = criterion(outputs, labels)
                # Backward pass
                loss.backward()
                # Update model parameters
                optimizer.step()  # Apply gradients
                # scheduler.step()

                total_loss += loss.item()
            
            # Check if the validation loss is at least 10% better than the best loss
            if total_loss < best_loss * improvement_threshold:
                best_loss = total_loss  # Update the best loss
            else:
                print(f"Validation loss did not improve by 5%. Stopping training.")
                break

            print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss/len(self.train_loader):.4f}")
        
        # model.save_pretrained(os.path.expanduser(save_folder))
    
    def main(self):

       
        if self.type == 'structured':
            self.global_structured_removal()
            # self.retrain_pruned_model()
            # self.global_structured_pruning()
            self.quantize_model()
            # self.global_structured_pruning()
            # self.retrain_pruned_model(0.1, 0.1)
        else:
            self.global_unstructured_pruning()
            self.quantize_model()
            # self.retrain_pruned_model(0.1, 0.1)
        # Step 7: Save the pruned and fine-tuned model
        # file_name = 'resnet50_' + self.type + '_prunned_' + str(self.percentage) + '.pth'
        # write_path = os.path.join(self.write_path, file_name)
        # torch.save(self.prunned_model.state_dict(), write_path)

    
    def evaluate_prunning(self):

        # Clear PyTorch cache to free memory
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

        
        available_providers = ort.get_available_providers()
        if 'CUDAExecutionProvider' in  available_providers:
            providers = providers = [
                                        ('CUDAExecutionProvider', {
                                            'arena_extend_strategy': 'kNextPowerOfTwo',
                                            'gpu_mem_limit': 32 * 1024 * 1024 * 1024,  # 32 GB limit,
                                            "enable_cuda_graph": '1',
                                            "cudnn_conv1d_pad_to_nc1d": '1',
                                            "cudnn_conv_use_max_workspace": '1',
                                            'cudnn_conv_algo_search': 'EXHAUSTIVE'
                                        }),
                                        'CPUExecutionProvider'
                                    ]
        elif "CoreMLExecutionProvider" in available_providers:
            providers = ["CoreMLExecutionProvider"]
        else:
            providers = ['CPUExecutionProvider']
        
        prunned_correct = 0
        total = 0
        latency = []

        if self.quantize:

            dir_name_quantized = 'resnet50_' + self.type + '_quantized_optimized_' + self.subset + '_' + str(self.percentage) if self.subset else 'resnet50_' + self.type + '_quantized_optimized_' + str(self.percentage)
            if optimization_level != 'all':
                
                file_name_quantized = (
                    f'resnet50_{self.type}_quantized_{self.subset}_{self.percentage}.{self.optimization_level}.ort'
                    if self.subset else f'resnet50_{self.type}_quantized_{self.percentage}.{self.optimization_level}.ort'
                )
            else:
                file_name_quantized = (
                    f'resnet50_{self.type}_quantized_{self.subset}_{self.percentage}.ort'
                    if self.subset else f'resnet50_{self.type}_quantized_{self.percentage}.ort'
                )
            # file_name_quantized = (f'resnet50_{self.type}_quantized_{self.subset}_{self.percentage}.ort' if self.subset else f'resnet50_{self.type}_quantized_{self.percentage}.ort')
            write_path_quantized = os.path.join(self.write_path, dir_name_quantized, file_name_quantized)
        else:
            dir_name_prunned = (
            f'resnet50_{self.type}_prunned_{self.subset}_{self.percentage}'
            if self.subset else f'resnet50_{self.type}_prunned_{self.percentage}'
            )
            if optimization_level != 'all':
                
                file_name_prunned = (
                    f'resnet50_{self.type}_prunned_{self.subset}_{self.percentage}.{self.optimization_level}.ort'
                    if self.subset else f'resnet50_{self.type}_prunned_{self.percentage}.{self.optimization_level}.ort'
                )
            else:
                file_name_prunned = (
                    f'resnet50_{self.type}_prunned_{self.subset}_{self.percentage}.ort'
                    if self.subset else f'resnet50_{self.type}_prunned_{self.percentage}.ort'
                )
                # file_name_prunned = (
                #     f'resnet50_{self.type}_prunned_{self.subset}_{self.percentage}.onnx'
                #     if self.subset else f'resnet50_{self.type}_prunned_{self.percentage}.onnx'
                # )
            write_path_prunned = os.path.join(self.write_path, dir_name_prunned, file_name_prunned)
        if self.quantize:
            sess_options = ort.SessionOptions()
            sess_options.enable_mem_pattern = True
            session = ort.InferenceSession(write_path_quantized, sess_options=sess_options, providers=providers)
        else:
            file_name_prunned = 'resnet50_' + self.type + '_prunned_' + self.subset + '_' + str(self.percentage) + '.onnx' if self.subset else 'resnet50_' + self.type + '_prunned_' + str(self.percentage) + '.onnx'
            write_path_prunned = os.path.join(self.write_path, file_name_prunned)
            sess_options = ort.SessionOptions()
            sess_options.enable_mem_pattern = True
            sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            session = ort.InferenceSession(write_path_prunned, sess_options=sess_options, providers=providers)
        
        print('using model' + str(session._model_path))
        # Prepare for inference
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name
        input_shape = (self.batch_size, 3, 224, 224)
        num_classes = 1000 if self.subset == None else len(self.subset_labels)
        output_shape = (self.batch_size, num_classes)  # For ResNet50 ImageNet classification

        # Allocate GPU memory for inputs and outputs
        input_tensor_gpu = torch.empty(input_shape, device='cuda', dtype=torch.float32)
        output_tensor_gpu = torch.empty(output_shape, device='cuda', dtype=torch.float32)

        # Create I/O binding and bind pre-allocated GPU tensors
        io_binding = session.io_binding()
        io_binding.bind_input(
            name=input_name,
            device_type='cuda',
            device_id=0,
            element_type=np.float32,
            shape=input_shape,
            buffer_ptr=input_tensor_gpu.data_ptr(),
        )
        io_binding.bind_output(
            name=output_name,
            device_type='cuda',
            device_id=0,
            element_type=np.float32,
            shape=output_shape,
            buffer_ptr=output_tensor_gpu.data_ptr(),
        )

        # Warm-up run for stable performance & CUDA Graph capture
        session.run_with_iobinding(io_binding)

        # with torch.no_grad():
        for inputs, labels in tqdm(self.test_loader):
            if inputs.shape[0] == self.batch_size:
                inputs = inputs.squeeze(1)
                # inputs = inputs.numpy()  # Convert the tensor to a NumPy array
                # Transfer batch to GPU (using pinned memory & non-blocking transfer)
                input_tensor_gpu.copy_(inputs, non_blocking=True)
                start_time = time.time()
                session.run_with_iobinding(io_binding)
                torch.cuda.synchronize()  # Ensure accurate timing
                # prunned_outputs = self.quantized_model(inputs)
                end_time = time.time() - start_time
                latency.append(end_time)
                # Efficient approach
                probabilities = F.softmax(output_tensor_gpu, dim=1)  # Softmax on GPU
                predicted_labels = probabilities.argmax(dim=1).cpu().numpy()  # Argmax on GPU, then move to CPU if needed
                if self.subset:
                    true_predicted_labels = self.label_encoder.inverse_transform(predicted_labels)
                else:
                    true_predicted_labels = predicted_labels
                
                # prunned_, prunned_predicted = torch.max(prunned_logits.data, 1)
                total += labels.size(0)
                
                prunned_correct += (true_predicted_labels == labels.numpy()).sum().item()
            else:
                continue
            
            prunned_accuracy = 100 * prunned_correct / total
        
        mean_latency = np.mean(np.array(latency))
        # mean_latency = np.array(latency)[-1]

        
        prunned_results = [self.model_name + '_prunned', str(self.subset), self.type, self.percentage, prunned_accuracy, self.batch_size, mean_latency]

        return prunned_results
    
    def evaluate_original(self):

        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

        available_providers = ort.get_available_providers()
        if 'CUDAExecutionProvider' in  available_providers:
            providers = providers = [
                                        ('CUDAExecutionProvider', {
                                            'arena_extend_strategy': 'kNextPowerOfTwo',
                                            'gpu_mem_limit': 32 * 1024 * 1024 * 1024,  # 32 GB limit,
                                            "enable_cuda_graph": '1',
                                            "cudnn_conv1d_pad_to_nc1d": '1',
                                            "cudnn_conv_use_max_workspace": '1',
                                            'cudnn_conv_algo_search': 'EXHAUSTIVE'
                                        }),
                                        'CPUExecutionProvider'
                                    ]
        elif "CoreMLExecutionProvider" in available_providers:
            providers = ["CoreMLExecutionProvider"]
        else:
            providers = ['CPUExecutionProvider']

        file_name_original = 'resnet50_' + self.type + '_original_' + self.subset + '_' + str(self.percentage) + '.onnx' if self.subset else 'resnet50_' + self.type + '_original_' + str(self.percentage) + '.onnx'
        write_path_original = os.path.join(self.write_path, file_name_original)
        
        session = ort.InferenceSession(write_path_original, providers=providers)
        

        # Prepare for inference
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name
        input_shape = (self.batch_size, 3, 224, 224)
        num_classes = 1000
        output_shape = (self.batch_size, num_classes)  # For ResNet50 ImageNet classification

        # Allocate GPU memory for inputs and outputs
        input_tensor_gpu = torch.empty(input_shape, device='cuda', dtype=torch.float32)
        output_tensor_gpu = torch.empty(output_shape, device='cuda', dtype=torch.float32)

        # Create I/O binding and bind pre-allocated GPU tensors
        io_binding = session.io_binding()
        io_binding.bind_input(
            name=input_name,
            device_type='cuda',
            device_id=0,
            element_type=np.float32,
            shape=input_shape,
            buffer_ptr=input_tensor_gpu.data_ptr(),
        )
        io_binding.bind_output(
            name=output_name,
            device_type='cuda',
            device_id=0,
            element_type=np.float32,
            shape=output_shape,
            buffer_ptr=output_tensor_gpu.data_ptr(),
        )

        # Warm-up run for stable performance & CUDA Graph capture
        session.run_with_iobinding(io_binding)
        total = 0
        original_correct = 0
        latency = []
        # with torch.no_grad():
        for inputs, labels in tqdm(self.test_loader):
            if inputs.shape[0] == self.batch_size:
                inputs = inputs.squeeze(1)
                # inputs = inputs.numpy()  # Convert the tensor to a NumPy array
                # Transfer batch to GPU (using pinned memory & non-blocking transfer)
                input_tensor_gpu.copy_(inputs, non_blocking=True)
                start_time = time.time()
                session.run_with_iobinding(io_binding)
                torch.cuda.synchronize()  # Ensure accurate timing
                # prunned_outputs = self.quantized_model(inputs)
                end_time = time.time() - start_time
                latency.append(end_time)
                # Efficient approach
                probabilities = F.softmax(output_tensor_gpu, dim=1)  # Softmax on GPU
                predicted_labels = probabilities.argmax(dim=1).cpu().numpy()  # Argmax on GPU, then move to CPU if needed
                
                # prunned_, prunned_predicted = torch.max(prunned_logits.data, 1)
                total += labels.size(0)
                
                original_correct += (predicted_labels == labels.numpy()).sum().item()
            else:
                continue
        
        mean_latency = np.mean(np.array(latency))
        # mean_latency = np.array(latency)[-1]

        original_accuracy = 100 * original_correct / total

        original_results = [self.model_name + '_original', str(self.subset), self.type, self.percentage, original_accuracy, self.batch_size, mean_latency]
        
        return original_results
    
if __name__ == '__main__':

    available_providers = ort.get_available_providers()
    print("Available ONNX Runtime Providers:", available_providers)
    
    # Step 1:Load the ResNet50 model from Hugging Face
    model = ResNetForImageClassification.from_pretrained("microsoft/resnet-50")
    
    preprocessor = AutoImageProcessor.from_pretrained("microsoft/resnet-50")
    cores = torch.get_num_threads()
    
    # Set the number of threads
    #### Local testing:
    # global_folder_path =  "~/llm_adapt_serving"
    # imagenet_path = "~/inferdb-unstructured/data/IMAGENET"
    # target_platform = 'arm'
    # quantize = False
    # optimization_level = 'disable'
    ### Cluster variables
    imagenet_path = "/app/llm_adapt_serving/data"
    global_folder_path = "/app/llm_adapt_serving"
    target_platform = 'amd64'
    quantize = False
    optimization_level = 'disable'
    write_path = os.path.join(os.path.expanduser(global_folder_path), 'data/artifacts')
    
    
    # strategies = ['structured', 'unstructured']
    strategies = ['structured']
    # imagenet_subset_list = [None, 'animals', 'traffic']
    imagenet_subset_list = ['traffic']
    
    batch_size = 256
    results = []
    for imagenet_subset in imagenet_subset_list:
        for t in strategies:   
            for p in [0.1, 0.3, 0.5]:
                
                train_size = 0.5 if imagenet_subset == None else 1
                my_pruner = Pruner(t, 'resnet50', p, model, train_size, 1, cores, batch_size, write_path, imagenet_path, target_platform, quantize, optimization_level, imagenet_subset)
                my_pruner.main()
                
                evaluation_results = my_pruner.evaluate_prunning()
                results.append(evaluation_results)

        original_results = my_pruner.evaluate_original()
        results.append(original_results)

    results_df = pd.DataFrame(results, columns=['model name', 'subset', 'prunning type', 'prunning percentage', 'accuracy', 'batch size', 'latency'])
    csv_path = os.path.join(os.path.expanduser(write_path), 'prunning_results_all_cluster.csv') 

    print(f"File {csv_path} does not exist. Saving new data.")
    results_df.to_csv(csv_path, index=False)
    