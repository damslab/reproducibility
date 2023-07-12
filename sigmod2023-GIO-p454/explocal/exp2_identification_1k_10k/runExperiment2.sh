#!/bin/bash

# Experiment1 Micro-Benchmark Identification Part

parallel=$1 # parallel option is not affected to the performance 
bcmd=./explocal/exp2_identification_1k_10k/runExperiment2_Frame.sh

$bcmd aminer-author-json-1k-10k Experiment2a_times $parallel
$bcmd aminer-paper-json-1k-10k Experiment2b_times $parallel
$bcmd yelp-json-1k-10k Experiment2c_times $parallel
$bcmd aminer-author-1k-10k Experiment2d_times $parallel
$bcmd aminer-paper-1k-10k Experiment2e_times $parallel
$bcmd yelp-csv-1k-10k Experiment2f_times $parallel        
$bcmd message-hl7-1k-10k Experiment2g_times $parallel      
