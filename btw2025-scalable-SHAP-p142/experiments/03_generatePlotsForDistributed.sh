#!/bin/bash

source ./python-venv/bin/activate

cd ./03_evaluation

python3 plots_runtime.py --distributed

cd ..
