#!/bin/bash

export LOG4JPROP='code/logging/log4j-compression.properties'

logstart="results/lossy_classification"
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"

echo "code/e2enew/lossy_classification.sh"
exrep=2
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
            timeout 3600 \
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
    # run binary_lm_1 TULAb16 singlenode $1.bin $2
    # run binary_lm_1 TCLAb16 singlenode $1.bin $2
    # run binary_lm_1 TAWAb16 singlenode $1.bin $2
    removetmp $1.bin

    run mtd_compress ULAb16 singlenode $1
    # run binary_lm_1 ULAb16 singlenode $1.cla $2
    # # run binary_lm_1 TULAb16 singlenode $1.cla $2
    # # run binary_lm_1 TCLAb16 singlenode $1.cla $2
    run binary_lm_1 TAWAb16 singlenode $1.cla $2
    removetmp $1.cla
}

binary_lm_last() {
    # removetmp
    # run binary_lm_last ULAb16 singlenode $1 $2
    # # run binary_lm_last TULAb16 singlenode $1 $2
    # # run binary_lm_last TCLAb16 singlenode $1 $2
    # run binary_lm_last TAWAb16 singlenode $1 $2
    # removetmp

    run mtd_detect ULAb16 singlenode $1
    run binary_lm_last ULAb16 singlenode $1.bin $2
    # run binary_lm_last TULAb16 singlenode $1.bin $2
    # run binary_lm_last TCLAb16 singlenode $1.bin $2
    # run binary_lm_last TAWAb16 singlenode $1.bin $2
    removetmp $1.bin

    run mtd_compress ULAb16 singlenode $1
    # run binary_lm_last ULAb16 singlenode $1.cla $2
    # run binary_lm_last TULAb16 singlenode $1.cla $2
    # run binary_lm_last TCLAb16 singlenode $1.cla $2
    run binary_lm_last TAWAb16 singlenode $1.cla $2
    removetmp $1.cla
}

# binary -- last column

# # Cat 
file="data/cat/train.csv"
spec="code/scripts/specs/catindat"
ls=("l1 l2 l3 l5 l10 l20 l40 l80")
for t in $ls; do
   binary_lm_last $file ${spec}_$t.json
done 

# # Adult
file="data/adult/adult.csv"
spec="code/scripts/specs/adult"
binary_lm_last $file $spec
ls=("l1 l2 l3 l5 l10 l20 l40 l80")
for t in $ls; do
   binary_lm_last $file ${spec}_$t.json
done 
# # binary -- first column

# # Sanatander
file="data/santander/train.csv"
spec="code/scripts/specs/santander"
ls=("l1 l2 l3 l5 l10 l20 l40 l80")
for t in $ls; do
   binary_lm_1 $file ${spec}_$t.json
done 

# # Home
file="data/home/train.csv"
spec="code/scripts/specs/home"
ls=("l1 l2 l3 l5 l10 l20 l40 l80")
for t in $ls; do
   binary_lm_1 $file ${spec}_$t.json
done 

# Criteo
# file="data/criteo/day_0_100000.tsv"
file="data/criteo/day_0_10000000.tsv"
spec="code/scripts/specs/criteo"
# binary_lm_1 $file $spec
ls=("l1 l2 l3 l5 l10 l20 l40 l80")
for t in $ls; do
   binary_lm_1 $file ${spec}_$t.json
done 

