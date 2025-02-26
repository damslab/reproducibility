# Artifacts
For `Towards Workload-aware Optimization and Reconfiguration of ML Serving Pipelines`

## Setup
```
conda create --name <env_name> python=3.12 -y
conda activate <env_name>
conda install nvidia/label/cuda-12.2.2::cuda-toolkit
pip install vllm datasets
```

## vLLM Request Rate Scaling Experiments
The following script benchmarks the latency/throughput of vLLM as we scale up the request rate for different types of parallelism (data, pipeline, tensor). We configure the script to benchmark LLama 13B on 4 GPUs with request rates 1-128. The output is redirected to a log file.

```
sh ./request_rate_scaling_experiments.sh meta-llama/Llama-2-13b 4 > /tmp/13b_rr_scaling.log 2>&1 &
```

We then use the following script to parse the output and generate latency/throughput vs request rate plots.

```
python utils/parse_request_scaling_experiments.py --file_path /tmp/13b_rr_scaling.log
```

## vLLM Hybrid Parallelism Experiments
The following script benchmarks the latency/throughput of vLLM with different combinations of data/pipeline/tensor parallelism. Assumes a node with 8 GPUs. We configure the script for an int8 quantized LLama 70B model on 8 GPUs and benchmark request rates 8 and 32. The output is redirected to a log file.

```
sh ./hybrid_parallelism_experiments.sh neuralmagic/Meta-Llama-3.1-70B-Instruct-quanti
zed.w8a8 "8 32" > /tmp/70b_hybrid_parallel.log 2>&1 &
```

We then use the following script to parse the outputs and generate latency vs throughput plots

```
python utils/parse_hybrid_parallelism_experiments.py --file_path /tmp/70b_hybrid_parallel.log
```