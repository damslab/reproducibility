#!/bin/bash

# Check if parameters are provided
if [ $# -ne 2 ]; then
    echo "Error: Please provide model name and number of GPUs"
    echo "Usage: $0 <model_name> <num_gpus>"
    echo "Example: $0 meta-llama/Llama-2-13b-hf 8"
    exit 1
fi

model_name=$1
num_gpus=$2

# Cleanup function
cleanup() {
    echo "Cleaning up..."
    pgrep python | xargs kill -9
    pgrep vllm | xargs kill -9
    sleep 5
}

request_rates="1 2 4 8 16 32 64 128 256"

echo "+++++++ Running request rate scaling experiments for $model_name with $num_gpus x Data Parallelism"
sh data_parallel.sh $model_name $num_gpus 1 1
sleep 5
for rate in $request_rates; do
    echo "+++++++ Running with request rate: $rate"
    sh benchmark_request_rate_scaling.sh $model_name $rate
done
cleanup

echo "+++++++ Running request rate scaling experiments for $model_name with $num_gpus x Tensor Parallelism"
sh data_parallel.sh $model_name 1 $num_gpus 1
sleep 5
for rate in $request_rates; do
    echo "+++++++ Running with request rate: $rate"
    sh benchmark_request_rate_scaling.sh $model_name $rate
done
cleanup

echo "+++++++ Running request rate scaling experiments for $model_name with $num_gpus x Pipeline Parallelism"
sh data_parallel.sh $model_name 1 1 $num_gpus
sleep 5
for rate in $request_rates; do
    echo "+++++++ Running with request rate: $rate"
    sh benchmark_request_rate_scaling.sh $model_name $rate
done
cleanup
