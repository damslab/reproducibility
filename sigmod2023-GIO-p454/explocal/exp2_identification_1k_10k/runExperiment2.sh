#!/bin/bash

# Experiment1 Micro-Benchmark Identification Part

bcmd=./explocal/exp2_identification_1k_10k/runExperiment2_Frame.sh

$bcmd aminer-author-json-1k-10k Experiment2a_times
$bcmd aminer-paper-json-1k-10k Experiment2b_times
$bcmd yelp-json-1k-10k Experiment2c_times
$bcmd aminer-author-1k-10k Experiment2d_times
$bcmd aminer-paper-1k-10k Experiment2e_times
$bcmd yelp-csv-1k-10k Experiment2f_times      
$bcmd message-hl7-1k-10k Experiment2g_times     
