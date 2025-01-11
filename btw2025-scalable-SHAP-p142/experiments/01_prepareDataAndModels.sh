#!/bin/bash
set -e

echo "========================================================================"
echo "Downloading and preparing data and training models"
echo "========================================================================"

cd ./01_preparation

./downloadData.sh
./prepareAndTrain.sh

if ../00_setup/checkSpark.sh; then
  echo "Trying to copy data and models to HDFS."
  set +e
  ./copyToHdfs.sh
  set -e
fi


cd ..
