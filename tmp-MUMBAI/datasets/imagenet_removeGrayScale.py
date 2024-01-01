import os
from PIL import Image
import torch
import torchvision.transforms as transforms

# Function to resize images in a folder
def remove_grayscale(folder):
    grayscale_image_count = 0
    for filename in os.listdir(folder):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".JPEG"):
            # Load the image
            image = Image.open(os.path.join(folder, filename))
            # Convert the image to a tensor
            image_tensor = transforms.ToTensor()(image)

            # Check if grayscale
            if image_tensor.shape[0] == 1:
                # Remove the grayscale image
                os.remove(os.path.join(folder, filename))
                grayscale_image_count += 1
    return grayscale_image_count


# Resize all images in all folders
dirc = "train_renamed"
folders = os.listdir(dirc)

# Check if each folder is a directory
total_grayscale_image_count = 0
for folder in folders:
    path = os.path.join(dirc, folder)
    if os.path.isdir(path):
        grayscale_image_count = remove_grayscale(path)
        total_grayscale_image_count += grayscale_image_count

print("Total grayscale images removed:", total_grayscale_image_count)

