#!/bin/bash
set -e

echo "Starting Preparation Adult"
./runSystemDS -f "prepareAdult.dml"
echo "Starting Preparation Census"
./runSystemDS -f "prepareCensus.dml"

echo "Training MLR on Adult"
./runSystemDS -f "trainMultiLogReg_adult.dml"
echo "Training SVM on Census"
./runSystemDS -f "trainSVM_census.dml"
echo "Training basic FNN on Adult"
./runSystemDS -f "trainFNN_adult.dml"

echo "Training FNNs with varying layers on Adult"
for layers in 1 2 4 8; do
  ./runSystemDS -f "trainVaryingLayersFNN_adult/ffTrain${layers}.dml"
done

echo "Testing FNN with varying layers on Adult"
./runSystemDS -f "trainVaryingLayersFNN_adult/ffPredict_test.dml"

echo "Preparing Partitions to simulate feature scaling."
./runSystemDS -f preparePartitionsForFeatureScaling.dml

source "../python-venv/bin/activate"

echo "Training MLR in Python"
python3 ./python_trainMultiLogReg_adult.py 
echo "Training FNN in Python"
python3 ./python_trainFNN_adult.py
