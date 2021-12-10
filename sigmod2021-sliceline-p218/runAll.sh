#!/bin/bash

# clean original results
rm -R results/*;
rm -R plots/*;

# setup, run experiments, plots
./run1SetupDependencies.sh;
./run2SetupSystemDS.sh;
./run3DownloadData.sh;
./run4PrepareLocalData.sh; # on scale-up node
./run5LocalExperiments.sh; # on scale-up node 
./run6PrepareDistData.sh;  # on scale-out cluster
./run7DistExperiments.sh;  # on scale-out cluster
./run8PlotResults.sh;
