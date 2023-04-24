#!/bin/bash

export SYSDS_DISTRIBUTED=1

logstart="results/algorithms/"
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"
for d in $data; do

    for x in $algorithms; do

        for y in $sysmltechniques; do

            mkdir -p "$logstart/$x/$d/$HOSTNAME/"

            fullLognamesysml="$logstart/$x/$d/$HOSTNAME/$y-singlenode-spark.log"

            if [ ! -f "$fullLognamesysml" ] || [ $clear == 1 ]; then
                if [ $sysml == 1 ]; then

                    # source loadSysMLSettings.sh
                    rm -f $fullLognamesysml
                    for i in $(seq $exrep); do
                        printf "."

                        perf stat -d -d -d \
                            spark-submit \
                            --master yarn \
                            --deploy-mode client \
                            --driver-memory 110g \
                            --conf spark.driver.extraJavaOptions="-XX:+UseG1GC -Xms110g -Xmn11g -Dlog4j.configuration=file:$LOG4JPROP_SYSML" \
                            --conf spark.executor.extraJavaOptions="-XX:+UseG1GC -Xms105g -Xmn10g" \
                            --files $LOG4JPROP_SYSML \
                            --conf spark.executor.heartbeatInterval=10000000s \
                            --conf spark.network.timeout=10000001s \
                            --conf spark.executor.memoryOverhead=10000 \
                            --conf spark.task.maxFailures=10 \
                            --conf spark.storage.memoryMapThreshold=150m \
                            --num-executors 6 \
                            --executor-memory 105g \
                            --executor-cores 32 \
                            $HOME/github/systemml/target/SystemML.jar \
                            -f code/algorithms/${x}.dml \
                            -config code/conf/$y.xml \
                            -stats 100 \
                            -exec singleNode \
                            -args "data/census/${d}_sysML.data" \
                            1 \
                            "results/algorithms/$x/$d/cla-sysml-spark.csv" \
                            "data/census/${d}_labels_sysML.data" \
                            "data/census/test_census_sysML.data" \
                            "data/census/test_census_labels_sysML.data" \
                            >>$fullLognamesysml 2>&1

                        # --files $LOG4JPROP_SYSML \
                            # --conf spark.driver.extraJavaOptions=\"-XX:+UseG1GC -Xms110g -Xmn11g\" \
                        # --conf spark.driver.extraJavaOptions="-Xms110g -Xmn11g -Dlog4j.configuration=file:$LOG4JPROP_SYSML" \
                        # --conf spark.executor.extraJavaOptions="-Dlog4j.configuration=file:$LOG4JPROP_SYSML" \
                        # -cp ${sysmlClassPath} \
                    done

                    echo "------------------------------------"
                    rm -f $fullLognamesysml.res
                    echo "$HOSTNAME - $d-$x-$y"
                    cat $fullLognamesysml | grep -E 'compress |Total elapsed time| instructions | cycles  | CPUs utilized ' | tee -a $fullLognamesysml.res
                    echo "$HOSTNAME - $d-$x-$y"
                    echo "------------------------------------"
                fi
            fi
        done
    done
done

SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"
