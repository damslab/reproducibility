#!/bin/bash

# Check if parameters are provided
if [ $# -ne 2 ]; then
    echo "Error: Please provide model name and request rate"
    echo "Usage: $0 <model_name> <request_rate>"
    echo "Example: $0 meta-llama/Llama-2-13b-hf 8"
    exit 1
fi

model_name=$1
request_rates=$2

# Cleanup function
cleanup() {
    echo "Cleaning up..."
    pgrep python | xargs kill -9
    pgrep vllm | xargs kill -9
    sleep 5
}

configs=(
    "8 1 1"
    "4 2 1"
    "4 1 2"
    "2 4 1"
    "2 1 4"
    "2 2 2"
    "1 8 1"
    "1 1 8"
    "1 4 2"
    "1 2 4"
)

# Loop through each parallelism configuration
for config in "${configs[@]}"; do
    # Split the config string into individual values
    read -r dp tp pp <<< "$config"
    
    echo "+++++++ Running experiment with configuration: DP=$dp, TP=$tp, PP=$pp"
    
    # Run the experiment with current configuration
    sh data_parallel.sh $model_name $dp $tp $pp
    sleep 5
    
    # Loop through each request rate
    for rate in $request_rates; do
        echo "+++++++ Running with request rate: $rate"
        sh benchmark_request_rate_scaling.sh $model_name $rate
    done
    
    cleanup
    
    echo "Finished experiment with configuration: DP=$dp, TP=$tp, PP=$pp"
    echo "----------------------------------------"
done
