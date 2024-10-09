import os
from PIL import Image
import torch
import torchvision.transforms as transforms

# Function to resize images in a folder
def resize_images(folder):
    for filename in os.listdir(folder):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".JPEG"):
            # Load the image
            image = Image.open(os.path.join(folder, filename))
            # Convert the image to a tensor
            image_tensor = transforms.ToTensor()(image)

            # Define the transform
            if image_tensor.shape[0] == 3:
                transform = transforms.Compose([
                        transforms.Resize(256),
                        transforms.CenterCrop(224),
                        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
                ])
            if image_tensor.shape[0] == 1:
                transform = transforms.Compose([
                        transforms.Resize(256),
                        transforms.CenterCrop(224),
                        transforms.Normalize(mean=[0.5], std=[0.5])
                ])

            # Apply the transform to the image
            resized_image_tensor = transform(image_tensor)
            print(filename,": ",resized_image_tensor.shape)
            # Convert the resized tensor image back to a PIL Image for saving
            resized_image = transforms.ToPILImage()(resized_image_tensor)

            # Save the resized image
            resized_image.save(os.path.join(folder, filename))

# Resize all images in all folders
dirc = "train_renamed"
folders = os.listdir(dirc)

# Check if each folder is a directory
for folder in folders:
    path = os.path.join(dirc, folder)
    if os.path.isdir(path):
        resize_images(path)

