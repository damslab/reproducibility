import os
models = [
    'meta-llama/Llama-3.1-8B-Instruct',
    'espressor/meta-llama.Llama-3.1-8B-Instruct_W8A8_int8',
    'espressor/meta-llama.Llama-3.1-8B-Instruct_W4A16',
    'espressor/meta-llama.Llama-3.1-8B-Instruct_W8A8_FP8',
]

jobs = []
# models = [x for x in models if 'FP8' not in x]
tasks = "logiqa,boolq,truthfulqa,openbookqa,mmlu"
for model in models:
    job = f"lm_eval --model vllm --model_args pretrained={model},tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.85,max_model_len=4096 --tasks {tasks} --use_cache .local/cache/{model} --output_path .local/eval_results/{model} --batch_size 4"
