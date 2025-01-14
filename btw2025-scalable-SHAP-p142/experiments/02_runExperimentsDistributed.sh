#!/bin/bash

cd ./02_experiments

echo "Running all distributed experiments. This can take 10+ hours..."
echo "--> Distributed Runtimes"
./test_runtimes_distributed.sh

echo "--> Weak Scaling"
./test_runtimes_weak_scaling_distributed.sh

cd ..
