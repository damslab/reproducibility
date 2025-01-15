#!/bin/bash

source ./python-venv/bin/activate

mkdir -p "./11_results"
cd ./03_evaluation

python3 plots_runtime.py --plots-path="../11_results/"

python3 plots_accuracy.py --plots-path="../11_results/"

cd ..
