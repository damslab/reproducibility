#!/bin/bash

export SYSDS_DISTRIBUTED=1

logstart="results/algorithms/"

SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"
for d in $data; do
    if [[ "$d" =~ "infimnist" ]]; then
        folder="infimnist"
    elif [[ "$d" =~ "binarymnist" ]]; then
        folder="binarymnist"
    elif [[ "$d" =~ "census" ]]; then
        folder="census"
    else
        folder=$d
    fi

    for x in $algorithms; do

        for y in $sysmltechniques; do

            mkdir -p "$logstart/$x/$d/$HOSTNAME/"

            fullLognamesysml="$logstart/$x/$d/$HOSTNAME/cla-hybrid-sysml-spark.log"

            if [ ! -f "$fullLognamesysml" ] || [ $clear == 1 ]; then
                if [ $sysml == 1 ]; then

                    source loadSysMLSettings.sh
                    rm -f $fullLognamesysml
                    for i in $(seq $exrep); do
                        printf "."

                        perf stat -d -d -d \
                            spark-submit \
                            --master yarn \
                            --deploy-mode client \
                            --driver-memory 110g \
                            --conf spark.driver.extraJavaOptions="-Xms110g -Xmn11g" \
                            --conf spark.executor.heartbeatInterval=100s \
                            --conf spark.network.timeout=512s \
                            --num-executors 6 \
                            --executor-memory 105g \
                            --executor-cores 32 \
                            $HOME/github/systemml/target/SystemML.jar \
                            -f code/algorithms/${x}.dml \
                            -config code/conf/cla-sysmlb16.xml \
                            -stats 100 \
                            -args "data/census/train_census_enc_sysML_128x.data" \
                            1 \
                            "results/algorithms/$x/$d/cla-sysml-spark.csv" \
                            "data/census/train_census_enc_sysML_128x_labels.data" \
                            "data/census/test_census.csv" \
                            "data/census/test_census_labels.csv" \
                            >>$fullLognamesysml 2>&1

                        # -exec hybrid \
                        # --files $LOG4JPROP_SYSML \
                        # --conf spark.driver.extraJavaOptions="-Xms110g -Xmn11g -Dlog4j.configuration=file:$LOG4JPROP_SYSML" \
                        # --conf spark.executor.extraJavaOptions="-Dlog4j.configuration=file:$LOG4JPROP_SYSML" \
                        # -cp ${sysmlClassPath} \
                    done

                    echo "------------------------------------"
                    rm -f $fullLognamesysml.res
                    echo "$HOSTNAME - $d-$x-$s-cla"
                    cat $fullLognamesysml | grep -E 'compress |Total elapsed time| instructions | cycles  | CPUs utilized ' | tee -a $fullLognamesysml.res
                    echo "$HOSTNAME - $d-$x-$s-cla"
                    echo "------------------------------------"
                fi
            fi
        done
    done
done

SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"
