
## Reproducibility Submission for MEMPHIS

**Paper name:** MEMPHIS: Holistic Lineage-based Reuse and 
Memory Management for Multi- backend ML Systems

Source Code Info
 - Repository: Apache SystemDS [1] (https://github.com/apache/systemds).
 - Programming Language: Java, Python, R, SystemDS DML (a R-like Domain Specific Language)
 - Additional Programming Language info: Java version 11 is required

Hardware Info to Reproduce Experiment Results

 - Processor: AMD EPYC 744P CPU @ 2.80GHz or above
 - Cores: 24 physical cores (48 vCores)
 - Memory: 38GP driver, 230GB executors, 20GB bufferpool, 7GB operation memory, 5GB lineage cache
 - Disk: SSD, at least 60GB. More is better.

Experimentation Info

 - Environment: Ubuntu 20.04 LTS is used for the experiments. However, Apache SystemDS and the experiments are fully portable to any OS. CUDA 10.2, CUDNN 7.6.
-----------------------------------

### Step-by-step Execution

**Step 1:** System setup.

Install jdk11, maven, python3, cuda10.2 cudnn7.6 PyTorch2.1. Java 11 and Maven are needed to build the source code. Python is required to execute the baselines. We use R to generate the plots.

**Step 2:** Clone and build the source code.

Clone Apache SystemDS. Next, follow the [documentation](https://systemds.apache.org/docs/3.0.0/site/install) to build SystemDS from source.

**Step 3:** Download and prepare the datasets.

All the datasets are publicly available. `datasets/` directory contains the scripts to prepare the datasets.

**Step 4:** Run micro benchmarks.

Execute the shell scripts in the `microbenchmarks/` directory.

**Step 5:** Run End-to-End ML pipelines and compare with other reuse frameworks.

Execute the shell scripts in the `MLPipelines` directory.

**Step 6:** Run other ML systems (PyTorch) for comparison.

Execute the PyTorch scripts in the `MLSystemsComparison` directory.

--------------------------------------


*[1] Matthias Boehm, Iulian Antonov, Sebastian Baunsgaard, Mark Dokter, Robert Ginthör, Kevin Innerebner, Florijan Klezin, Stefanie N. Lindstaedt, Arnab Phani, Benjamin Rath, Berthold Reinwald, Shafaq Siddiqui, and Sebastian Benjamin
Wrede. 2020. SystemDS: A Declarative Machine Learning System for the End-to-End Data Science Lifecycle. In CIDR.*

