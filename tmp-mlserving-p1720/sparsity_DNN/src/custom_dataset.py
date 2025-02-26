from torch.utils.data import Dataset
import os
from imagenet_classes import IMAGENET2012_CLASSES
from PIL import Image
from extract_imagenet_subclasses import get_subset_labels

class CustomDataset(Dataset):
    def __init__(self, img_dir, subset=None, transform=None):
        super().__init__()  # Initialize the Parent class
        if subset:
            subset_classes = get_subset_labels(subset)
            self.img_labels = [i for i in os.listdir(img_dir) if any(label in i for label in subset_classes)]
        else:
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