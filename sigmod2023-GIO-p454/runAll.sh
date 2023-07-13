#!/bin/bash

export LOG4JPROP='explocal/log4j.properties'
export CMD="java -Xms12g -Xmx12g -Dlog4j.configuration=file:$LOG4JPROP"

# clean original results
rm -rf results/*;
mkdir -p results;

mkdir -p setup

source load-had3.3-java11.sh

# setup, run experiments, plots
#./run1SetupDependencies.sh;
#./run2SetupBaseLines.sh;
#./run3DownloadData.sh;
#./run4GenerateData.sh;
#./run5LocalExperiments.sh;

./run6PlotResults.sh
