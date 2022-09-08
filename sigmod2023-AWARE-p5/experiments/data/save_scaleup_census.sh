#/bin/bash

source parameters.sh

export SYSDS_DISTRIBUTED=1

# systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc"    "census/train_census_enc_2x"
# systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc_2x"    "census/train_census_enc_4x"
# systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc_4x"    "census/train_census_enc_8x"
# systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc_8x"    "census/train_census_enc_16x"
# systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc_16x"   "census/train_census_enc_32x"
# systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc_32x"   "census/train_census_enc_64x"
# systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc_64x"   "census/train_census_enc_128x"
# systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc_128x"  "census/train_census_enc_256x"
# systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc_256x"  "census/train_census_enc_512x"
# systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc_512x"  "census/train_census_enc_1024x"
# systemds code/dataPrep/save_scaleup.dml -args "census/train_census_enc_1024x" "census/train_census_enc_2048x"

source loadSysMLSettings.sh

cmd="--master yarn \
    --deploy-mode client \
    --driver-memory 110g \
    --conf spark.driver.extraJavaOptions=\"-Xms110g\" \
    --conf spark.executor.heartbeatInterval=100s \
    --conf spark.network.timeout=512s \
    --num-executors 6 \
    --executor-memory 105g \
    --executor-cores 32 \
    $HOME/github/systemml/target/SystemML.jar \
    -config code/conf/sysmlb16.xml \
    -explain "
    # --conf spark.executor.extraJavaOptions=\"-Dlog4j.configuration=file:$LOG4JPROP_SYSML\" \
    # --files $LOG4JPROP_SYSML \

# spark-submit $cmd -f  "code/dataPrep/save_scaleup_fromCSV.dml" -args "census/train_census_enc" "data/census/train_census_enc_sysML_2x"
# spark-submit $cmd -f  "code/dataPrep/save_scaleup_sysml.dml" -args "census/train_census_enc_sysML_2x" "census/train_census_enc_sysML_4x"
# spark-submit $cmd -f "code/dataPrep/save_scaleup_sysml.dml" -args "census/train_census_enc_sysML_4x" "census/train_census_enc_sysML_8x"
# spark-submit $cmd -f "code/dataPrep/save_scaleup_sysml.dml" -args "census/train_census_enc_sysML_8x" "census/train_census_enc_sysML_16x"
# spark-submit $cmd -f "code/dataPrep/save_scaleup_sysml.dml" -args "census/train_census_enc_sysML_16x" "census/train_census_enc_sysML_32x"
# spark-submit $cmd -f "code/dataPrep/save_scaleup_sysml.dml" -args "census/train_census_enc_sysML_32x" "census/train_census_enc_sysML_64x"
spark-submit $cmd -f "code/dataPrep/save_scaleup_sysml.dml" -args "census/train_census_enc_sysML_64x" "census/train_census_enc_sysML_128x"
