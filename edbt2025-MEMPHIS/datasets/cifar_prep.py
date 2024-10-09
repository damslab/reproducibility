import numpy as np
from keras.datasets import cifar10
import csv

# Function to linearize all images and write the linearized images to a CSV file
def linearize(images, csv_file_path):
    # Linearize the images
    lin_images = []
    for image in images:
        image_array = np.array(image)
        linearized_image = image_array.reshape(-1)
        lin_images.append(linearized_image)

    # Write the images to the CSV file
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for image in lin_images:
            writer.writerow(image)

(trainX, trainy), (testX, testy) = cifar10.load_data()
csv_file = "/home/arnab/datasets/linearized_cifar.csv"

linearize(trainX, csv_file)

