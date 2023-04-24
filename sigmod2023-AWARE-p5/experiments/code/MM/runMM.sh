#!/bin/bash

logstart="results/MM"
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
    for x in $mm; do
        for s in $mVSizes; do
            for y in $techniques; do
                mkdir -p "$logstart/$x-$s/$d/$HOSTNAME/"
                fullLogname="$logstart/$x-$s/$d/$HOSTNAME/$y-$mode.log"
                if [ ! -f "$fullLogname" ] || [ $clear == 1 ]; then
                    if [ $sysds == 1 ]; then
                        source loadSysDSSettings.sh
                        rm -f $fullLogname

                        for i in $(seq $exrep); do
                            printf "."
                            perf stat -d -d -d \
                                systemds \
                                code/MM/$x.dml \
                                -config code/conf/$y.xml \
                                -stats 100 \
                                -exec "$mode" \
                                -debug \
                                -seed $seed \
                                -args "data/$folder/train_$d.data" $inrep $s \
                                "data/$folder/train_${d}_labels.data" \
                                >>$fullLogname 2>&1
                        done

                        echo "------------------------------------"
                        rm -f $fullLogname.res
                        echo "$HOSTNAME - $d-$x-$s-$y"
                        cat $fullLogname | grep -E '1  r| ba\+\*| compress |Total elapsed time| instructions | cycles  | CPUs utilized | tsmm | \*   | \+   ' | tee -a $fullLogname.res
                        echo "$HOSTNAME - $d-$x-$s-$y"
                        echo "------------------------------------"
                    fi
                fi
            done

            for y in $sysmltechniques; do
                mkdir -p "$logstart/$x-$s/$d/$HOSTNAME/"
                fullLognamesysml="$logstart/$x-$s/$d/$HOSTNAME/$y-$mode-sysml.log"

                if [ ! -f "$fullLognamesysml" ] || [ $clear == 1 ]; then
                    if [ $sysml == 1 ]; then
                        rm -f $fullLognamesysml
                        for i in $(seq $exrep); do
                            printf "."

                            if [[ "$d" =~ "census" ]]; then
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
                                    -f code/MM/$x.dml \
                                    -config code/conf/$y.xml \
                                    -stats 100 \
                                    -exec singleNode \
                                    -args "data/$folder/train_${d}_sysML.data" $inrep $s \
                                    "data/$folder/train_${d}_labels_sysML.data" \
                                    >>$fullLognamesysml 2>&1
                            else
                                source loadSysMLSettings.sh
                                perf stat -d -d -d \
                                    java ${SYSTEMML_STANDALONE_OPTS} \
                                    -cp ${sysmlClassPath} \
                                    -Dlog4j.configuration=file:${LOG4JPROP_SYSML} \
                                    org.apache.sysml.api.DMLScript \
                                    -f code/MM/$x.dml \
                                    -config code/conf/$y.xml \
                                    -stats 100 \
                                    -exec "$mode" \
                                    -args "data/$folder/train_$d.csv" $inrep $s \
                                    "data/$folder/train_${d}_labels.csv" \
                                    >>$fullLognamesysml 2>&1
                            fi
                        done
                        echo "------------------------------------"
                        rm -f $fullLognamesysml.res
                        echo "$HOSTNAME - $d-$x-$s-$y"
                        cat $fullLognamesysml | grep -E '1  r| ba\+\*| compress |Total elapsed time| instructions | cycles  | CPUs utilized | tsmm | \*   | \+   ' | tee -a $fullLognamesysml.res
                        echo "$HOSTNAME - $d-$x-$s-$y"
                        echo "------------------------------------"
                    fi
                fi
            done
        done
    done
done
SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"
