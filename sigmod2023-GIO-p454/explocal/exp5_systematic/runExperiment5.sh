#!/bin/bash

# Systematic Experiments

# Identification for Vary Number of Fields
##########################################
./explocal/exp5_systematic/runExperiment5a_Frame.sh aminer-author-json Experiment5aa_times $parallel
./explocal/exp5_systematic/runExperiment5a_Frame.sh aminer-paper-json Experiment5ab_times $parallel
./explocal/exp5_systematic/runExperiment5a_Frame.sh yelp-json Experiment5ac_times $parallel
./explocal/exp5_systematic/runExperiment5a_Frame.sh aminer-author Experiment5ad_times $parallel
./explocal/exp5_systematic/runExperiment5a_Frame.sh aminer-paper Experiment5ae_times $parallel
./explocal/exp5_systematic/runExperiment5a_Frame.sh yelp-csv Experiment5af_times $parallel
./explocal/exp5_systematic/runExperiment5a_Frame.sh message-hl7 Experiment5ag_times $parallel    
./explocal/exp5_systematic/runExperiment5a_Matrix.sh mnist8m-libsvm Experiment5ah_times $parallel
./explocal/exp5_systematic/runExperiment5a_Matrix.sh susy-libsvm Experiment5ai_times $parallel
./explocal/exp5_systematic/runExperiment5a_Frame.sh ReWasteF-csv Experiment5aj_times $parallel
./explocal/exp5_systematic/runExperiment5a_Matrix.sh higgs-csv Experiment5ak_times $parallel
./explocal/exp5_systematic/runExperiment5a_Matrix.sh queen-mm Experiment5al_times $parallel

# Reader for Vary Number of Fields
##################################

# GIO
./explocal/exp5_systematic/runExperiment5b_GIOFrame.sh aminer-author-json Experiment5a_times $parallel
./explocal/exp5_systematic/runExperiment5b_GIOFrame.sh aminer-paper-json Experiment5b_times $parallel
./explocal/exp5_systematic/runExperiment5b_GIOFrame.sh yelp-json Experiment5c_times $parallel
./explocal/exp5_systematic/runExperiment5b_GIOFrame.sh aminer-author Experiment5d_times $parallel
./explocal/exp5_systematic/runExperiment5b_GIOFrame.sh aminer-paper Experiment5e_times $parallel
./explocal/exp5_systematic/runExperiment5b_GIOFrame.sh yelp-csv Experiment5f_times $parallel
./explocal/exp5_systematic/runExperiment5b_GIOFrame.sh message-hl7 Experiment5g_times $parallel  
./explocal/exp5_systematic/runExperiment5b_GIOMatrix.sh mnist8m-libsvm Experiment5h_times $parallel
./explocal/exp5_systematic/runExperiment5b_GIOMatrix.sh susy-libsvm Experiment5i_times $parallel
./explocal/exp5_systematic/runExperiment5b_GIOFrame.sh ReWasteF-csv Experiment5j_times $parallel
./explocal/exp5_systematic/runExperiment5b_GIOMatrix.sh higgs-csv Experiment5k_times $parallel
./explocal/exp5_systematic/runExperiment5b_GIOMatrix.sh queen-mm Experiment5l_times $parallel

# SystemDS baseline
./explocal/exp5_systematic/runExperiment5_SystemDS.sh JACKSON aminer-author-json Experiment5a_times $parallel
./explocal/exp5_systematic/runExperiment5_SystemDS.sh JACKSON aminer-paper-json Experiment5b_times $parallel
./explocal/exp5_systematic/runExperiment5_SystemDS.sh JACKSON yelp-json Experiment5c_times $parallel

./explocal/exp5_systematic/runExperiment5_SystemDS.sh GSON aminer-author-json Experiment5a_times $parallel
./explocal/exp5_systematic/runExperiment5_SystemDS.sh GSON aminer-paper-json Experiment5b_times $parallel
./explocal/exp5_systematic/runExperiment5_SystemDS.sh GSON yelp-json Experiment5c_times $parallel

./explocal/exp5_systematic/runExperiment5_SystemDS.sh JSON4J aminer-author-json Experiment5a_times $parallel
./explocal/exp5_systematic/runExperiment5_SystemDS.sh JSON4J aminer-paper-json Experiment5b_times $parallel
./explocal/exp5_systematic/runExperiment5_SystemDS.sh JSON4J yelp-json Experiment5c_times $parallel

./explocal/exp5_systematic/runExperiment5_SystemDS.sh CSV yelp-csv Experiment5f_times $parallel
./explocal/exp5_systematic/runExperiment5_SystemDS.sh CSV ReWasteF-csv Experiment5j_times $parallel

./explocal/exp5_systematic/runExperiment5_SystemDS.sh aminer-author aminer-author Experiment5d_times $parallel
./explocal/exp5_systematic/runExperiment5_SystemDS.sh aminer-paper aminer-paper Experiment5e_times $parallel
    
./explocal/exp5_systematic/runExperiment5_SystemDS.sh LibSVM mnist8m-libsvm Experiment5h_times $parallel
./explocal/exp5_systematic/runExperiment5_SystemDS.sh LibSVM susy-libsvm Experiment5i_times $parallel
./explocal/exp5_systematic/runExperiment5_SystemDS.sh CSV higgs-csv Experiment5k_times $parallel
./explocal/exp5_systematic/runExperiment5_SystemDS.sh MM queen-mm Experiment5l_times $parallel
./explocal/exp5_systematic/runExperiment5_SystemDS.sh message-hl7 message-hl7 Experiment5g_times $parallel

# Python baseline
./explocal/exp5_systematic/runExperiment5_Python.sh setup/Python/frameCSVReader.py yelp-csv Experiment5f_times $parallel
./explocal/exp5_systematic/runExperiment5_Python.sh setup/Python/frameCSVReader.py ReWasteF-csv Experiment5j_times $parallel
./explocal/exp5_systematic/runExperiment5_Python.sh setup/Python/frameHL7Reader.py message-hl7 Experiment5g_times $parallel
./explocal/exp5_systematic/runExperiment5_Python.sh setup/Python/matrixLibSVMReader.py mnist8m-libsvm Experiment5h_times $parallel
./explocal/exp5_systematic/runExperiment5_Python.sh setup/Python/matrixLibSVMReader.py susy-libsvm Experiment5i_times $parallel
./explocal/exp5_systematic/runExperiment5_Python.sh setup/Python/matrixCSVReader.py higgs-csv Experiment5k_times $parallel
./explocal/exp5_systematic/runExperiment5_Python.sh setup/Python/matrixMMReader.py queen-mm Experiment5l_times $parallel

# RapidJSON baseline
./explocal/exp5_systematic/runExperiment5_RapidJSON.sh aminer-author-json aminer-author-json Experiment5a_times $parallel
./explocal/exp5_systematic/runExperiment5_RapidJSONPaper.sh aminer-paper-json aminer-paper-json Experiment5b_times $parallel
./explocal/exp5_systematic/runExperiment5_RapidJSON.sh yelp-json yelp-json Experiment5c_times $parallel
