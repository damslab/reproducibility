#!/bin/bash

cd /hpi/fs00/share/fg/rabl/ricardo.salazardiaz/data

# List of subfolders to process
subfolders=("train_images_0" "train_images_1" "train_images_2" "train_images_3" "train_images_4")

# Pattern to match
pattern="._*"

# Iterate over each subfolder
for folder in "${subfolders[@]}"; do
  if [ -d "$folder" ]; then
    echo "Processing folder: $folder"
    find "$folder" -type f -name "$pattern" -exec rm -f {} \;
    echo "Deleted files matching '$pattern' in $folder"
  else
    echo "Skipping $folder: Directory does not exist"
  fi
done

echo "Done!"