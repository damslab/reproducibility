## Reproducibility Submission for Paper 32

**Paper name: LIMA: Fine-grained Lineage Tracing and Reuse in Machine Learning Systems
Paper link: https://dl.acm.org/doi/10.1145/3448016.3452788**

Source Code Info
 - Repository: Apache SystemDS [1] (https://github.com/apache/systemds)
 - Programming Language: java, DML (a R-like Domain Specific Language)
 - Additional Programming Language info: Java 8

Hardware Info to Reproduce Experiment Results

 - Processor: Intel(R) Xeon(R) Platinum 8175M CPU @ 2.50GHz or above
 - Cores: 16 physical cores (32 vCores)
 - Memory: 128GB. 110GB JVM heap is needed for the experiments
 - Disk: SSD, at least 30GB. More is better.
 - Example System: AWS instance *m5.8xlarge*

Experimentation Info

 - Environment: Ubuntu 20.04 LTS is used for the original and reproducibility experiments. We provide a system-setup script for Ubuntu. However, Apache SystemDS and the experiments are fully portable to any OS.
-----------------------------------

Execution Guide:

#### Approach 1: Fully automated 
Execute `./main.sh`. `main.sh` runs all the steps and outputs a compiled paper. Although this script is thoroughly tested, fully automated execution makes it harder to follow and catch errors early. Complete execution takes approximately 44.5 hours to complete.
   
**Step 1:** Launch an Ubuntu 20.04 system with the aforementioned configurations.   Configure sudo without password (no-password is the default for AWS instances)
   
**Step 2:** Clone the reproducibility repository and execute:

                cd reproducibility/sigmod2021-LIMA-p32
                ./main.sh &> runall.out  

Output: paper containing reproduced plots. Time to complete: ~44.5 hours
   
**Step 3:** Find the reproduced paper, sigmod2021-LIMA-p32/*rdm32_repro.pdf*  and compare with the original submission, *rdm32_org.pdf*.

#### Approach 2: Step-by-step execution
Note that the scripts are written with relative paths. It is necessary to step into the right directory to execute a script. Please follow `main.sh`.

**Step 1:** Launch an Ubuntu 20.04 system with the aforementioned configurations and clone the reproducibility repo.

**Step 2:** System setup.

                cd rdm32_SIGMOD21_repro
                ./system_setup.sh 2>&1 | tee setup.out

  This script installs jdk8, maven, git, python3, r-base, and texlive. Maven and git are needed to clone and build the source code. Java 8 and python are needed to execute the scripts. r-base and texlive generate the plots and compile the paper.

**Step 3:** Clone and build the source code

                cd libraries
                ./buildSource.sh 2>&1 | tee buildcode.out

  1) This script first clones Apache SystemDS and checks out a particular commit hash. SystemDS is an active repository. Code added after the paper submission might impact the experiments. I use a commit from soon after the submission that has all the necessary code changes.
  2) It next builds the jar files and moves them to `libraraies/` to be accessible by the scripts. Output: *SystemDS.jar* and *lib/*
  3) Figure 10(a) needs Intel MKL library. The next step is to download and compile MKL
  4) To reproduce Figure 6(b) we need code changes to run periodic garbage collector which measures exact memory overheads of lineage tracing. The code changes are available at https://github.com/phaniarnab/systemds/tree/reproducibility. The last step is to get and build this branch. Output: *SystemDS_mem.jar*. 

**Step 4:** Set path.

                export PATH=$PWD/libraries:$PATH

  To verify, try `which runjava`, `which runjava_mem` and `which config`. They should point to the corresponding scripts in `libraries/`. Script `runjava` is  just a wrapper around `java -cp` with proper jars and JVM flags (110GB heap).

**Step 5:** Download and prepare the datasets

                cd datasets
                ./prepareData.sh 2>&1 | tee prepdata.out

  This script downloads two datasets from UCI repositry (https://archive.ics.uci.edu/ml/index.php) and apply different transformations to produce multiple datasets. 
  Output: *.csv* and *.mtd* files

**Step 6:** Run micro benchmarks (reproduce Figure 6, 7, 8).

                cd microbenchmarks
                ./repro_Fig6-8.sh &> micro.out

  This script executes a few simplified ML scripts. Note that the scripts are written in DML language which is a domain specific language with R-like syntax. 
  Output: *.dat* files (raw execution time and memory usage). Time to complete: ~12.5 hours.

**Step 7:** Run end-to-end experiments (reproduce Figure 9).

                cd end2end
                ./repro_Fig9.sh &> end2end.out

  This script executes various end-to-end ML pipelines with synthetic and real datasets.
  Output: *.dat* files. Time to complete: ~15 hours.

**Step 8:** Run ML systems comparison experiments (reproduce Figure 10).

                cd MLSystems_comparison
                ./setupPythonEnv.sh 2>&1 | tee pysetup.out
                ./repro_Fig10.sh &> mlsystems.out

  1) `setupPythonEnv` script creates a virtual environment and installs TensorFlow 2.3, Scikit-learn 0.23 and Pandas.
  2) `repro_Fig10.sh` executes various DML and python scripts to compare elapsed time. Note that, TensorFlow fails with out-of-memory in 10c experiment (`exp_10c.sh`), which may lead to a different looking plot.
Output: *.dat* files. Time to complete: ~17 hours.

**Step 9:** Generate all plots
  Move all the .dat files generated by Step 6, 7 and 8 to `results/` and execute:

                cd plots
                ./genAllPlots.sh

  This script reads the results and produces the plots in pdf. R plotting tools are used to produce the plots.

**Step 10:** Recompile the paper

                cd paper
                ./genPaper.sh

  This script compiles the LaTeX files with the new plots. `Experiment.tex` file reads the plots from the `plots/` directory.
  Lastly, the paper is renamed and moved to `sigmod2021-LIMA-p32` folder

**Step 11:** Find the reproduced paper, sigmod2021-LIMA-p32/*rdm32_repro.pdf* and compare with the original submission, *rdm32_org.pdf*.

--------------------------------------

Replicability Notes:

Here I list all the parameters that may impact the experiment results. However, all of the following may not be necessary
for the Replicability testing. We believe our system is robust against all these variables.
1) **Environment:** *Portability across Operating Systems*
  Apache SystemDS is written in Java, hence platform-independent. We believe the experiment results are independent of the underlying OS. To verify, you can install the packages listed in  `system_setup` script, create a Bash setup and execute the scripts.
2) **Data Characteristics:** *Varying #rows, #cols, sparsity, datasets*
  The shell scripts inside `end2end` (figure 9) take various data characteristics such as #rows, #columns, #hypermarameters etc. as inputs. You can pass different values and see the impact on performance. Additional parameters can be changed as well by editing the .dml files. Moreover, one can try the same ML scripts on different datasets (e.g. edit `end2end/gridsearchLM_kdd.dml`).
3) **Workload Characteristics:** *Varying algorithms and workloads*
  We could only show a few ML pipelines in the paper. However, we believe all real-world exploratory ML pipelines provide reuse opportunities. You can construct pipelines in dml by using SystemDS provided built-ins and execute with and without lineage-based reuse.
4) **System Characteristics:** *Varying memory and CPU*
  The lineage cache size is set to 5% of the heap size with disk spilling enabled. 110GB heap is used for the experiments. It can be an interesting experiment to reduce the heap for the end-to-end experiments. You can change the heap size in `libraries/runjava` file (`Xmx`, `Xms`, `Xmn`). `Xmn` is usually 10% of `Xmx` and`Xms`.
5) **Maintenance:** *Robustness of the open-sourced offering*
  Apache SystemDS is an active repository. Many code and features have been added after the submission. One interesting experiment is to rerun the end-to-end experiments on the latest 2.2.1 release. Edit `buildSource.sh` to clone and build 2.2.1-rc3 tag. `git clone --branch 2.2.1-rc3 https://github.com/apache/systemds.git`. Note that, 2 builtins, `lmPredict` and `smote` have different signatures in 2.2 release. These calls are coded but commented out in the corresponding .dml files.
  
---------------------------------------------

Troubleshooting:
1) Log all the steps.
2) Grep 'Exception' to get the backtraces in the SystemDS run logs in case of failures.
3) Grep 'Killed' in the tensorflow logs to detect OOM (occurs in `exp_10c.sh`).
4) In case of path-related issues, ensure to set the paths from inside the `sigmod2021-LIMA-p32` folder and execute the scripts from inside the corresponding folders.
5) The authors are always available to help. Reach out to arnab.phani@tugraz.at / phaniarnab@gmail.com.

----

*[1] Matthias Boehm, Iulian Antonov, Sebastian Baunsgaard, Mark Dokter, Robert Ginthör, Kevin Innerebner, Florijan Klezin, Stefanie N. Lindstaedt, Arnab Phani, Benjamin Rath, Berthold Reinwald, Shafaq Siddiqui, and Sebastian Benjamin
Wrede. 2020. SystemDS: A Declarative Machine Learning System for the End-to-End Data Science Lifecycle. In CIDR.*

