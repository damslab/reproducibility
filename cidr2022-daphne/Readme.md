# Reproducibility Scripts for Daphne CIDR2022 Submission
*DAPHNE: An Open and Extensible System Infrastructure for Integrated Data Analysis Pipelines*

Paper link: http://www.cidrdb.org/cidr2022/papers/p4-damme.pdf

## Getting Started

The scripts contained in this repository reproduce the results presented in the paper. After checking with the hardware 
and software requirements below, the results and plots should be produced by running `run-all.sh`. Alternatively,
the numbered scripts (`1_setup_env.sh`, `...`) can be run independently in sequence.

Once the experiment execution completes successfully, the data and plots can be found in the results directory in the repository root.


### Hardware Requirements
* Nvidia GPU, Turing Architecture (may run on Pascal or Volta, does not run on Ampere)
  * 16 GB for the inference parts of experiment P2
  * 32 GB to train the model on GPU. Alternatively the model can slowly be trained on CPU (20 minutes per epoch on the 112 
    core reference system). To train on CPU, insert `export CUDA_VISIBLE_DEVICES=""` at the beginning of 
    `2_setup_p2_data.sh`
* 32 GB main memory
* 100 GB disk space
* "Decent" network connection (~70 GB download size)
### Software Requirements

To run the experiments the following list of prerequisites should be considered:

* Root privileges *might* be required to install software dependencies
  * [Singularity-CE 3.9.x](https://github.com/sylabs/singularity) is needed to set up the experiment environment. 
    Install from package (sudo/root required) or [compile from source](https://sylabs.io/guides/3.9/user-guide/quick_start.html#quick-installation-steps)
  * Building the container image requires sudo/root privileges or a [fakeroot setup](https://sylabs.io/guides/3.9/user-guide/fakeroot.html) 
    Alternatively you can run the build step () on a computer where you have the required privileges using the definition file [provided in this repository](resources/singularity-container.def)
    to create the container image and copy it to the machine where you intend to run the experiments. The image needs to be in the 
    root directory of your copy of this repository and the file name needs to be  **experiment-sandbox.sif**
  * CUDA 10.2 + CUDNN 7.6.5 and CUDA 11.4.1 + CUDNN 8.2.2 will be set up locally and integrated into the container - no system installation needed.
    For this to work, the files 
    [cudnn-10.2-linux-x64-v7.6.5.32.tgz](https://developer.nvidia.com/compute/machine-learning/cudnn/secure/7.6.5.32/Production/10.2_20191118/cudnn-10.2-linux-x64-v7.6.5.32.tgz) 
    and 
    [cudnn-11.4-linux-x64-v8.2.2.26.tgz](https://developer.nvidia.com/compute/machine-learning/cudnn/secure/8.2.2/11.4_07062021/cudnn-11.4-linux-x64-v8.2.2.26.tgz) 
    need to be downloaded manually (due to license restrictions) and placed in the repository root.
  
# Experiment Description

There are three groups of experiments. The micro benchmark experiments run kmeans and a linear regression model, 
the pipeline P1 runs database queries and a linear regression model and the pipeline P2 runs the inference step of a 
resnet20 neural network on a dataset of satellite images.
## Reference System
The system, these experiments originally ran on has the following specs:
* System: HPE ProLiant DL380 Gen10/ProLiant DL380 Gen10
* CPU: 2 x Intel(R) Xeon(R) Gold 6238R CPU @ 2.20GHz
* RAM: 768 GB DDR4 2933 MT/s (12 x 64 GB DIMMs)  
* GPU: Nvidia Tesla T4
* Disk: HPE SSD SATA 6Gb/s

## Experiment MicroBenchmarks
- LM: training of linear regression model
- k-means clustering
#### Environment
- Note that we used commit 4d6db3c7bbf29cff89004cc55d1852836469302b of the master branch for the micro benchmarks.
- `python3` with the following libraries (versions used for the CIDR submission's experiments in brackets):
  - `matplotlib` (3.4.3)
  - `numpy` (1.21.2)
  - `pandas` (1.3.2)
  - `seaborn` (0.11.2)
  - `tensorflow` (2.6.0)

## Experiment P1
#### Environment
- Note that we used commit 549b05660f9bea874765135f4c5c4af67f843ac2 of the master branch for the P1 experiments.
- `python3` with the following libraries (versions used for the CIDR submission's experiments in brackets):
  - `duckdb` (0.2.7)
  - `matplotlib` (3.4.3)
  - `numpy` (1.21.2)
  - `pandas` (1.3.2)
  - `seaborn` (0.11.2)
  - `tensorflow` (2.6.0)
- Note that the TPC-H data generator (2.4.0) is automatically downloaded and built.
- Note that MonetDB (11.39.17) is automatically downloaded, built, and installed locally.

### Queries
Pipeline P1 consists of a relational query followed by a linear regression model training on the query output.
We experimented with two queries (referred to as `a` and `b`).
The queries can be found in `p1-a.daphne`/`p1-b.daphne` and in `eval.sh`.

### For the CIDR submission
We used
- TPC-H data at scale factor 10
- query `a`
- 3 repetitions

## Experiment P2
#### Environment
* TF Version 2.6.0 pip-installed in a virtual environment (Ubuntu 20.04, python 3.8.10)
* SystemDS based on commit 5deaa1acd40890d09428b424ce35162c774706da plus an additional bugfix from 007b684a99090b178ec33d3c75f38f7ccaccf07a
  - JVM config: -Xmx16g -Xms16g -Xmn512m
  - SysDS settings used: MKL; single/parallel io; optLevel: 4; single floating point precision
* Daphne based on tip of branch p2-alpha
* Training was conducted on an external system with a larger GPU

#### Dataset
* [So2Sat LCZ42 version 2 testing set](https://mediatum.ub.tum.de/1483140) (24188 images)
* Preprocessing done with convertH5imagesToCSV.py:
  * Extracted from HDF5 to CSV
  * Converted to NCHW format
  * Mean removed
* I tried to run the TF inference on the training set, but that did crash in all variants I tried:
  * w/ TF Dataset API
  * w/o -"-
  * w/ eager mode (default for TF 2.x)
  * w/o eager
* Data loading for TF was done with Pandas
#### Model
* Trained with resnet20-training.py for 200 epochs
* Saved only best performing models (-> happened after epoch 15)
* For TF/XLA, the h5 saved model was used
* For Daphne/SystemDS the model was exported to CSV with tf-model-export.py
