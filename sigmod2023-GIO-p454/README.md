## Reproducibility Submission SIGMOD 2023, Paper 454

**Authors:** Saeed Fathollahzadeh, Matthias Boehm

**Paper Name:** GIO: Generating Efficient Matrix and Frame Readers for Custom Data Formats by Example

**Paper Link:**  <https://dl.acm.org/doi/pdf/10.1145/3589265> 

**Source Code Info:**
 * Repository: Apache SystemDS (<https://github.com/apache/systemds>, commit [82d9d130861be8e36d37a08c22cdd8d3231de6c2](https://github.com/apache/systemds/commit/82d9d130861be8e36d37a08c22cdd8d3231de6c2))
 * Reproducibility Repository: <https://github.com/damslab/reproducibility/tree/master/sigmod2023-GIO-p454>
 * Programming Language: Java, Clang++10, Python 3.8, SystemDS 
 * Packages/Libraries Needed: JDK 11, Git, Maven, Clang++, Python, LaTex

**Datasets Used:**
Dataset | URL | Download Link
---|---|---
HIGGS|https://archive.ics.uci.edu/ml/machine-learning-databases/00280/HIGGS.csv.gz| [download](https://archive.ics.uci.edu/ml/machine-learning-databases/00280/HIGGS.csv.gz)
Mnist8m| https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/multiclass/mnist8m.xz|[download](https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/multiclass/mnist8m.xz)
Susy|https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/SUSY.xz|[download](https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/SUSY.xz)
Queen|<https://suitesparse-collection-website.herokuapp.com/MM/Janna/Queen_4147.tar.gz>|[download](https://suitesparse-collection-website.herokuapp.com/MM/Janna/Queen_4147.tar.gz)
AMiner| <https://www.aminer.org/aminernetwork> |[[download paper](https://lfs.aminer.cn/lab-datasets/aminerdataset/AMiner-Paper.rar)], [[download author](https://lfs.aminer.cn/lab-datasets/aminerdataset/AMiner-Author.zip)] 
Yelp**| https://www.yelp.com/dataset/download | **required to accept the terms and conditions of the dataset license**
ReWaste F | Local Dataset | in-repository link 
HL7 | Local Dataset | in-repository link 
ADF| Local Dataset | in-repository link 

**Note:**

All datasets (except Yelp) will be downloaded automatically.

** The Yelp (yelp_dataset.tar) dataset needs to be downloaded manually and stored in the "tmodata" directory. After extracting it (you don't need to manually extract it; we will handle the extraction process automatically), we will have the following data::
* yelp_academic_dataset_review.json
* yelp_academic_dataset_business.json 
* yelp_academic_dataset_tip.json
* yelp_academic_dataset_checkin.json   
* yelp_academic_dataset_user.json 




**Hardware and Software Info:** We ran all experiments on a server node with an AMD EPYC 7302 CPU @ 3.0-3.3, GHz (16 physical/32 virtual cores) with 512KB, 8MB and 128MB L1, L2 and L3 caches, 128 GB DDR4 RAM (peak performance is 768 GFLOP/s, 183.2 GB/s), two 480 GB SATA SSDs (system/home), and twelve 2 TB SATA HDDs (data). All reader experiments utilize a single SSD. The software stack comprises Ubuntu 20.04.1, OpenJDK 11 with 120 GB max and initial JVM heap sizes for GIO, as well as Python 3.8 and clang++10 for other baseline readers.

**Setup and Experiments:** The repository is pre-populated with the paper's experimental results (`./results`), individual plots (`./plots`), and SystemDS source code. The entire experimental evaluation can be run via `./runAll.sh`, which deletes the results and plots and performs setup, dataset download, dataset preparation, dataset generating, local experiments, and plotting. However, for a more controlled evaluation, we recommend running the individual steps separately:

    ./run1SetupDependencies.sh;
    ./run2SetupBaseLines.sh;
    ./run3DownloadData.sh;
    ./run4GenerateData.sh;
    ./run5LocalExperiments.sh;
    ./run6PlotResults.sh; 

The `./run1SetupDependencies.sh` script installs all the required dependencies. Here is a brief overview of each dependency and its purpose:

* **JDK 11**: for Java-based baselines and GIO implementation
* **cmake**, **clang**, **RapidJSON**: for RapidJSON (C++ implementation) baseline
* **unzip**, **unrar**, and **xz-utils**: for decompressing datasets
* **python3.8+**: for python-based baselines
* **pdflatex**: for result visualization

The `./run2SetupBaseLines.sh` script will automatically compile Java, C++, and Python based implementations and set up the runnable apps in the `Setup` directory. There is no need for manual effort in this process.

We manage our datasets using two scripts: `./run3DownloadData.sh` and `./run4GenerateData.sh`.

* In the `./run3DownloadData.sh` script, we automatically download all datasets used in the experiments. The refined format of these datasets is then moved into the `data` directory.

* The `./run4GenerateData.sh` script is responsible for generating nested datasets and duplicating existing ones.

* Nested generated datasets: AMiner-Author (JSON), AMiner-Paper (JSON), Yelp (JSON)
* Duplicated datasets: HL7, ADF

The `./run5LocalExperiments.sh` script is responsible for running all experiments. For each experiment, we have planned to execute it five times and store the experimental results in the `results` directory.

Since we run experiments five times in the `./run6PlotResults.sh` script, we follow the following process:

* Merge the results of the five runs and compute their average. The resulting text file is saved in the `explocal/plotting/results` directory.

* Plot the averaged results using LaTeX's tikzpicture and store the plots in the `plots` directory.


**Last Update:** Jul 19, 2023 (draft version)