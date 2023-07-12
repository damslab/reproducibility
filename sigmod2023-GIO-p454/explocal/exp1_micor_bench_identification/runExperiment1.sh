#!/bin/bash

# Experiment1 Micro-Benchmark Identification Part

parallel=$1 # parallel option is not affected to the performance 
bcmd=./explocal/exp1_micor_bench_identification/runExperiment1_Frame.sh

$bcmd aminer-author-json Experiment1a_times $parallel
$bcmd aminer-paper-json Experiment1b_times $parallel
$bcmd yelp-json Experiment1c_times $parallel
$bcmd aminer-author Experiment1d_times $parallel
$bcmd aminer-paper Experiment1e_times $parallel
$bcmd yelp-csv Experiment1f_times $parallel        
$bcmd message-hl7 Experiment1g_times $parallel      
