#/bin/bash

source parameters.sh

# source loadSysMLSettings.sh

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
    -config code/conf/ula-sysmlb16.xml \
    -explain "
    # --conf spark.executor.extraJavaOptions=\"-Dlog4j.configuration=file:$LOG4JPROP_SYSML\" \
    # --files $LOG4JPROP_SYSML \

# hdfs dfs -mkdir -p data/census

# # Save the files as binary local
# spark-submit $cmd -f "code/dataPrep/save_bin_census_enc_ml.dml" 
# Save the files as binary on hdfs.
spark-submit $cmd -f "code/dataPrep/save_bin_census_enc_ml.dml" 
# spark-submit $cmd -f "code/dataPrep/save_scaleup_sysml.dml" -args "census/train_census_enc" "census/train_census_enc_2x"
# spark-submit $cmd -f "code/dataPrep/save_scaleup_sysml.dml" -args "census/train_census_enc_2x" "census/train_census_enc_4x"
# spark-submit $cmd -f "code/dataPrep/save_scaleup_sysml.dml" -args "census/train_census_enc_4x" "census/train_census_enc_8x"
# spark-submit $cmd -f "code/dataPrep/save_scaleup_sysml.dml" -args "census/train_census_enc_8x" "census/train_census_enc_16x"
# spark-submit $cmd -f "code/dataPrep/save_scaleup_sysml.dml" -args "census/train_census_enc_16x" "census/train_census_enc_32x"
# spark-submit $cmd -f "code/dataPrep/save_scaleup_sysml.dml" -args "census/train_census_enc_32x" "census/train_census_enc_64x"
# spark-submit $cmd -f "code/dataPrep/save_scaleup_sysml.dml" -args "census/train_census_enc_64x" "census/train_census_enc_128x"
spark-submit $cmd -f "code/dataPrep/save_scaleup_sysml.dml" -args "census/train_census_enc_128x" "census/train_census_enc_256x"
