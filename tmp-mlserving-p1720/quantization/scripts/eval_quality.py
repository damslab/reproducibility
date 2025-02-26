import os

job_template ="""
docker run \
--rm \
--runtime=nvidia \
-e HF_HOME=/HF_HOME \
-v $(pwd)/.local:/local \
-v $HF_HOME/:/HF_HOME \
ghcr.io/xiaozheyao/adaml:0.0.1 \
lm_eval --model vllm --model_args pretrained={model},tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.85,max_model_len=4096 --tasks {tasks} --use_cache /local/cache/{model} --output_path /local/eval_results/{model} --batch_size 4
"""

models = [
    'meta-llama/Llama-3.1-8B-Instruct',
    'espressor/meta-llama.Llama-3.1-8B-Instruct_W8A8_int8',
    'espressor/meta-llama.Llama-3.1-8B-Instruct_W4A16',
    'espressor/meta-llama.Llama-3.1-8B-Instruct_W8A8_FP8',
]
tasks = "logiqa,boolq,truthfulqa,openbookqa,mmlu"
for model in models:
    job = job_template.format(model=model, tasks=tasks)
    # print(job)
    os.system(job)