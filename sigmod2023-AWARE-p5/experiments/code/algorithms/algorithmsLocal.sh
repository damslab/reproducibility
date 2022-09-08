#!/bin/bash

source parameters.sh

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
        for y in $techniques; do

            mkdir -p "$logstart/$x/$d/$HOSTNAME/"
            fullLogname="$logstart/$x/$d/$HOSTNAME/$y-$mode.log"
            if [ ! -f "$fullLogname" ] || [ $clear == 1 ]; then
                rm -f $fullLogname
                for i in $(seq $exrep); do
                    profile="hprof/$(date +"%Y-%m-%d-%T")-Alg-$HOSTNAME-$d-$x-$y-$i.html"
                    export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/build/libasyncProfiler.so=start,event=cpu,file=$profile"
                    printf "."
                    perf stat -d -d -d \
                        systemds \
                        code/algorithms/$x.dml \
                        -config code/conf/$y.xml \
                        -stats 100 -debug \
                        -exec $mode \
                        -seed $seed \
                        -explain \
                        -args "data/$folder/train_$d.data" \
                        1 \
                        "results/algorithms/$x/$d/$y.csv" \
                        "data/$folder/train_${d}_labels.data" \
                        "data/$folder/test_${folder}.data" \
                        "data/$folder/test_${folder}_labels.data" \
                        >>$fullLogname 2>&1

                done

                rm -f $fullLogname.res
                echo "------------------------------------"
                echo "$d-$x-$y -- $HOSTNAME"
                cat $fullLogname | grep -E ' compress  |Total elapsed time| instructions |  cycles  | CPUs utilized ' | tee -a $fullLogname.res
                echo "$d-$x-$y -- $HOSTNAME"
                echo "------------------------------------"
            fi
        done
    done
done

SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"
