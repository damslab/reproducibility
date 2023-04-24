#!/bin/bash

source parameters.sh 

export SYSDS_DISTRIBUTED=1

systemds code/dataPrep/save_reblock.dml -config code/conf/ulab16.xml -args "census/train_census_enc"
systemds code/dataPrep/save_reblock.dml -config code/conf/ulab16.xml -args "census/train_census_enc_2x"    
systemds code/dataPrep/save_reblock.dml -config code/conf/ulab16.xml -args "census/train_census_enc_4x"    
systemds code/dataPrep/save_reblock.dml -config code/conf/ulab16.xml -args "census/train_census_enc_8x"    
systemds code/dataPrep/save_reblock.dml -config code/conf/ulab16.xml -args "census/train_census_enc_16x"   
systemds code/dataPrep/save_reblock.dml -config code/conf/ulab16.xml -args "census/train_census_enc_32x"   
systemds code/dataPrep/save_reblock.dml -config code/conf/ulab16.xml -args "census/train_census_enc_64x"   
systemds code/dataPrep/save_reblock.dml -config code/conf/ulab16.xml -args "census/train_census_enc_128x"  
systemds code/dataPrep/save_reblock.dml -config code/conf/ulab16.xml -args "census/train_census_enc_256x"  



# systemds code/dataPrep/save_reblock_32.dml -config code/conf/ulab32.xml -args "census/train_census_enc"
# systemds code/dataPrep/save_reblock_32.dml -config code/conf/ulab32.xml -args "census/train_census_enc_2x"    
# systemds code/dataPrep/save_reblock_32.dml -config code/conf/ulab32.xml -args "census/train_census_enc_4x"    
# systemds code/dataPrep/save_reblock_32.dml -config code/conf/ulab32.xml -args "census/train_census_enc_8x"    
# systemds code/dataPrep/save_reblock_32.dml -config code/conf/ulab32.xml -args "census/train_census_enc_16x"   
# systemds code/dataPrep/save_reblock_32.dml -config code/conf/ulab32.xml -args "census/train_census_enc_32x"   
# systemds code/dataPrep/save_reblock_32.dml -config code/conf/ulab32.xml -args "census/train_census_enc_64x"   
# systemds code/dataPrep/save_reblock_32.dml -config code/conf/ulab32.xml -args "census/train_census_enc_128x"  
# systemds code/dataPrep/save_reblock_32.dml -config code/conf/ulab32.xml -args "census/train_census_enc_256x" 

# systemds code/dataPrep/save_reblock.dml -config code/conf/ulab16.xml -args "census/test_census"