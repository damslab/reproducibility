#!/bin/bash
# This script takes ~45 hours to complete

# Step 1: Launch an Ubuntu 20.04 system (16x2 cores, 128GB memory)

# Step 2: System setup for Ubuntu
./system_setup.sh 2>&1 | tee setup.out

# Step 3: Clone the source code and build the jars
cd libraries
./buildSource.sh 2>&1 | tee buildcode.out
cd ..

# NOTE: Below scripts assume the JVM size as 110GB
# Edit libraries/runjava file to change JVM size

# Cleanup results and plots
rm -f results/*
rm -f plots/*.pdf

# Step 4: Set path for the run-scripts (try `which runjava` to verify)
export PATH=$PWD/libraries:$PATH

# Step 5: Download and prepare all datasets
cd datasets
./prepareData.sh 2>&1 | tee prepdata.out
cd ..

# Step 6: Execute microbenchmarks (Figure 6 to 8)
cd microbenchmarks
./repro_Fig6-8.sh &> micro.out
mv *.dat ../results   #move results to results/
cd ..

# Step 7: Execute end-to-end experiments (Figure 9)
cd end2end
./repro_Fig9.sh &> end2end.out 
mv *.dat ../results   #move results to results/
cd ..

# Step 8: Execute ML systems (TF, sk-learn) comparision experiments (Figure 10)
cd MLSystems_comparison
./setupPythonEnv.sh  #create virtual environment, install TF, sklearn
./repro_Fig10.sh &> mlsystems.out 
mv *.dat ../results   #move results to results/
cd ..

# Step 9: Generate plots
cd plots
./genAllPlots.sh
cd ..

# Step 10: Recompile the new paper and move here.
cd paper
./genPaper.sh
cd ..

# Step 11: Compare original paper (rdm32_org.pdf) with recompiled paper (rdm32_repro.pdf) 

