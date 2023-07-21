#!/bin/bash

export LOG4JPROP='explocal/log4j.properties'
export CMD="java -Xms120g -Xmx120g -Dlog4j.configuration=file:$LOG4JPROP"

mkdir -p setup

source load-had3.3-java11.sh

# setup, run experiments, plots
./run1SetupDependencies.sh;
./run2SetupBaseLines.sh;
./run3DownloadData.sh;
./run4GenerateData.sh;
./run5LocalExperiments.sh;
./run6PlotResults.sh; 
