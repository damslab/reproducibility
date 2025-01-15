#!/bin/bash

source ./python-venv/bin/activate

mkdir -p "./11_results"
cd ./03_evaluation

n_computations=100
if [ "${SHAP_FAST_EXP}" = "1" ]; then
  echo "SHAP_FAST_EXP is set. Running with just 10 computations per configuration to be faster."
  n_computations=10
fi

python3 plots_runtime.py --plots-path="../11_results/"

python3 plots_accuracy.py --plots-path="../11_results/" --max-computations="$n_computations"

cd ..
