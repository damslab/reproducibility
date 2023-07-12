#!/bin/bash

# This script runs all local experiments on the specified scale-up machine.
export LOG4JPROP='explocal/log4j.properties'
export CMD="java -Xms12g -Xmx12g -Dlog4j.configuration=file:$LOG4JPROP"


for parallel in false; do   

    for rp in {1..1}; do

        #./explocal/exp1_micor_bench_identification/runExperiment1.sh $parallel # EXP1: Figure 8 (diagrams a-g)

        ./explocal/exp3_early/runExperiment3.sh $parallel # EXP3: Figure 9 (diagrams a-b)

        # ## <<<  Experiment1 Micro-Benchmark Identification Part >>>
        # #########################################################
        
        # # <<<  Experiment1 Micro-Benchmark Identification Part Indexing >>>
        # ##########################################
        # ./explocal/runExperiment1_FrameIndex.sh aminer-author-json Experiment0a_times $parallel
        # ./explocal/runExperiment1_FrameIndex.sh aminer-paper-json Experiment0b_times $parallel
        # ./explocal/runExperiment1_FrameIndex.sh yelp-json Experiment0c_times $parallel
        # ./explocal/runExperiment1_FrameIndex.sh aminer-author Experiment0d_times $parallel
        # ./explocal/runExperiment1_FrameIndex.sh aminer-paper Experiment0e_times $parallel
        # ./explocal/runExperiment1_FrameIndex.sh yelp-csv Experiment0f_times $parallel        
        # ./explocal/runExperiment1_FrameIndex.sh message-hl7 Experiment0g_times $parallel

        # # <<<  Experiment1 Micro-Benchmark Identification Part Mapping and Indexing >>>
        # ##########################################
        # ./explocal/runExperiment1_Frame.sh aminer-author-json Experiment1a_times $parallel
        # ./explocal/runExperiment1_Frame.sh aminer-paper-json Experiment1b_times $parallel
        # ./explocal/runExperiment1_Frame.sh yelp-json Experiment1c_times $parallel
        # ./explocal/runExperiment1_Frame.sh aminer-author Experiment1d_times $parallel
        # ./explocal/runExperiment1_Frame.sh aminer-paper Experiment1e_times $parallel
        # ./explocal/runExperiment1_Frame.sh yelp-csv Experiment1f_times $parallel        
        # ./explocal/runExperiment1_Frame.sh message-hl7 Experiment1g_times $parallel
        
        # # <<<  Experiment2 Micro-Benchmark Part >>>
        # ##########################################
        # # GIO
        # ./explocal/runExperiment2_GIOFrame.sh aminer-author-json Experiment2a_times $parallel
        # ./explocal/runExperiment2_GIOFrame.sh aminer-paper-json Experiment2b_times $parallel
        # ./explocal/runExperiment2_GIOFrame.sh yelp-json Experiment2c_times $parallel
        # ./explocal/runExperiment2_GIOFrame.sh aminer-author Experiment2d_times $parallel
        # ./explocal/runExperiment2_GIOFrame.sh aminer-paper Experiment2e_times $parallel
        # ./explocal/runExperiment2_GIOFrame.sh yelp-csv Experiment2f_times $parallel        
        # ./explocal/runExperiment2_GIOFrame.sh message-hl7 Experiment2g_times $parallel
        
        # # SystemDS baseline
        # ./explocal/runExperiment2_SystemDS.sh JACKSON aminer-author-json Experiment2a_times $parallel
        # ./explocal/runExperiment2_SystemDS.sh JACKSON aminer-paper-json Experiment2b_times $parallel
        # ./explocal/runExperiment2_SystemDS.sh JACKSON yelp-json Experiment2c_times $parallel

        # ./explocal/runExperiment2_SystemDS.sh GSON aminer-author-json Experiment2a_times $parallel
        # ./explocal/runExperiment2_SystemDS.sh GSON aminer-paper-json Experiment2b_times $parallel
        # ./explocal/runExperiment2_SystemDS.sh GSON yelp-json Experiment2c_times $parallel $parallel
        
        # ./explocal/runExperiment2_SystemDS.sh JSON4J aminer-author-json Experiment2a_times $parallel
        # ./explocal/runExperiment2_SystemDS.sh JSON4J aminer-paper-json Experiment2b_times $parallel
        # ./explocal/runExperiment2_SystemDS.sh JSON4J yelp-json Experiment2c_times $parallel
                
        # ./explocal/runExperiment2_SystemDS.sh aminer-author aminer-author Experiment2d_times $parallel
        # ./explocal/runExperiment2_SystemDS.sh aminer-paper aminer-paper Experiment2e_times $parallel
        # ./explocal/runExperiment2_SystemDS.sh CSV yelp-csv Experiment2f_times $parallel
        # ./explocal/runExperiment2_SystemDS.sh message-hl7 message-hl7 Experiment2g_times $parallel

        # # Python baseline
        # ./explocal/runExperiment2_Python.sh setup/Python/frameCSVReader.py yelp-csv Experiment2f_times $parallel
        # ./explocal/runExperiment2_Python.sh setup/Python/frameHL7Reader.py message-hl7 Experiment2g_times $parallel
        
        # # RapidJSON baseline
        # ./explocal/runExperiment2_RapidJSON.sh aminer-author-json aminer-author-json Experiment2a_times $parallel
        # ./explocal/runExperiment2_RapidJSON.sh aminer-paper-json aminer-paper-json Experiment2b_times $parallel
        # ./explocal/runExperiment2_RapidJSON.sh yelp-json yelp-json Experiment2c_times $parallel


        # # <<<  Experiment3 Identification for Vary Number of Fields>>>
        # ###############################################################
        # ./explocal/runExperiment3_Frame.sh aminer-author-json Experiment3a_times $parallel
        # ./explocal/runExperiment3_Frame.sh aminer-paper-json Experiment3b_times $parallel
        # ./explocal/runExperiment3_Frame.sh yelp-json Experiment3c_times $parallel
        # ./explocal/runExperiment3_Frame.sh aminer-author Experiment3d_times $parallel
        # ./explocal/runExperiment3_Frame.sh aminer-paper Experiment3e_times $parallel
        # ./explocal/runExperiment3_Frame.sh yelp-csv Experiment3f_times $parallel
        # ./explocal/runExperiment3_Frame.sh message-hl7 Experiment3g_times $parallel    
        # ./explocal/runExperiment3_Matrix.sh mnist8m-libsvm Experiment3h_times $parallel
        # ./explocal/runExperiment3_Matrix.sh susy-libsvm Experiment3i_times $parallel
        # ./explocal/runExperiment3_Frame.sh ReWasteF-csv Experiment3j_times $parallel
        # ./explocal/runExperiment3_Matrix.sh higgs-csv Experiment3k_times $parallel
        # ./explocal/runExperiment3_Matrix.sh queen-mm Experiment3l_times $parallel
        
        # #<<<  Experiment4 Reader for Vary Number of Fields >>>
        # #########################################################
        # # GIO
        # ./explocal/runExperiment4_GIOFrame.sh aminer-author-json Experiment4a_times $parallel
        # ./explocal/runExperiment4_GIOFrame.sh aminer-paper-json Experiment4b_times $parallel
        # ./explocal/runExperiment4_GIOFrame.sh yelp-json Experiment4c_times $parallel
        # ./explocal/runExperiment4_GIOFrame.sh aminer-author Experiment4d_times $parallel
        # ./explocal/runExperiment4_GIOFrame.sh aminer-paper Experiment4e_times $parallel
        # ./explocal/runExperiment4_GIOFrame.sh yelp-csv Experiment4f_times $parallel
        # ./explocal/runExperiment4_GIOFrame.sh message-hl7 Experiment4g_times $parallel  
        # ./explocal/runExperiment4_GIOMatrix.sh mnist8m-libsvm Experiment4h_times $parallel
        # ./explocal/runExperiment4_GIOMatrix.sh susy-libsvm Experiment4i_times $parallel
        # ./explocal/runExperiment4_GIOFrame.sh ReWasteF-csv Experiment4j_times $parallel
        # ./explocal/runExperiment4_GIOMatrix.sh higgs-csv Experiment4k_times $parallel
        # ./explocal/runExperiment4_GIOMatrix.sh queen-mm Experiment4l_times $parallel

        # # SystemDS baseline
        # ./explocal/runExperiment4_SystemDS.sh JACKSON aminer-author-json Experiment4a_times $parallel
        # ./explocal/runExperiment4_SystemDS.sh JACKSON aminer-paper-json Experiment4b_times $parallel
        # ./explocal/runExperiment4_SystemDS.sh JACKSON yelp-json Experiment4c_times $parallel
        
        # ./explocal/runExperiment4_SystemDS.sh GSON aminer-author-json Experiment4a_times $parallel
        # ./explocal/runExperiment4_SystemDS.sh GSON aminer-paper-json Experiment4b_times $parallel
        # ./explocal/runExperiment4_SystemDS.sh GSON yelp-json Experiment4c_times $parallel
        
        # ./explocal/runExperiment4_SystemDS.sh JSON4J aminer-author-json Experiment4a_times $parallel
        # ./explocal/runExperiment4_SystemDS.sh JSON4J aminer-paper-json Experiment4b_times $parallel
        # ./explocal/runExperiment4_SystemDS.sh JSON4J yelp-json Experiment4c_times $parallel
        
        # ./explocal/runExperiment4_SystemDS.sh CSV yelp-csv Experiment4f_times $parallel
        # ./explocal/runExperiment4_SystemDS.sh CSV ReWasteF-csv Experiment4j_times $parallel
        
        # ./explocal/runExperiment4_SystemDS.sh aminer-author aminer-author Experiment4d_times $parallel
        # ./explocal/runExperiment4_SystemDS.sh aminer-paper aminer-paper Experiment4e_times $parallel
            
        # ./explocal/runExperiment4_SystemDS.sh LibSVM mnist8m-libsvm Experiment4h_times $parallel
        # ./explocal/runExperiment4_SystemDS.sh LibSVM susy-libsvm Experiment4i_times $parallel
        # ./explocal/runExperiment4_SystemDS.sh CSV higgs-csv Experiment4k_times $parallel
        # ./explocal/runExperiment4_SystemDS.sh MM queen-mm Experiment4l_times $parallel
        # ./explocal/runExperiment4_SystemDS.sh message-hl7 message-hl7 Experiment4g_times $parallel

        # # Python baseline
        # ./explocal/runExperiment4_Python.sh setup/Python/frameCSVReader.py yelp-csv Experiment4f_times $parallel
        # ./explocal/runExperiment4_Python.sh setup/Python/frameCSVReader.py ReWasteF-csv Experiment4j_times $parallel
        # ./explocal/runExperiment4_Python.sh setup/Python/frameHL7Reader.py message-hl7 Experiment4g_times $parallel
        # ./explocal/runExperiment4_Python.sh setup/Python/matrixLibSVMReader.py mnist8m-libsvm Experiment4h_times $parallel
        # ./explocal/runExperiment4_Python.sh setup/Python/matrixLibSVMReader.py susy-libsvm Experiment4i_times $parallel
        # ./explocal/runExperiment4_Python.sh setup/Python/matrixCSVReader.py higgs-csv Experiment4k_times $parallel
        # ./explocal/runExperiment4_Python.sh setup/Python/matrixMMReader.py queen-mm Experiment4l_times $parallel
        
        # # RapidJSON baseline
        # ./explocal/runExperiment4_RapidJSON.sh aminer-author-json aminer-author-json Experiment4a_times $parallel
        # ./explocal/runExperiment4_RapidJSONPaper.sh aminer-paper-json aminer-paper-json Experiment4b_times $parallel
        # ./explocal/runExperiment4_RapidJSON.sh yelp-json yelp-json Experiment4c_times $parallel

        # # <<<  Experiment5 Identification for End-to-End Reader>>>
        # ##########################################################    
        # ./explocal/runExperiment5_GIOIdentification.sh aminer-author Experiment5a_times $parallel
        # ./explocal/runExperiment5_GIOIdentification.sh aminer-paper Experiment5a_times $parallel
        # ./explocal/runExperiment5_GIOIdentification.sh message-hl7 Experiment5a_times $parallel
        # ./explocal/runExperiment5_GIOIdentification.sh autolead-xml Experiment5a_times $parallel
        
        # # <<<  Experiment5 End-to-End Reader >>>
        # ########################################   
        # # GIO
        # ./explocal/runExperiment5_GIOFrame.sh aminer-author Experiment5b_times $parallel
        # ./explocal/runExperiment5_GIOFrame.sh aminer-paper Experiment5b_times $parallel
        # ./explocal/runExperiment5_GIOFrame.sh message-hl7 Experiment5b_times $parallel
        # ./explocal/runExperiment5_GIOFrame.sh autolead-xml Experiment5b_times $parallel

        # # SystemDS baseline
        # ./explocal/runExperiment5_SystemDS.sh aminer-author Experiment5b_times $parallel
        # ./explocal/runExperiment5_SystemDS.sh aminer-paper Experiment5b_times $parallel
        # ./explocal/runExperiment5_SystemDS.sh message-hl7 Experiment5b_times $parallel
        # ./explocal/runExperiment5_SystemDS.sh autolead-xml Experiment5b_times $parallel

        # # Python baseline
        # ./explocal/runExperiment5_Python.sh message-hl7 Experiment5b_times $parallel  


        # ./explocal/runExperiment1_MatrixCurrent.sh mm-col Experiment6a_times $parallel
        # ./explocal/runExperiment1_MatrixEarly.sh mm-col Experiment6a_times $parallel

        # ./explocal/runExperiment3_Matrix.sh mm-row Experiment6b_times $parallel
        # ./explocal/runExperiment3_MatrixEarly.sh mm-row Experiment6b_times $parallel
        

    done  
done