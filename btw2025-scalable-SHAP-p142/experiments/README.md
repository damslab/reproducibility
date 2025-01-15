## Reproducibility Submission BTW 2025, Paper 142
### Running the experiments

Experiments are split into local and distributed experiments. 
The scripts in the [00_setup](00_setup) dir install all packages and systemds necessary to run the local experiments.
For distributed execution, a spark cluster has to be available and HDF for data storage.

Since these experiments take a long time, using `tmux` and running them in a detached session might come in handy.

>The scripts can also be executed independently, as long as all prior scripts ran at least once.
Make sure to execute them from within their directory, since sourcing in scripts is always relative to the working directory.

### Local Experiments
`runAllLocal.sh` sets everything up, runs all local experiments and generates all plots from these experiment into 
[11_results](11_results). 
Since we are collecting runtimes from multiple methods of which each on their own already runs for up to 1h, 
it is likely that the experiments take >12h.

The actual runtime experiments [02_experiments/test_runtimes_local.sh](02_experiments%2Ftest_runtimes_local.sh) can be 
stopped at any given time to only get runtimes up to the current number of instances.
In this case, executing the following scripts should still produce 
plots for all runtimes that were collected up to this point. 

To do this it runs the following scripts:

- [runAllLocal.sh](runAllLocal.sh)
  - [run0_SetupSystem.sh](run0_SetupSystem.sh)
    - [00_setup/installAptPackages.sh](00_setup%2FinstallAptPackages.sh)
    - [00_setup/pythonSetup.sh](00_setup%2FpythonSetup.sh)
    - [00_setup/buildSystemDS.sh](00_setup%2FbuildSystemDS.sh)
    - [00_setup/checkSpark.sh](00_setup%2FcheckSpark.sh)
  
  - [run1_PrepareDataAndModels.sh](run1_PrepareDataAndModels.sh)
    - [01_preparation/downloadData.sh](01_preparation%2FdownloadData.sh)
    - [01_preparation/prepareAndTrain.sh](01_preparation%2FprepareAndTrain.sh)
    - [01_preparation/copyToHdfs.sh](01_preparation%2FcopyToHdfs.sh)
  
  - [run2_1ExperimentsLocal.sh](run2_1ExperimentsLocal.sh)
    - [02_experiments/test_runtimes_local.sh](02_experiments%2Ftest_runtimes_local.sh)
    - [02_experiments/testAccuracy.sh](02_experiments%2FtestAccuracy.sh)
    - [02_experiments/computeLargeBaseline.sh](02_experiments%2FcomputeLargeBaseline.sh)

  - [run3_1GeneratePlotsLocal.sh](run3_1GeneratePlotsLocal.sh)
    - `python3 plots_runtime.py --plots-path="../11_results/"`
    - `python3 plots_accuracy.py --plots-path="../11_results/"`



### Distributed Experiments
`runAllDistributed.sh` runs the experiments that need a spark cluster and HadoopFS. 
It expects that at least [run0_SetupSystem.sh](run0_SetupSystem.sh) and [run1_PrepareDataAndModels.sh](run1_PrepareDataAndModels.sh)
were executed once, so that the models are available in HDFS. AS with the local experiments, these test can run for >12h.
It generates the remaining plots into [11_results](11_results).

If [02_experiments/test_runtimes_local.sh](02_experiments%2Ftest_runtimes_local.sh) was not run for all instances configured,
it is possible that some speed-up plots may show unexpected results or do not render at all.
This is due to the fact that the plots reuse the runtimes from local as runtimes for single-node execution.

- [runAllDistributed.sh](runAllDistributed.sh)
  - [run2_2ExperimentsDistributed.sh](run2_2ExperimentsDistributed.sh)
    - [test_runtimes_distributed.sh](02_experiments%2Ftest_runtimes_distributed.sh)
    - [test_runtimes_weak_scaling_distributed.sh](02_experiments%2Ftest_runtimes_weak_scaling_distributed.sh)
  - [run3_2GeneratePlotsDistributed.sh](run3_2GeneratePlotsDistributed.sh)
    - `python3 plots_runtime.py --distributed --plots-path="../11_results/"`
    

## Accept more variance in results, but run faster
You can export the env var `FAST_SHAP_EXP=1` in your terminal to run the experiments with fewer samples etc. 
This may produce less accurate results and more variance in runtimes, but can cut total runtime down to approximately 8h.

