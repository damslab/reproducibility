## Reproducibility Submission for Paper 2528

**Paper name:** UPLIFT: Parallelization Strategies for Feature Transformations
in Machine Learning Workloads

Source Code Info
 - Repository: Apache SystemDS [1] (https://github.com/apache/systemds), specifically the [transform](https://github.com/apache/systemds/tree/main/src/main/java/org/apache/sysds/runtime/transform) package.
 Commit hash: [66e8bd58bb5ed9c51afdfe391d5f0246b8bf383d](https://github.com/apache/systemds/commit/66e8bd58bb5ed9c51afdfe391d5f0246b8bf383d)
 - Programming Language: Java, Python, R, SystemDS DML (a R-like Domain Specific Language)
 - Additional Programming Language info: Java version 11 is required

Hardware Info to Reproduce Experiment Results

 - Processor: Intel(R) Xeon(R) Platinum 8175M CPU @ 2.50GHz or above
 - Cores: 16 physical cores (32 vCores)
 - Memory: 128GB. 110GB JVM heap is needed for the experiments
 - Disk: SSD, at least 60GB. More is better.

Experimentation Info

 - Environment: Ubuntu 20.04 LTS is used for the experiments. However, Apache SystemDS and the experiments are fully portable to any OS.
-----------------------------------

### Step-by-step Execution

**Step 1:** System setup.

Install jdk11, maven, python3, and r-base. Java 11 and Maven are needed to build the source code. Python is required to execute the baselines. We use R to generate the plots.

**Step 2:** Clone and build the source code.

Clone Apache SystemDS and check out the commit hash. Next, follow the [documentation](https://systemds.apache.org/docs/3.0.0/site/install) to build SystemDS from source.

**Step 3:** Download and prepare the datasets.

All the datasets are publicly available. Use script `getAndPrep.sh` in the `datasets/` directory to automatically download and prepare the datasets. pass the use case ID as an argument to the script. E.g. `./getAndPrep.sh T5`.

**Step 4:** Run micro benchmarks.

Use `java -cp` with the SystemDS jar to execute the micro benchmarks in the `microbenchmarks/` directory.

**Step 5:** Run feature transformation benchmark, FTBench.

In this paper, we define a feature transformation benchmark, FTBench to foster research on feature transformations. FTBench documents 15 use cases, which are discussed in detail in the paper. We as well provide two full reference implementations and a few partial implementations of the benchmark.
1. Scripts to execute all the use cases in SystemDS and UPLIFT are available in `FTBench/systemds/` directory.
2. For the other baselines, install Scikit-learn 1.0.2, Keras on Tensorflow 2.8, pyspark 3.1.2, and dask. Scikit-learn implementation of all the use cases are in `/FTBench/scikit-learn`.  Additionally, we used specialized systems such as Keras, spark\.ml and dask to implement a subset of use cases.  They are available inside respective folders.
3. We further explored ml\.net's python binding NimbusML to implement one use case, T3. Even though that is not used in the paper experiments, we made it available here.


--------------------------------------


*[1] Matthias Boehm, Iulian Antonov, Sebastian Baunsgaard, Mark Dokter, Robert Ginthör, Kevin Innerebner, Florijan Klezin, Stefanie N. Lindstaedt, Arnab Phani, Benjamin Rath, Berthold Reinwald, Shafaq Siddiqui, and Sebastian Benjamin
Wrede. 2020. SystemDS: A Declarative Machine Learning System for the End-to-End Data Science Lifecycle. In CIDR.*
