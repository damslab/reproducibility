#!/bin/bash

cd ./02_experiments

echo "Running all local experiments. This can take 10+ hours..."
echo "--> Local Runtimes"
./test_runtimes_local.sh

echo "--> Accuracy"
./testAccuracy.sh

echo "--> Large Baseline (This can take multiple hours)"
./computeLargeBaseline.sh

cd ..
