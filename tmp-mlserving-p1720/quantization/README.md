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


#### 
```bash
python scripts/eval_routing.py
```