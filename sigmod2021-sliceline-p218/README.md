## Reproducibility Submission SIGMOD 2021, Paper 218

**Authors:** Svetlana Sagadeeva, Matthias Boehm

**Paper Name:** SliceLine: Fast, Linear-Algebra-based Slice Finding for ML Model Debugging

**Paper Links:** 
 - <https://dl.acm.org/doi/10.1145/3448016.3457323> 
 - <https://mboehm7.github.io/resources/sigmod2021b_sliceline.pdf> (green open access)

**Source Code Info:**
 - Repository: Apache SystemDS [1] (<https://github.com/apache/systemds>)
 - Programming Language: Java, R, SystemDS DML
 - Packages/Libraries Needed: JDK 8, Git, Maven, R

**Datasets Used:**
 * Adult: <https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data>
 * Covtype: <https://archive.ics.uci.edu/ml/machine-learning-databases/covtype/covtype.data.gz>
 * KDD'98: <https://archive.ics.uci.edu/ml/machine-learning-databases/kddcup98-mld/epsilon_mirror/cup98lrn.zip>
 * US Census: <https://archive.ics.uci.edu/ml/machine-learning-databases/census1990-mld/USCensus1990.data.txt>
 * CriteoD21: <http://azuremlsampleexperiments.blob.core.windows.net/criteo/day_21.gz>
 * Salaries: <https://forge.scilab.org/index.php/p/rdataset/source/file/master/csv/car/Salaries.csv>

**Setup and Experiments:** The repository is pre-populated with the paper's experimental results (`./results`) and individual plots (`./plots`). The entire experimental evaluation can be run via `./runAll.sh`, which deletes the results and plots and performs setup, dataset download and preparation, local and distributed experiments, and plotting. However, for a more controlled evaluation, we recommend running the individual steps separately:

    ./run1SetupDependencies.sh;
    ./run2SetupSystemDS.sh;
    ./run3DownloadData.sh;
    ./run4PrepareLocalData.sh; # on scale-up node
    ./run5LocalExperiments.sh; # on scale-up node 
    ./run6PrepareDistData.sh;  # on scale-out cluster
    ./run7DistExperiments.sh;  # on scale-out cluster
    ./run8PlotResults.sh;

**Last Update:** Dec 10, 2021 (initial commit)

----

*[1] Matthias Boehm, Iulian Antonov, Sebastian Baunsgaard, Mark Dokter, Robert Ginthör, Kevin Innerebner, Florijan Klezin, Stefanie N. Lindstaedt, Arnab Phani, Benjamin Rath, Berthold Reinwald, Shafaq Siddiqui, and Sebastian Benjamin Wrede: SystemDS: A Declarative Machine Learning System for the End-to-End Data Science Lifecycle, CIDR 2020*
