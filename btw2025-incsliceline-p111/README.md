## Reproducibility Submission BTW 2025, Paper 111

**Authors:** Frederic Caspar Zoepffel, Christina Dionysio, and Matthias Boehm

**Paper Name:** Incremental SliceLine for Iterative ML Model Debugging under Updates

**Paper Links:**
 * <https://mboehm7.github.io/resources/btw2025a.pdf> (green open access)

**Source Code Info:**
 * Repository: Apache SystemDS [1] (<https://github.com/apache/systemds>, commit [a41027f7aa256ee2ea8609f819cded19896bc9f4](https://github.com/apache/systemds/commit/a41027f7aa256ee2ea8609f819cded19896bc9f4))
 * Reproducibility Repository: <https://github.com/damslab/reproducibility/tree/master/btw2025-incsliceline-p111>
 * Programming Language: Java, R, SystemDS DML
 * Packages/Libraries Needed: JDK 11, Git, Maven, R

**Datasets Used:**
 * Adult: <https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data>
 * Covtype: <https://archive.ics.uci.edu/ml/machine-learning-databases/covtype/covtype.data.gz>
 * KDD'98: <https://archive.ics.uci.edu/ml/machine-learning-databases/kddcup98-mld/epsilon_mirror/cup98lrn.zip>
 * US Census: <https://tubcloud.tu-berlin.de/s/yWafF6pnZ6Ywdok/download/USCensus.csv>

**Hardware and Software Info:** The experiments use a single scale-out server node:
 * Scale-out node: single AMD EPYC 7443P CPU at 2.8-4.0 GHz (24 physical/48 virtual cores), 256GB DDR4 RAM at 3.2 GHz balanced across 8 memory channels, 2 x 480 GB SATA SSDs (system), 8 x 2TB SATA HDDs (data).
 * The software stack comprises Ubuntu 20.04.6, Apache Hadoop 3.3, Apache Spark 3.5, OpenJDK 11 (with -Xmx200g -Xms200g), and Apache SystemDS from the main branch (as of Jan 03, 2025).

**Setup and Experiments:** The repository is pre-populated with the paper's experimental results (`./results`), individual plots (`./plots`), and SystemDS source code. The entire experimental evaluation can be run via `./runAll.sh`, which deletes the results and plots and performs setup, dataset download and preparation, local experiments, and plotting. However, for a more controlled evaluation, we recommend running the individual steps separately (e.g., via `nohup ./run5Experiments.sh &` which takes approximately 20h):

    ./run1SetupDependencies.sh;
    ./run2SetupSystemDS.sh;
    ./run3DownloadData.sh;
    ./run4PrepareLocalData.sh;
    ./run5Experiments.sh;      # timed measurements
    ./run6PlotResults.sh;

**Last Update:** Jan 13, 2025 (initial setup)

----

*[1] Matthias Boehm, Iulian Antonov, Sebastian Baunsgaard, Mark Dokter, Robert Ginthoer, Kevin Innerebner, Florijan Klezin, Stefanie N. Lindstaedt, Arnab Phani, Benjamin Rath, Berthold Reinwald, Shafaq Siddiqui, and Sebastian Benjamin Wrede: SystemDS: A Declarative Machine Learning System for the End-to-End Data Science Lifecycle, CIDR 2020*
