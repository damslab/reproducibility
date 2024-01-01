import os
from PIL import Image
import numpy as np
import csv

# Function to linearize all images and write the linearized images to a CSV file
def linearize(image_folder, csv_file_path):
    # Open the CSV file for writing
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Loop through all images in the folder
        for filename in os.listdir(image_folder):
            if filename.endswith(".jpg") or filename.endswith(".JPEG") or filename.endswith(".png"):
                # Load the image
                image = Image.open(os.path.join(image_folder, filename))

                # Linearize the image array
                image_array = np.array(image)
                linearized_image = image_array.reshape(-1)

                # Write the linearized image to the CSV file
                writer.writerow(linearized_image)

dirc = "test"
csv_file = "linearized_images.csv"

linearize(dirc, csv_file)
