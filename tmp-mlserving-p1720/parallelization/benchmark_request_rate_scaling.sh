#!/bin/bash

# Check if parameters are provided
if [ $# -ne 2 ]; then
    echo "Error: Please provide model name and request rates"
    echo "Usage: $0 <model_name> <request_rates>"
    echo "Example: $0 meta-llama/Llama-2-13b-hf \"1 2 4 8 16 32 64 128\""
    exit 1
fi

model_name=$1
request_rates=$2

# Loop through each request rate
for rate in $request_rates; do
    echo "+++++++ Running with request rate: $rate"
    python3 benchmarks/benchmark_serving.py \
        --backend openai \
        --model $model_name \
        --dataset-name sharegpt \
        --dataset-path ~/data/ShareGPT_V3_unfiltered_cleaned_split.json \
        --num-prompts 512 \
        --request-rate $rate
done