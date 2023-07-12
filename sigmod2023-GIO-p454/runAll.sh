#!/bin/bash

# clean original results
rm -rf results/*;
mkdir -p results;

mkdir -p setup

source load-had3.3-java11.sh

# setup, run experiments, plots
#./run1SetupDependencies.sh;
#./run2SetupBaseLines.sh;
#./run3DownloadData.sh;
./run4GenerateData.sh;
#./run5LocalExperiments.sh;
