#!/bin/bash

# Experiment1 Micro-Benchmark Identification Part

parallel=$1 # parallel option is not affected to the performance 
bcmd=./explocal/exp1_micor_bench_identification/runExperiment1_Frame.sh

./explocal/exp3_early/runExperiment3_MatrixCurrentCol.sh mm-col Experiment3a_times $parallel
./explocal/exp3_early/runExperiment3_MatrixEarlyCol.sh mm-col Experiment3a_times $parallel

./explocal/exp3_early/runExperiment3_MatrixCurrentRow.sh mm-row Experiment3b_times $parallel
./explocal/exp3_early/runExperiment3_MatrixEarlyRow.sh mm-row Experiment3b_times $parallel
