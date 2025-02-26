FROM vllm/vllm-openai

COPY . /workspace
WORKDIR /workspace


# Install dependencies
RUN git clone --depth 1 https://github.com/EleutherAI/lm-evaluation-harness && cd lm-evaluation-harness && pip install -e .
RUN pip install llmcompressor && pip uninstall pynvml -y

ENTRYPOINT ["/usr/bin/env"]