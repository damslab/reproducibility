import os
from PIL import Image
import shutil

# Function to copy 20 images from 500 test folders
def copy_selected_images():
    # Create the "test" folder if it doesn't exist
    if not os.path.exists("test"):
        os.makedirs("test")

    total_copied_image_count = 0
    # Loop through the first 500 folders
    dirc = "train_renamed"
    folders = os.listdir(dirc)[:500]
    for folder in folders:
        path = os.path.join(dirc, folder)
        selected_image_count = 0
        if os.path.isdir(path):
            for filename in os.listdir(path):
                if filename.endswith(".jpg") or filename.endswith(".JPEG") or filename.endswith(".png"):
                    # Copy the image to the "test" folder
                    shutil.copy2(os.path.join(path, filename), "test")
                    selected_image_count += 1
                    total_copied_image_count += 1

                    # Move to the next folder after copying 20 images
                    if selected_image_count >= 20:
                        break

    print("Successfully copied", total_copied_image_count, "images to the 'test' folder.")

copy_selected_images()
