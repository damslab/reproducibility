#!/bin/bash

# This script takes ~4 minutes to finish

# Clone Apache SystemDS repository
rm -rf systemds #cleanup
git clone https://github.com/apache/systemds.git

# Create branch from the commit that includes all paper codes
cd systemds
git checkout -b reproducibility aa09b5c3d3b5d221426fd06871b6690e1297ee9e

# Build the source
mvn clean package -P distribution

# Move the jars outside to be accessible by the run scripts
cd ..
mv systemds/target/SystemDS.jar .
rm -rf lib
mv systemds/target/lib/ .

# Cleanup the class files to save space
cd systemds
mvn clean
cd ..

# Setup Intel-MKL
wget https://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15816/l_mkl_2019.5.281.tgz
tar -xzf l_mkl_2019.5.281.tgz
cd l_mkl_2019.5.281
sudo ./install.sh --silent ../my_silent_config.cfg   #takes a few minutes
cd ..

# Create a special build to measure memory usage (Figure 6b).
# We call gc after each instruction in this special build.
# Code changes are available in: https://github.com/phaniarnab/systemds/tree/reproducibility
# NOTE: this build is used only for experiment 6b
mkdir tmp
cd tmp
git clone https://github.com/phaniarnab/systemds.git
cd systemds
git checkout reproducibility #set remote branch reproduciblity
mvn clean package -P distribution
cd ../..
mv tmp/systemds/target/SystemDS.jar ./SystemDS_mem.jar
rm -rf tmp  #no need to keep this build

