#!/bin/bash

export LOG4JPROP='code/logging/log4j-compression.properties'

logstart="results/lossy_scaling"
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"

echo "code/e2enew/lossy_scaling.sh"
exrep=1
profileEnabled=1

run() {
    alg=$1
    conf="code/conf/$2.xml"
    mode=$3

    shift 3

    logDir="$logstart/$HOSTNAME/$alg/$conf/$mode"

    # make log string correct.
    t=$IFS
    IFS="_"
    lname="$*"
    lname="${lname//'/'/'-'}"
    log="$logDir/$lname.log"
    IFS=$t

    if [ -f "$log" ]; then
        mv $log "$log$(date +"%m-%d-%y-%r").log"
    fi

    echo -n "--- Log : $log "
    i=1
    for i in $(seq $exrep); do

        if [ $profileEnabled == 1 ]; then
            mkdir -p "$log-perf"
            profile="$log-perf/$i.profile.html"
            export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/lib/libasyncProfiler.so=start,event=cpu,file=$profile"
        fi

        perf stat -d -d -d \
            timeout 50000 \
            systemds \
            code/e2enew/$alg.dml \
            -config $conf \
            -stats 100 -debug \
            -exec $mode \
            -seed $seed \
            -args $* \
            >>$log 2>&1
        # -explain \
        echo -n "."

        export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"
    done
    echo ""
}

removetmp() {
    rm -fr $1.tmp
    rm -fr $1.tmp.dict
    rm -fr $1.tmp.mtd
    rm -fr $1.tmp.tmp
    rm -fr $1.tmp.tmp.dict
    rm -fr $1.tmp.tmp.mtd
}

binary_lm_1() {
    # removetmp
    # run binary_lm_1 ULAb16 singlenode $1 $2
    # run binary_lm_1 TULAb16 singlenode $1 $2
    # # run binary_lm_1 TCLAb16 singlenode $1 $2
    # run binary_lm_1 TAWAb16 singlenode $1 $2
    # removetmp

    run mtd_detect ULAb16 singlenode $1
    run binary_lm_1 ULAb16 singlenode $1.bin $2
    # # run binary_lm_1 TULAb16 singlenode $1.bin $2
    # # run binary_lm_1 TCLAb16 singlenode $1.bin $2
    # run binary_lm_1 TAWAb16 singlenode $1.bin $2
    # removetmp

    run mtd_compress ULAb16 singlenode $1
    # run binary_lm_1 ULAb16 singlenode $1.cla $2
    # # run binary_lm_1 TULAb16 singlenode $1.cla $2
    # # run binary_lm_1 TCLAb16 singlenode $1.cla $2
    run binary_lm_1 TAWAb16 singlenode $1.cla $2
    # removetmp
}



# Criteo
spec="code/scripts/specs/criteo"
# file="data/criteo/day_0_10000.tsv"
# binary_lm_1 $file ${spec}_l10.json
# binary_lm_1 $file ${spec}_full.json
# file="data/criteo/day_0_100000.tsv"
# binary_lm_1 $file ${spec}_l10.json
# binary_lm_1 $file ${spec}_full.json
# file="data/criteo/day_0_1000000.tsv"
# binary_lm_1 $file ${spec}_l10.json
# binary_lm_1 $file ${spec}_full.json
# file="data/criteo/day_0_10000000.tsv"
# binary_lm_1 $file ${spec}_l10.json
# binary_lm_1 $file ${spec}_full.json
file="data/criteo/day_0_100000000.tsv"
# binary_lm_1 $file ${spec}_l10.json
binary_lm_1 $file ${spec}_full.json
file="data/criteo/day_0.tsv"
binary_lm_1 $file ${spec}_l10.json
binary_lm_1 $file ${spec}_full.json

