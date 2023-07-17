#!/bin/bash

# Experiment1 Micro-Benchmark Identification Part

bcmd=./explocal/exp2_identification_1k_10k/runExperiment2_Frame.sh

$bcmd aminer-author-json-1k-10k aminer-author-json Experiment2a_times
$bcmd aminer-paper-json-1k-10k aminer-paper-json Experiment2b_times
$bcmd yelp-json-1k-10k yelp-json Experiment2c_times
$bcmd aminer-author-1k-10k aminer-author Experiment2d_times
$bcmd aminer-paper-1k-10k aminer-paper Experiment2e_times
$bcmd yelp-csv-1k-10k yelp-csv Experiment2f_times      
$bcmd message-hl7-1k-10k message-hl7 Experiment2g_times     
