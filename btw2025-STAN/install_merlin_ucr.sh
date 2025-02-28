#!/bin/bash
# We slightly modified to preserve MERLIN3_1.m to add it to the root directory

DATADIR="data"
TARGET="ucraa"

# check if dataset already installed
if [ -d "$DATADIR/$TARGET" ]; then
  printf "UCR Anomaly Archive already installed!\n"
  exit 0
fi

# create dataroot dir if not exists
mkdir -p $DATADIR
# create tmp dir
mkdir -p tmp && cd tmp

# Download the dataset
if command -v wget > /dev/null; then
  wget https://www.cs.ucr.edu/~eamonn/time_series_data_2018/UCR_TimeSeriesAnomalyDatasets2021.zip
elif command -v curl > /dev/null; then
  curl -O https://www.cs.ucr.edu/~eamonn/time_series_data_2018/UCR_TimeSeriesAnomalyDatasets2021.zip
else
  printf "Error: Neither wget nor curl is installed.\n"
  exit 1
fi

# Unzip the dataset
if command -v unzip > /dev/null; then
  unzip UCR_TimeSeriesAnomalyDatasets2021.zip -d $TARGET
else
  printf "Error: unzip is not installed.\n"
  exit 1
fi

# Move to data dir
mv ./$TARGET/AnomalyDatasets_2021/UCR_TimeSeriesAnomalyDatasets2021/FilesAreInHere/UCR_Anomaly_FullData ../$DATADIR/$TARGET

# Move Merlin to the root
mv ./$TARGET/AnomalyDatasets_2021/UCR_TimeSeriesAnomalyDatasets2021/FilesAreInHere/introducingMERLIN/MERLIN3_1.m ../stan_alone/

# Clean up
cd ..
rm -rf tmp

printf "UCR Anomaly Archive successfully installed in $DATADIR/$TARGET\n"
printf "MERLIN3_1.m successfully installed in the root directory\n"