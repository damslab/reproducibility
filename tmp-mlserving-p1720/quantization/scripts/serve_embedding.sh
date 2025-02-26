docker run \
--rm \
--runtime=nvidia \
-e PYTHONPATH=/scratchpad \
-e HF_HOME=/HF_HOME \
-v $(pwd)/.local:/local \
-v $HF_HOME/:/HF_HOME \
-p 8080:8080 \
--ipc=host --ulimit stack=67108864 \
ghcr.io/xiaozheyao/scratchpad:v0.1.5-x86_64 \
sp serve meta-llama/Llama-3.2-1B-Instruct --host 0.0.0.0 --port 8080 --tp-size 1 --is-embedding