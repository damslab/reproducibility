#!/bin/bash

echo "Running Read and Write Compressed experiments"

export LOG4JPROP='code/logging/log4j-compression.properties'

exrep=5
clear=1
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"
profileEnabled=1
mode="singlenode"

# Experiment 1! write and read different blocksizes compressed and binary.
blockSizes=("0.5 1 2 4 8 16 32 64 128")
techniques=("ULA")
format=("compressed binary")

# Experiment2! write and read different sparsities Binary
sparsities=("0.0 0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 0.91 0.92 0.93 0.94 0.95 0.96 0.97 0.98 0.99 1.0")
techniques=("ULA")
format=("compressed binary")

# Experiment3! write and read differnt blocksizes compressed ternary balanced
blockSizes=("0.5 1 2 4 8 16 32 64 128")
techniques=("ULA")
format=("compressed binary")

# Experiment4! write and read different number of distinct balanced
distinct=("1 2 3 4 5 6 7 8 9 10 16 32 64 128 256 512 1024 2048 4096 8192 16384 32768 65536")
techniques=("ULA")
format=("compressed binary")

# sparsities=("0.0")

# distinct=("11 12 13 14 15 16 17 18 19 20")
# distinct=("25 30 35 40 45 50")
distinct=("32 64 128 256")
# distinct=("60 70 80 90 100")
# distinct=("120 140 160 180 200")
# distinct=("250 300 350 400 450 500")
# distinct=("512 1024 2048 4096 8192 16384 32768 65536")
# distinct=("16384 32768 65536")

# blockSizes=("0.5")
# sparsities=("0.0 0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0")
# sparsities=("0.0 0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.1")
# sparsities=("0.91 0.92 0.93 0.94 0.95 0.96 0.97 0.98 0.99")
# sparsities=("0.3 0.9")
# sparsities=("1.0")
# sparsities=("0.0 1.0")
# sparsities=("0.0")
# sparsities=("0.03")
# techniques=("CLA AWA ULA")
# blockSizes=("128")
# blockSizes=("16")
# blockSizes=("0.5")
# blockSizes=("1")
# blockSizes=("0.5 1 2 4")
# blockSizes=("8 16 32 64 128")
# format=("compressed")
# blockSizes=("8")
# format=("binary")
# format=("compressed binary text csv")

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
                code/ReadWrite/write.dml \
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
        # cat $1 | grep -E ' Total elapsed time| instructions |  cycles  | CPUs utilized '
        # echo "---"
        # echo ""
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
                code/ReadWrite/read.dml \
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
        # cat $1 | grep -E ' Total elapsed time| instructions |  cycles  | CPUs utilized '
        # echo "---"
        # echo ""

    fi
}

for t in $techniques; do
    for f in $format; do
        mkdir -p "results/Write/$HOSTNAME/$t-$f/"
        mkdir -p "results/Read/$HOSTNAME/$t-$f/"
        mkdir -p "tmp/Write/$HOSTNAME/$t-$f/"

        # for s in $blockSizes; do
        # #     # Experiment 1 part 1
        #     fullLogName="results/Write/$HOSTNAME/$t-$f/B$s-$mode-Sparse0.5-64k-Binary-Write.log"
        #     fullFileName="tmp/Write/$HOSTNAME/$t-$f/B$s-$mode-Sparse0.5-64k-Binary.cla"
        #     write $fullLogName $fullFileName $t $f $s 1 1 0.5 64000
        #     fullLogName="results/Read/$HOSTNAME/$t-$f/B$s-$mode-Sparse0.5-64k-Binary-Read.log"
        #     readfile $fullLogName $fullFileName $t $f $s 0.5

        #     # Experiment 1 part 2
        #     fullLogName="results/Write/$HOSTNAME/$t-$f/B$s-$mode-Sparse0.5-256k-Binary-Write.log"
        #     fullFileName="tmp/Write/$HOSTNAME/$t-$f/B$s-$mode-Sparse0.5-256k-Binary.cla"
        #     write $fullLogName $fullFileName $t $f $s 1 1 0.5 256000
        #     fullLogName="results/Read/$HOSTNAME/$t-$f/B$s-$mode-Sparse0.5-256k-Binary-Read.log"
        #     readfile $fullLogName $fullFileName $t $f $s 0.5

        #     # Experiment 2 part 1
        #     fullLogName="results/Write/$HOSTNAME/$t-$f/B$s-$mode-Sparse1.0-64k-Ternary-Write.log"
        #     fullFileName="tmp/Write/$HOSTNAME/$t-$f/B$s-$mode-Sparse1.0-64k-Ternary.cla"
        #     write $fullLogName $fullFileName $t $f $s 0 3 1.0 64000
        #     fullLogName="results/Read/$HOSTNAME/$t-$f/B$s-$mode-Sparse1.0-64k-Ternary-Read.log"
        #     readfile $fullLogName $fullFileName $t $f $s 1.0
        # done

        # # experiment 2 Sparsities
        # for s in $sparsities; do
        #     fullLogName="results/Write/$HOSTNAME/$t-$f/B16-$mode-Sparse$s-64k-Binary-Write.log"
        #     fullFileName="tmp/Write/$HOSTNAME/$t-$f/B16-$mode-Sparse$s-64k-Binary.cla"
        #     write $fullLogName $fullFileName $t $f 16 1 1 $s 64000
        #     fullLogName="results/Read/$HOSTNAME/$t-$f/B16-$mode-Sparse$s-64k-Binary-Read.log"
        #     readfile $fullLogName $fullFileName $t $f 16

        #     fullLogName="results/Write/$HOSTNAME/$t-$f/B16-$mode-Sparse$s-256k-Binary-Write.log"
        #     fullFileName="tmp/Write/$HOSTNAME/$t-$f/B16-$mode-Sparse$s-256k-Binary.cla"
        #     write $fullLogName $fullFileName $t $f 16 1 1 $s 256000
        #     fullLogName="results/Read/$HOSTNAME/$t-$f/B16-$mode-Sparse$s-256k-Binary-Read.log"
        #     readfile $fullLogName $fullFileName $t $f 16
        # done

        # experiment 4 Distincts
        for s in $distinct; do
            fullLogName="results/Write/$HOSTNAME/$t-$f/B16-$mode-Sparse1.0-64k-Distinct$s-Write.log"
            fullFileName="tmp/Write/$HOSTNAME/$t-$f/B16-$mode-Sparse1.0-64k-Distinct$s.cla"
            write $fullLogName $fullFileName $t $f 16 0 $s 1.0 64000
            fullLogName="results/Read/$HOSTNAME/$t-$f/B16-$mode-Sparse1.0-64k-Distinct$s-Read.log"
            readfile $fullLogName $fullFileName $t $f 16

            # fullLogName="results/Write/$HOSTNAME/$t-$f/B16-$mode-Sparse1.0-256k-Distinct$s-Write.log"
            # fullFileName="tmp/Write/$HOSTNAME/$t-$f/B16-$mode-Sparse1.0-256k-Distinct$s.cla"
            # write $fullLogName $fullFileName $t $f 16 0 $s 1.0 256000
            # fullLogName="results/Read/$HOSTNAME/$t-$f/B16-$mode-Sparse1.0-256k-Distinct$s-Read.log"
            # readfile $fullLogName $fullFileName $t $f 16
        done
    done

done
