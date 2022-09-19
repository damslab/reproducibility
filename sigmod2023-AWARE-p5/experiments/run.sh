#!/bin/bash

source parameters.sh

mkdir -p results
mkdir -p hprof

source code/util/gitIdLog.sh
logGitIDs

date +%T

# Compression experiment (Table 5)
# ./code/compression/comp.sh

# Compression experiment Distributed (Table 6)
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
./code/MM/exptab.sh
