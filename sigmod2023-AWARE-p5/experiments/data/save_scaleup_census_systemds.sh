#/bin/bash

source parameters.sh

export SYSDS_DISTRIBUTED=1

hdfs dfs -mkdir -p data/census
hdfs dfs -put data/census data

# systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc"    "census/train_census_enc_2x"
# systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc_2x"    "census/train_census_enc_4x"
# systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc_4x"    "census/train_census_enc_8x"
# systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc_8x"    "census/train_census_enc_16x"
# systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc_16x"   "census/train_census_enc_32x"
# systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc_32x"   "census/train_census_enc_64x"
# systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc_64x"   "census/train_census_enc_128x"
systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc_128x"   "census/train_census_enc_256x"
