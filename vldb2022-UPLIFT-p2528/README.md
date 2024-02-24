## Reproducibility Submission for Paper 2528

**Paper name:** UPLIFT: Parallelization Strategies for Feature Transformations
in Machine Learning Workloads

Source Code:
 - Repository: [Apache SystemDS](https://github.com/apache/systemds) [1]. 
 - Specific package: [transform](https://github.com/apache/systemds/tree/main/src/main/java/org/apache/sysds/runtime/transform).
 - Commit hash: [42b3caae0ad5a0563427358794559be1fc420ef7](https://github.com/apache/systemds/commit/42b3caae0ad5a0563427358794559be1fc420ef7)
 - Programming Language: Java (version 11), Python, R, SystemDS DML (R-like DSL)

Hardware and Software:

 - Processor: AMD EPYC 7302 CPU @3.0-3.3 GHz
 - Cores: 16 physical cores (32 vCores)
 - Memory: 130GB or more
 - Disk: SSD, at least 80GB (more recommended)
 - OS: Ubuntu 20.04 LTS (experiments portable to other OS)
-----------------------------------

### Step-by-step Execution

We provide `main.sh` for fully automated reproduction of experiments. However, fully automated execution makes it harder to follow and catch errors early. We recommend to follow the step-by-step guide instead.

**Step 1:** Launch Ubunut 20.04 System.

**Step 2:** System Setup:

		    ./system_setup.sh 2>&1 | tee setup.out
		    
This script installs `jdk11`, `maven`, `git`, `python3`, `r-base`, and `texlive`. Java 11 and Maven are needed to build the source code. Python is required for data preparation and baselines. We use R to generate the plots.

**Step 3:** Setup SystemDS and Python Baselines:

		    cd libraries
		    ./buildSource.sh 2>&1 | tee buildcode.out
		    pip install -r requirements.txt
	    
1) This script first clones Apache SystemDS and checks out the commit hash with all code. SystemDS is an active repository. Code added after the paper submission might impact the experiments. We use a commit from soon after the submission that has all the necessary code changes.
2) It next builds the jar files (*SystemDS.jar* and *lib/*) and moves them to `libraraies/` to be accessible by the scripts.
3) Install required Python packages.

**Step 4:** Download and prepare the datasets:

All the datasets are publicly available. 
1) To automatically download the Kaggle datasets, please setup Kaggle [API](https://github.com/Kaggle/kaggle-api). Install kaggle via `pip`, add `~/.local/bin` to `PATH`, and update `KAGGLE_USERNAME` and `KAGGLE_KEY` fields in `.bash_profile` or `.bashrc`. Verify with `which kaggle`. An alternative is to manually download the datasets from the Kaggle website in the `datasets` folder.
2) I could not make `wget` work for the Criteo dataset. Please download the day_21.gz from [here](https://criteo.wetransfer.com/downloads/4bbea9b4a54baddea549d71271a38e2c20230428071257/d4f0d2/grid).
3) Finally, use the below script to automatically download and prepare the datasets.

		    cd datasets
		    ./prepareData.sh 2>&1 | tee prepdata.out

**Step 5:** Run Micro Benchmarks:

Execute the micro benchmarks and reproduce Figure 3 plots and move the results to the `results` folder. If not available, create the `results` folder first.

		    mkdir results
		    cd microbenchmarks
		    ./repro_fig3.sh 2>&1 | tee outMicro.log
		    mv *.dat ../results

**Step 6:** Run Feature Transformation Benchmark (FTBench):

In this paper, we define a feature transformation benchmark, **FTBench**, to foster research on feature transformations. FTBench documents 15 use cases, which are discussed in detail in the paper. We also provide two full reference implementations of the use cases and a few partial implementations of the benchmark. The below scripts reproduce Figure 4 and Table 3.
1. Scripts for all the use cases in SystemDS and UPLIFT are in `FTBench/systemds/`.

		    cd FTBench/systemds
		    ./runAll_dml.sh 2>&1 | tee outFTdml.log
		    mv *.dat ../../results

2. Scikit-learn implementation of all the use cases are in `FTBench/scikit-learn`. 

		    cd FTBench/scikit-learn
		    ./runAll_sk.sh 2>&1 | tee outFTsk.log
		    mv *.dat ../../results

3. Additionally, we used specialized systems such as sparkml, dask, and TensorFlow/Keras to implement a subset of use cases.  They are available inside respective folders.

		    cd FTBench/sparkml
		    ./runAll_spark.sh 2>&1 | tee outFTspark.log
		    mv *.dat ../../results
		    
		    cd FTBench/dask
		    ./runAll_dask.sh 2>&1 | tee outFTdask.log
		    mv *.dat ../../results
		    
		    cd FTBench/keras
		    ./runAll_keras.sh 2>&1 | tee outFTtf.log
		    mv *.dat ../../results


**Step 7:** Generate all plots. All plots are generated in the pdf format.

		    cd plots
		    ./genAllPlots.sh

**Step 8:** Visually compare original plots and reproduced plots. Table 4(e) and Table-3 are stored as text files. Use `cat` command to print those tables on the standard output.

--------------------------------------


*[1] Matthias Boehm, Iulian Antonov, Sebastian Baunsgaard, Mark Dokter, Robert Ginthör, Kevin Innerebner, Florijan Klezin, Stefanie N. Lindstaedt, Arnab Phani, Benjamin Rath, Berthold Reinwald, Shafaq Siddiqui, and Sebastian Benjamin
Wrede. 2020. SystemDS: A Declarative Machine Learning System for the End-to-End Data Science Lifecycle. In CIDR.*

