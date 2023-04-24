#!/bin/bash

# source parameters.sh

# # Compression repetitions - for the compression experiments only.
# compressionRep=1

# # Techniques used:
# techniques=("clab16 claWorkloadb16")
# sysmltechniques=("cla-sysml")

# # Data used
# data=("covtypeNew census census_enc airlines infimnist_1m")

# Note be carefull about this experiments since it takes 37 hours in cla-sysml.
# data=("amazon")

#Setup
# export LOG4JPROP='code/conf/log4j-factory.properties'

logstart="results/compression/"
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
    for y in $techniques; do
        mkdir -p "$logstart/$x/$d/$HOSTNAME/"
        fullLogname="$logstart/$x/$d/$HOSTNAME/$y-$mode.log"

        if [ ! -f "$fullLogname" ] || [ $clear == 1 ]; then

            if [ $sysds == 1 ]; then
                source loadSysDSSettings.sh
                rm -f $fullLogname
                for i in $(seq $exrep); do
                    perf stat -d -d -d \
                        systemds \
                        code/compression/read.dml \
                        -config code/conf/$y.xml \
                        -stats \
                        -exec singlenode \
                        -debug \
                        -seed $seed \
                        -args "data/$folder/train_$d.data" \
                        $compressionRep \
                        >>$fullLogname 2>&1

                done
                rm -f $fullLogname.res
                echo "------------------------------------"
                echo "$HOSTNAME - $d-Compress-$y"
                cat $fullLogname | grep -E 'compressed size|col groups types|Cache times |compression ratio|col groups types|col groups sizes|execution time| 1  compress |Total elapsed time| instructions |  cycles  | CPUs utilized ' | tee -a $fullLogname.res
                echo "$HOSTNAME - $d-Compress-$y"
                echo "------------------------------------"
            fi

        fi
    done

    for y in $sysmltechniques; do

        mkdir -p "$logstart/$x/$d/$HOSTNAME/"
        fullLognamesysml="$logstart/$x/$d/$HOSTNAME/$y-$mode-sysml.log"
        if [ ! -f "$fullLognamesysml" ] || [ $clear == 1 ]; then
            if [ $sysml == 1 ]; then
                source loadSysMLSettings.sh
                rm -f $fullLognamesysml
                for i in $(seq $exrep); do

                    perf stat -d -d -d \
                        java ${SYSTEMML_STANDALONE_OPTS} \
                        -cp ${sysmlClassPath} \
                        -Dlog4j.configuration=file:${LOG4JPROP_SYSML} \
                        org.apache.sysml.api.DMLScript \
                        -f code/compression/read-noWorkload.dml \
                        -exec singlenode \
                        -config code/conf/$y.xml \
                        -stats \
                        -args "data/$folder/train_$d.csv" \
                        $compressionRep \
                        >>$fullLognamesysml 2>&1
                done

                rm -f $fullLognamesysml.res
                echo "------------------------------------"
                echo "$HOSTNAME - $d-Compress-$y"
                cat $fullLognamesysml | grep -E 'compressed size|col groups types|Cache times |compression ratio|col groups types|col groups sizes|execution time| 1  compress |Total elapsed time| instructions |  cycles  | CPUs utilized ' | tee -a $fullLognamesysml.res
                echo "$HOSTNAME - $d-Compress-$y"
                echo "------------------------------------"
            fi

        fi
    done
done

SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"
