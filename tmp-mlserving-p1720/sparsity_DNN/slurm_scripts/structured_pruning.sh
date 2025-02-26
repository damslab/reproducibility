#!/bin/bash

ulimit -n 65536

cd /app/llm_adapt_serving

export PYTHONPATH=$PYTHONPATH:$(pwd)
# export OPENBLAS_NUM_THREADS=64
# export OMP_NUM_THREADS=64  # If OpenMP is used

python src/structured_pruning.py