## Reproducibility Submission SIGMOD 2021, Paper 218

**Authors:** Svetlana Sagadeeva, Matthias Boehm

**Paper Name:** SliceLine: Fast, Linear-Algebra-based Slice Finding for ML Model Debugging

**Paper Links:** 
 * <https://dl.acm.org/doi/10.1145/3448016.3457323> 
 * <https://mboehm7.github.io/resources/sigmod2021b_sliceline.pdf> (green open access)

**Source Code Info:**
 * Repository: Apache SystemDS [1] (<https://github.com/apache/systemds>, commit [627825c25d5a5938a772a78ce037c57e68611998](https://github.com/apache/systemds/commit/627825c25d5a5938a772a78ce037c57e68611998))
 * Reproducibility Repository: <https://github.com/damslab/reproducibility/tree/master/sigmod2021-sliceline-p218>
 * Programming Language: Java, R, SystemDS DML
 * Packages/Libraries Needed: JDK 8, Git, Maven, R

**Datasets Used:**
 * Adult: <https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data>
 * Covtype: <https://archive.ics.uci.edu/ml/machine-learning-databases/covtype/covtype.data.gz>
 * KDD'98: <https://archive.ics.uci.edu/ml/machine-learning-databases/kddcup98-mld/epsilon_mirror/cup98lrn.zip>
 * US Census: <https://archive.ics.uci.edu/ml/machine-learning-databases/census1990-mld/USCensus1990.data.txt>
 * CriteoD21: <http://azuremlsampleexperiments.blob.core.windows.net/criteo/day_21.gz>
 * Salaries: <https://forge.scilab.org/index.php/p/rdataset/source/file/master/csv/car/Salaries.csv>

**Hardware and Software Info:** The experiments use both a scale-up, two-socket Intel server, and a scale-out cluster of 1+12 single-socket AMD servers:
 * Scale-up node: two Intel Xeon Gold 6238 CPUs@2.2-2.5 GHz (56 physical/112 virtual cores), 768GB DDR4 RAM at 2.933GHz balanced across 6 memory channels per socket, 2 x 480GB SATA SSDs (system/home), and 12 x 2TB SATA SSDs (data). 
 * Scale-out cluster: 1+12 nodes, each a single AMD EPYC 7302 CPU at 3.0-3.3 GHz (16 physical/32 virtual cores), 128GB DDR4 RAM at 2.933 GHz balanced across 8 memory channels, 2 x 480 GB SATA SDDs (system/home), 12 x 2TB SATA HDDs (data), and 2 x 10Gb Ethernet.
 * We used Ubuntu 20.04.1, OpenJDK Java 1.8.0_265 with -Xmx600g -Xms600g (on scale-up) -Xmx 100g -Xmx100g (on scale-out), Apache Hadoop 2.7.7, and Apache Spark 2.4.7.

**Setup and Experiments:** The repository is pre-populated with the paper's experimental results (`./results`), individual plots (`./plots`), and SystemDS source code. The entire experimental evaluation can be run via `./runAll.sh`, which deletes the results and plots and performs setup, dataset download and preparation, local and distributed experiments, and plotting. However, for a more controlled evaluation, we recommend running the individual steps separately:

    ./run1SetupDependencies.sh;
    ./run2SetupSystemDS.sh;
    ./run3DownloadData.sh;
    ./run4PrepareLocalData.sh; # on scale-up node
    ./run5LocalExperiments.sh; # on scale-up node 
    ./run6PrepareDistData.sh;  # on scale-out cluster
    ./run7DistExperiments.sh;  # on scale-out cluster
    ./run8PlotResults.sh;

**Last Update:** May 10, 2022 (minor fixes)

----

*[1] Matthias Boehm, Iulian Antonov, Sebastian Baunsgaard, Mark Dokter, Robert Ginthoer, Kevin Innerebner, Florijan Klezin, Stefanie N. Lindstaedt, Arnab Phani, Benjamin Rath, Berthold Reinwald, Shafaq Siddiqui, and Sebastian Benjamin Wrede: SystemDS: A Declarative Machine Learning System for the End-to-End Data Science Lifecycle, CIDR 2020*
