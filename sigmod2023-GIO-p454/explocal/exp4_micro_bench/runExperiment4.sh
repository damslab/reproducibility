#!/bin/bash

# Experiment4 Micro-Benchmark Part (Query Processing)
parallel=$1 # parallel option is not affected to the performance 

# GIO
./explocal/exp4_micro_bench/runExperiment4_GIO.sh aminer-author-json Experiment4a_times $parallel
./explocal/exp4_micro_bench/runExperiment4_GIO.sh aminer-paper-json Experiment4b_times $parallel
./explocal/exp4_micro_bench/runExperiment4_GIO.sh yelp-json Experiment4c_times $parallel
./explocal/exp4_micro_bench/runExperiment4_GIO.sh aminer-author Experiment4d_times $parallel
./explocal/exp4_micro_bench/runExperiment4_GIO.sh aminer-paper Experiment4e_times $parallel
./explocal/exp4_micro_bench/runExperiment4_GIO.sh yelp-csv Experiment4f_times $parallel
./explocal/exp4_micro_bench/runExperiment4_GIO.sh message-hl7 Experiment4g_times $parallel

# SystemDS baseline
./explocal/exp4_micro_bench/runExperiment4_SystemDS.sh JACKSON aminer-author-json Experiment4a_times $parallel
./explocal/exp4_micro_bench/runExperiment4_SystemDS.sh JACKSON aminer-paper-json Experiment4b_times $parallel
./explocal/exp4_micro_bench/runExperiment4_SystemDS.sh JACKSON yelp-json Experiment4c_times $parallel

./explocal/exp4_micro_bench/runExperiment4_SystemDS.sh GSON aminer-author-json Experiment4a_times $parallel
./explocal/exp4_micro_bench/runExperiment4_SystemDS.sh GSON aminer-paper-json Experiment4b_times $parallel
./explocal/exp4_micro_bench/runExperiment4_SystemDS.sh GSON yelp-json Experiment4c_times $parallel $parallel

./explocal/exp4_micro_bench/runExperiment4_SystemDS.sh JSON4J aminer-author-json Experiment4a_times $parallel
./explocal/exp4_micro_bench/runExperiment4_SystemDS.sh JSON4J aminer-paper-json Experiment4b_times $parallel
./explocal/exp4_micro_bench/runExperiment4_SystemDS.sh JSON4J yelp-json Experiment4c_times $parallel

./explocal/exp4_micro_bench/runExperiment4_SystemDS.sh aminer-author aminer-author Experiment4d_times $parallel
./explocal/exp4_micro_bench/runExperiment4_SystemDS.sh aminer-paper aminer-paper Experiment4e_times $parallel
./explocal/exp4_micro_bench/runExperiment4_SystemDS.sh CSV yelp-csv Experiment4f_times $parallel
./explocal/exp4_micro_bench/runExperiment4_SystemDS.sh message-hl7 message-hl7 Experiment4g_times $parallel

# Python baseline
./explocal/exp4_micro_bench/runExperiment4_Python.sh setup/Python/frameCSVReader.py yelp-csv Experiment4f_times $parallel
./explocal/exp4_micro_bench/runExperiment4_Python.sh setup/Python/frameHL7Reader.py message-hl7 Experiment4g_times $parallel

# RapidJSON baseline
./explocal/exp4_micro_bench/runExperiment4_RapidJSON.sh aminer-author-json aminer-author-json Experiment4a_times $parallel
./explocal/exp4_micro_bench/runExperiment4_RapidJSON.sh aminer-paper-json aminer-paper-json Experiment4b_times $parallel
./explocal/exp4_micro_bench/runExperiment4_RapidJSON.sh yelp-json yelp-json Experiment4c_times $parallel