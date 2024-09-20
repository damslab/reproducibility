## Reproducibility Submission SIGMOD 2024, Paper 218

**Authors:** Shafaq Siddiqi, Roman Kern, Matthias Boehm

**Paper Name:** SAGA: A Scalable Framework for Optimizing Data Cleaning Pipelines for Machine Learning Applications

**Paper Links:**
 * <https://dl.acm.org/doi/pdf/10.1145/3617338>
 * <https://mboehm7.github.io/resources/sigmod2024a.pdf> (green open access)

**Source Code Artifacts:**
 - Repository: Apache SystemDS [1] (https://github.com/apache/systemds)
 - Programming Language: Java, Python, SystemDS DML (a R-like Domain Specific Language)
 - Additional Programming Language info: Java version 11 is required

**HW/SW Environment for Reproducibility:**
 - We ran all experiments on a 1+6 node cluster, each node having an AMD EPYC 7302 CPU at 3.0-3.3 GHz (16 physical/32 virtual cores), and 128 GB DDR4 RAM (peak performance is 768 GFLOP/s, 183.2 GB/s).
 - The software stack comprises Ubuntu 20.04.1, Apache Hadoop 3.3.1, and Apache Spark 3.2.0. SAGA uses OpenJDK 11.0.13 with 110 GB max and initial JVM heap size. However, Apache SystemDS and the experiments are fully portable to any OS.

**Quickstart Guide:**
 - Setup the environment

        ./system_setup.sh

 - Clone Apache SystemDS

        rm -rf systemds;
        git clone https://github.com/apache/systemds.git

 - Build SystemDS (few minutes)

        cd systemds;
        mvn clean package -P distribution

 - Run JUnit tests of cleaning pipelines

        mvn test -Dtest="**.functions.pipelines.**"

 - Run the individual experiments for specific tables/plots
   (see experiments and TaskParallelExperiments)

   
**Last Update:** Sep 20, 2024 (minor fixes)

