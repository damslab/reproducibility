#!/bin/bash


./run0LoadConfig.sh; # require for all steps

# setup, run experiments, plots
./run1SetupDependencies.sh;
./run2SetupBaseLines.sh;
./run3DownloadData.sh;
./run4GenerateData.sh;
./run5LocalExperiments.sh;
./run6PlotResults.sh; 
