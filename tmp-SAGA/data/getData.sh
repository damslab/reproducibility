# Download the dataset EEG
mkdir -p EEG
wget https://www.dropbox.com/s/nerfrhbrseev928/CleanML-datasets-2020.zip?dl=0&file_subpath=%2Fdata%2FEEG%2Fraw
mv raw.csv EEG.csv
# # split into train test
python splitData.py EEG
