#!/bin/bash

# Check if 4 parameters are provided
if [ $# -eq 4 ]; then
    # Define the model name, dp_degree, tp_degree, and pp_degree as command line arguments
    model_name=$1
    dp_degree=$2
    tp_degree=$3
    pp_degree=$4
    echo "Serving model name: $model_name"
    echo "Data Parallel Degree: $dp_degree"
    echo "Tensor Parallel Degree: $tp_degree"
    echo "Pipeline Parallel Degree: $pp_degree"
else
    echo "Error: Please provide exactly 4 parameters: model_name, dp_degree, tp_degree, and pp_degree."
    exit 1
fi
sleep 1

# Trap the SIGINT signal (triggered by Ctrl+C)
trap 'cleanup' INT

# Cleanup function
cleanup() {
    echo "Caught Ctrl+C, cleaning up..."
    # Cleanup commands
    pgrep python | xargs kill -9
    pkill -f python
    echo "Cleanup complete. Exiting."
    exit 0
}

# a function that waits vLLM server to start
wait_for_server() {
  local port=$1
  timeout 1200 bash -c "
    until curl -s localhost:${port}/v1/completions > /dev/null; do
      sleep 1
    done" && return 0 || return 1
}

# Launch vLLM instances for data parallel serving
i=0
while [ $i -lt $dp_degree ]; do
    # Calculate GPU device IDs for this instance
    gpu_ids=""
    start_gpu=$((i * pp_degree * tp_degree))
    j=0
    while [ $j -lt $((pp_degree * tp_degree)) ]; do
        if [ -n "$gpu_ids" ]; then
            gpu_ids="${gpu_ids},"
        fi
        gpu_ids="${gpu_ids}$((start_gpu + j))"
        j=$((j + 1))
    done

    # Launch vLLM instance
    port=$((8100 + i*100))
    CUDA_VISIBLE_DEVICES=$gpu_ids vllm serve $model_name \
        --port $port \
        --pipeline-parallel-size $pp_degree \
        --tensor-parallel-size $tp_degree \
        --disable-log-request \
        --max_model_len 16384 \
        --gpu-memory-utilization 0.9 &
    
    echo "Launched vLLM instance $((i+1)) on GPUs: $gpu_ids port: $port"
    i=$((i + 1))
done

# Wait for all instances to be ready
i=0
while [ $i -lt $dp_degree ]; do
    port=$((8100 + i*100))
    wait_for_server $port
    i=$((i + 1))
done

# launch a proxy server that opens the service at port 8000
# the workflow of this proxy:
# - send the request to prefill vLLM instance (port 8100), change max_tokens 
#   to 1
# - after the prefill vLLM finishes prefill, send the request to decode vLLM 
#   instance
# NOTE: the usage of this API is subject to change --- in the future we will 
# introduce "vllm connect" to connect between prefill and decode instances
python3 ./benchmarks/round_robin_proxy.py --num_servers $dp_degree &
sleep 1

# serve two example requests
output1=$(curl -X POST -s http://localhost:8000/v1/completions \
-H "Content-Type: application/json" \
-d '{
"model": "'"$model_name"'",
"prompt": "San Francisco is a",
"max_tokens": 10,
"temperature": 0
}')

output2=$(curl -X POST -s http://localhost:8000/v1/completions \
-H "Content-Type: application/json" \
-d '{
"model": "'"$model_name"'",
"prompt": "Santa Clara is a",
"max_tokens": 10,
"temperature": 0
}')


# Cleanup commands
# pgrep python | xargs kill -9
# pgrep vllm | xargs kill -9 
# pkill -f python

echo ""

sleep 1

# Print the outputs of the curl requests
echo ""
echo "Output of first request: $output1"
echo "Output of second request: $output2"

echo "🎉🎉 Successfully finished 2 test requests! 🎉🎉"
echo ""
