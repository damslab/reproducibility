#!/bin/bash

echo "Running Read and Write Compressed experiments"

export LOG4JPROP='code/logging/log4j-compression.properties'

exrep=5
clear=1
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"
profileEnabled=1
mode="singlenode"

# Experiment 1! write and read different blocksizes compressed and binary.
# blockSizes=("1 2 4 8")
# blockSizes=("0.5 32 64 128")
# blockSizes=("0.5")
blockSizes=("0.5 1 2 4 8 16 32 64 128")
# blockSizes=("0.5 1 ")
# blockSizes=("64")
techniques=("ULA")
format=("binary csv")
format=("binary")

sparsities=("0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0")


write() {
    if [ ! -f "$1" ] || [ $clear == 1 ]; then
        rm -f $1

        for i in $(seq $exrep); do
            if [ $profileEnabled == 1 ]; then
                mkdir -p "$1-perf"
                profile="$1-perf/$i.profile.html"
                export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/build/libasyncProfiler.so=start,event=cpu,file=$profile"
            fi
            perf stat -d -d -d \
                systemds \
                code/ReadWrite/frameWrite.dml \
                -config code/conf/${3}b${5}.xml \
                -stats 100 \
                -exec "$mode" \
                -debug \
                -seed $seed \
                -args $9 2000 $6 $7 $8 $4 $2 \
                >>$1 2>&1
            # Disk size add.
            du $2 >>$1
            export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"
        done
        echo "--- Write : $1"
    fi
}

readfile() {
    if [ ! -f "$1" ] || [ $clear == 1 ]; then
        rm -f $1

        for i in $(seq $exrep); do
            if [ $profileEnabled == 1 ]; then
                mkdir -p "$1-perf"
                profile="$1-perf/$i.profile.html"
                export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/build/libasyncProfiler.so=start,event=cpu,file=$profile"
            fi
            perf stat -d -d -d \
                systemds \
                code/ReadWrite/frameRead.dml \
                -config code/conf/${3}b${5}.xml \
                -stats 100 \
                -exec "$mode" \
                -debug \
                -seed $seed \
                -args $2 \
                >>$1 2>&1
            export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"
        done

        echo "--- Read  : $1"

    fi
}

for t in $techniques; do
    for f in $format; do
        mkdir -p "results/WriteFrame/$HOSTNAME/$t-$f/"
        mkdir -p "results/ReadFrame/$HOSTNAME/$t-$f/"
        mkdir -p "tmp/WriteFrame/$HOSTNAME/$t-$f/"

        # echo "BASELINES:"
        # fullLogName="results/WriteFrame/$HOSTNAME/$t-$f/B1-$mode-Sparse0.5-64k-Binary-Write.log"
        # fullFileName="tmp/WriteFrame/$HOSTNAME/$t-$f/B1-$mode-Sparse0.5-64k-Binary.$f"
        # write $fullLogName $fullFileName $t $f  1 1 0.5 64000
        # fullLogName="results/ReadFrame/$HOSTNAME/$t-$f/B1-$mode-Sparse0.5-64k-Binary-Read.log"
        # readfile $fullLogName $fullFileName $t $f 1 0.5

        # echo "Blocksizes:"
        # for b in $blockSizes; do
        #     fullLogName="results/WriteFrame/$HOSTNAME/$t-$f/B$b-$mode-Sparse0.5-64k-Binary-Write.log"
        #     fullFileName="tmp/WriteFrame/$HOSTNAME/$t-$f/B$b-$mode-Sparse0.5-64k-Binary.$f"
        #     write $fullLogName $fullFileName $t $f $b 1 1 0.5 64000
        #     fullLogName="results/ReadFrame/$HOSTNAME/$t-$f/B$b-$mode-Sparse0.5-64k-Binary-Read.log"
        #     readfile $fullLogName $fullFileName $t $f $b 0.5
        # done 

        echo "Sparsities:"
        for s in $sparsities; do
            fullLogName="results/WriteFrame/$HOSTNAME/$t-$f/B16-$mode-Sparse$s-64k-Binary-Write.log"
            fullFileName="tmp/WriteFrame/$HOSTNAME/$t-$f/B16-$mode-Sparse$s-64k-Binary.$f"
            write $fullLogName $fullFileName $t $f 16 1 1 $s 64000
            fullLogName="results/ReadFrame/$HOSTNAME/$t-$f/B16-$mode-Sparse$s-64k-Binary-Read.log"
            readfile $fullLogName $fullFileName $t $f 16 $s
        done 

    done

done
