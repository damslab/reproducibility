import os
import shutil
 
# Update the folder names with class labels

MAP_CLASS_LOC = "LOC_synset_mapping.txt"
 
class_dir_map = {}
id_class_map = {}
 
with open(MAP_CLASS_LOC, "r") as map_class_file:
    rows = map_class_file.readlines()
    for row in rows:
        row = row.replace(',','')
        row = row.strip()
        arr = row.split(" ")
        class_dir_map[arr[0]] = arr[1]
 
TRAIN_DATA_FOLDER = "train/"
renamed_folder = "train_renamed/"

# Rename and move to a new folder
# FIXME: Multiple folders map to same name (water buffalo, water snake)
for file in os.listdir(TRAIN_DATA_FOLDER):
    shutil.move(os.path.join(TRAIN_DATA_FOLDER, file), os.path.join(renamed_folder, class_dir_map[file]))

