#!/bin/bash

# Step 1: Launch an Ubuntu 20.04 system (16x2 cores, 130GB memory)
# The original experiments used 16/32 physical/virtual cores

# Step 2: System setup for Ubuntu
./system_setup.sh 2>&1 | tee setup.out

# Step 3: Clone the source code and build the jars
cd libraries
./buildSource.sh 2>&1 | tee buildcode.out
pip install -r requirements.txt
cd ..

# Cleanup results and plots
mkdir results
rm -f results/*
rm -f plots/*.pdf

# Step 4: Download and prepare all datasets
# Setup Kaggle API to download the Kaggle datasets:
# https://github.com/Kaggle/kaggle-api
# pip install kaggle
# Add ~/.local/bin to PATH
# Update KAGGLE_USERNAME and KAGGLE_KEY fields in .bash_profile or .bashrc
# check `which kaggle`
cd datasets
./prepareData.sh 2>&1 | tee prepdata.out
cd ..

# Step 5: Execute microbenchmarks (Figure 3)
cd microbenchmarks
./repro_fig3.sh 2>&1 | tee outMicro.log
mv *.dat ../results   #move results to results/
cd ..

# Step 6: Execute FTBench benchmark (Figure 4, Table 3)
# Reference implementation: SystemDS
cd FTBench/systemds
./runAll_dml.sh 2>&1 | tee outFTdml.log
mv *.dat ../../results   #move results to results/
cd ..

# Reference implementation: Scikit-learn
cd scikit-learn
./runAll_sk.sh 2>&1 | tee outFTsk.log
mv *.dat ../../results   #move results to results/
cd ..

# Reference implementation: SparkML
cd sparkml
./runAll_spark.sh 2>&1 | tee outFTspark.log
mv *.dat ../../results   #move results to results/
cd ..

# Reference implementation: Dask
cd dask
./runAll_dask.sh 2>&1 | tee outFTdask.log
mv *.dat ../../results   #move results to results/
cd ..

# Reference implementation: TensorFlow/Keras
cd keras
./runAll_keras.sh 2>&1 | tee outFTtf.log
mv *.dat ../../results   #move results to results/
cd ../..

# Step 7: Generate plots
cd plots
./genAllPlots.sh
cd ..

# Step 8: Compare original plots with reproduced plots 

