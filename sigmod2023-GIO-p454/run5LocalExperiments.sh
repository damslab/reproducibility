#!/bin/bash

# This script runs all local experiments on the specified scale-up machine.

# clean original results
rm -rf results/*;
mkdir -p results;

for rp in {1..5}; do  
    ./explocal/exp1_micor_bench_identification/runExperiment1.sh # EXP1: Figure 8 (diagrams a-g)
    ./explocal/exp2_identification_1k_10k/runExperiment2.sh # EXP2: Table 3 (1k to 10k rows)
    ./explocal/exp3_early/runExperiment3.sh # EXP3: Figure 9 (diagrams a-b)

    ./explocal/exp4_micro_bench/runExperiment4.sh true # EXP4 (multi-threaded): Figure 10 (diagrams a-g)
    ./explocal/exp4_micro_bench/runExperiment4.sh false # EXP4 (single-threaded): Figure 10 (diagrams a-g)

    ./explocal/exp5_systematic/runExperiment5.sh true # EXP5 (multi-threaded): Figure 11 (diagrams a-l)

    ./explocal/exp6_end_to_end/runExperiment6.sh true # EXP6 (multi-threaded): End-to-End Reader (diagrams a-b)
    ./explocal/exp6_end_to_end/runExperiment6.sh false # EXP6 (single-threaded): End-to-End Reader (diagrams a-b)
done