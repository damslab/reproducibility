## Reproducibility Submission SIGMOD 2023, Paper 454

**Authors:** Saeed Fathollahzadeh, Matthias Boehm

**Paper Name:** GIO: Generating Efficient Matrix and Frame Readers for Custom Data Formats by Example

**Paper Link:** 
 * <https://dl.acm.org/doi/pdf/10.1145/3589265> 

**Source Code Info:**
 * Repository: Apache SystemDS (<https://github.com/apache/systemds>)
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
Yelp| https://www.yelp.com/dataset/download | required to accept the terms and conditions of the dataset license
ReWaste F | Local Dataset | in-repository link 

**Hardware and Software Info:** We ran all experiments on a server node with an AMD EPYC 7302 CPU @ 3.0-3.3, GHz (16 physical/32 virtual cores) with 512KB, 8MB and 128MB L1, L2 and L3 caches, 128 GB DDR4 RAM (peak performance is 768 GFLOP/s, 183.2 GB/s), two 480 GB SATA SSDs (system/home), and twelve 2 TB SATA HDDs (data). All reader experiments utilize a single SSD. The software stack comprises Ubuntu 20.04.1, OpenJDK 11 with 120 GB max and initial JVM heap sizes for GIO, as well as Python 3.8 and clang++10 for other baseline readers.

**Setup and Experiments:** The repository is pre-populated with the paper's experimental results (`./results`), individual plots (`./plots`), and SystemDS source code. The entire experimental evaluation can be run via `./runAll.sh`, which deletes the results and plots and performs setup, dataset download, dataset preparation, dataset generating, local experiments, and plotting. However, for a more controlled evaluation, we recommend running the individual steps separately:

    ./run1SetupDependencies.sh;
    ./run2SetupBaseLines.sh;
    ./run3DownloadData.sh;
    ./run4GenerateData.sh;
    ./run5LocalExperiments.sh;
    ./run6PlotResults.sh 


**Last Update:** Jul 19, 2023 (draft version)