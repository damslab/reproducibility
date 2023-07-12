#!/bin/bash

# Experiment1 Micro-Benchmark Identification Part

bcmd=./explocal/exp1_micor_bench_identification/runExperiment1_Frame.sh

$bcmd aminer-author-json Experiment1a_times 
$bcmd aminer-paper-json Experiment1b_times 
$bcmd yelp-json Experiment1c_times 
$bcmd aminer-author Experiment1d_times
$bcmd aminer-paper Experiment1e_times
$bcmd yelp-csv Experiment1f_times      
$bcmd message-hl7 Experiment1g_times    
