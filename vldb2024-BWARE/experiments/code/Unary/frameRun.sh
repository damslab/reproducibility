#!/bin/bash

echo "Running Read and Write Compressed experiments"

export LOG4JPROP='code/logging/log4j-compression.properties'

exrep=5
inrep=5
clear=1
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"
profileEnabled=1
mode="singlenode"

# Experiment 1! write and read different blocksizes compressed and binary.
blockSizes=("0.5 1 2 4 8 16 32 64 128")
blockSizes=("64")
techniques=("ULA")
format=("binary")

sparsities=("0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0")

unary=("cbind rbind")

write() {
    rm -f $1
    # write is only to materialize already there.
    systemds \
        code/ReadWrite/frameWrite.dml \
        -config code/conf/${3}b${5}.xml \
        -stats 100 \
        -exec "$mode" \
        -debug \
        -seed $seed \
        -args $9 2000 $6 $7 $8 $4 $2 \
        >>$1 2>&1

    echo "--- Write (materialize) : $1"
}

unaryexp() {
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
                code/Unary/$6.dml \
                -config code/conf/${3}b${5}.xml \
                -stats 100 \
                -exec "$mode" \
                -debug \
                -seed $seed \
                -args $2 $inrep \
                >>$1 2>&1
            export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"
        done

        echo "--- $6  : $1"

    fi
}

for t in $techniques; do
    for f in $format; do
        mkdir -p "results/unaryW/$HOSTNAME/$t-$f/"
        mkdir -p "tmp/unary/$HOSTNAME/$t-$f/"
        for b in $blockSizes; do
            writeLog="results/unaryW/$HOSTNAME/$t-$f/B$b-$mode-Sparse0.5-64k-Binary-Write.log"
            tmpFile="tmp/unary/$HOSTNAME/$t-$f/B$b-$mode-Sparse0.5-64k-Binary-Write.$f"
            write $writeLog $tmpFile $t $f $b 1 1 0.5 64000

            for u in $unary; do
                mkdir -p "results/unary/$HOSTNAME/$t-$f-$u/"
                fullLogName="results/unary/$HOSTNAME/$t-$f-$u/B$b-$mode-Sparse0.5-64k-Binary-Write.log"
                unaryexp $fullLogName $tmpFile $t $f $b $u
            done
        done
    done
done
