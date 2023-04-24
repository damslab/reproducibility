#/bin/bash

source parameters.sh

# export SYSDS_DISTRIBUTED=1

export LOG4JPROP='code/conf/log4j-compress-spark.properties'

logstart="results/sparkCompression/"
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"

techniques=("clab1 clab2 clab4 clab8 clab16 clab32 clab64 clab128 clab256 claWorkloadb1 claWorkloadb2 claWorkloadb4 claWorkloadb8 claWorkloadb16 claWorkloadb32 claWorkloadb64 claWorkloadb128 claWorkloadb256")

# techniques=("clab1 claWorkloadb256")

data=("census_enc")

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
        fullLogname="$logstart/$x/$d/$HOSTNAME/$y-spark.log"
        if [ ! -f "$fullLogname" ] || [ $clear == 1 ]; then

            if [ $sysds == 1 ]; then
                source loadSysDSSettings.sh
                rm -f $fullLogname
                for i in $(seq $exrep); do
                      perf stat -d -d -d \
                        systemds \
                        code/compression/read.dml \
                        -config code/conf/$y.xml \
                        -stats -debug \
                        -exec spark \
                        -seed $seed \
                        -args "data/$folder/train_$d.data" \
                        $compressionRep \
                        >>$fullLogname 2>&1

                done
                rm -f $fullLogname.res
                echo "------------------------------------"
                echo "$HOSTNAME - $d-Compress-$y-Spark"
                cat $fullLogname | grep -E 'compressed size|col groups types|Cache times |compression ratio|col groups types|col groups sizes|execution time| 1  compress |Total elapsed time| instructions |  cycles  | CPUs utilized ' | tee -a $fullLogname.res
                echo "$HOSTNAME - $d-Compress-$y-Spark"
                echo "------------------------------------"
            fi

        fi
    done
done
SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"
