#!/bin/bash

source parameters.sh

mkdir -p results
mkdir -p hprof

source code/util/gitIdLog.sh
logGitIDs

date +%T

# Compression experiment (Table 5)
# ./code/compression/tab5.sh

# Compression experiment Distributed (Table 6)
# Note this experiment require there to NOT be a spark cluster.... since we rely on local spark mode.
# ./code/compression/comp-spark.sh

# Figure 6 Sum and ColSum.
# ./code/UA/exp6.sh

# Figure 7 Plus and Div Row Vector
# ./code/scalar/exp7.sh

# Figure 8 Matrix Multiplication (Figure 8 a and b)
# ./code/MM/exp8ab.sh

# Figure 8 TSMM (c and d)
# ./code/UA/exp8cd.sh

# Figure 8 LMM and RMM Scaling
# ./code/MM/exp8ef.sh

# Figure 9 Scale and Shift
# ./code/UA/exp9a.sh

# Figure 9 Euclidean Distance
# ./code/MM/exp9b.sh

# Figure 10 RMM Overlap Sequence
# ./code/MM/exptab.sh

# TOPS table
# ./code/tops.sh


### ALGORITHMS RUNS:

# Table 9: Local baseline end-to-end experiments
# ./code/algorithms/exptab9.sh


## Table 10 SystemML baseline 
# ./code/algorithms/exptab10SysML.sh

# Table 10: Local CLA comparison. no scale and shift
./code/algorithms/exptab10.sh

## Before running distributed created the distributed datasets for HDFS:
##  hdfs dfs -put data/census data/
## ./data/save_scaleup_census_systemds.sh 
## ./data/save_scaleup_census_reblock_systemds.sh

# Table 11: Distributed Baseline CLA ...
# ./code/algorithms/exptab11.sh

# Figure 12: Tensorflow comparison.
# ./code/tensorflow/tensorflow.sh

# Table 12: Hybrid scaling
# ./code/algorithms/exptab12.sh

# Table 12: Grid search
# ./code/algorithms/exptab13.sh
