#!/bin/bash

# End-to-End Experiments
parallel=$1

# Identification for End-to-End Reader
######################################
./explocal/exp6_end_to_end/runExperiment6_GIOIdentification.sh aminer-author Experiment6a_times $parallel
./explocal/exp6_end_to_end/runExperiment6_GIOIdentification.sh aminer-paper Experiment6a_times $parallel
./explocal/exp6_end_to_end/runExperiment6_GIOIdentification.sh message-hl7 Experiment6a_times $parallel
./explocal/exp6_end_to_end/runExperiment6_GIOIdentification.sh autolead-xml Experiment6a_times $parallel

# End-to-End Reader
###################
# GIO
./explocal/exp6_end_to_end/runExperiment6_GIOFrame.sh aminer-author Experiment6b_times $parallel
./explocal/exp6_end_to_end/runExperiment6_GIOFrame.sh aminer-paper Experiment6b_times $parallel
./explocal/exp6_end_to_end/runExperiment6_GIOFrame.sh message-hl7 Experiment6b_times $parallel
./explocal/exp6_end_to_end/runExperiment6_GIOFrame.sh autolead-xml Experiment6b_times $parallel

# SystemDS baseline
./explocal/exp6_end_to_end/runExperiment6_SystemDS.sh aminer-author Experiment6b_times SystemDS $parallel
./explocal/exp6_end_to_end/runExperiment6_SystemDS.sh aminer-paper Experiment6b_times SystemDS $parallel
./explocal/exp6_end_to_end/runExperiment6_SystemDS.sh message-hl7 Experiment6b_times SystemDS+HAPI-HL7 $parallel
./explocal/exp6_end_to_end/runExperiment6_SystemDS.sh autolead-xml Experiment6b_times SystemDS+Jackson $parallel

# Python baseline
./explocal/exp6_end_to_end/runExperiment6_Python.sh message-hl7 Experiment6b_times $parallel  
