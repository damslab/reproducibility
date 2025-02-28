## Artifact for Adaptive ML

#### Evaluate Post-Compression Model Accuracy

```bash
python scripts/eval_quality.py
```

This could take several hours to run. Ideally the script should be executed on a machine with Hopper GPU for fp8 support.

Once this finishes, we run the following script to aggregate the results:

```bash
python scripts/parse_eval_results.py
```

and plot the results figure:

```bash
python scripts/plot_accuracy.py
```


#### Evaluate Performance of Model Router

First we need to start an embedding model server:

```
bash scripts/serve_embeddings.sh
```

and then we can start evaluating the router performance

```bash
python scripts/eval_routing.py
```

and plot the results:

```
python scripts/plot_router_results.py
```

You can also find the training and testing data on this [HuggingFace repository](https://huggingface.co/datasets/xiaozheyao/mmlu_responses/tree/main)
