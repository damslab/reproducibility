#!/bin/bash

export LOG4JPROP='code/logging/log4j-compression.properties'

logstart="results/lossy_alg"
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"

echo "code/e2enew/lossy_lm.sh"
exrep=5
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
            timeout 40 \
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

removetmp(){
    rm -fr $1.tmp
    rm -fr $1.tmp.dict
    rm -fr $1.tmp.mtd
    rm -fr $1.tmp.tmp
    rm -fr $1.tmp.tmp.dict
    rm -fr $1.tmp.tmp.mtd
}

removevars(){
    rm -fr $1
    rm -fr $1.dict
    rm -fr $1.mtd
}



all_types_regress(){
#    run regress_lm ULAb16 singlenode $1.bin $2
   run regress_lm TAWAb16 singlenode $1.cla $2
   echo "Done: $1 $2"
}


# #  Crypto
file="data/crypto/train.csv"
spec="code/scripts/specs/crypto"
ls=("l1 l2 l3 l5 l10 l20 l40 l80 l160 l320 l640 l1280 l2560")
# ls=("l10 ")
# ls=("l80 ")


exrept=$exrep
exrep=1
run mtd_detect ULAb16 singlenode $file
run mtd_compress ULAb16 singlenode $file
exrep=$exrept


# all_types_regress $file ${spec}_full.json

for t in $ls; do
   all_types_regress $file ${spec}_$t.json
done 



# #  KDD
# file="data/kdd98/cup98lrn.csv"
# spec="code/scripts/specs/kdd"
# ls=("l1 l2 l3 l5 l10 l20 l40 l80 l160 l320 l640 l1280 l2560")
# # ls=("l10 ")
# exrept=$exrep
# exrep=1
# run mtd_detect ULAb16 singlenode $file
# run mtd_compress ULAb16 singlenode $file
# exrep=$exrept


# all_types_regress $file ${spec}_full.json

# for t in $ls; do
#    all_types_regress $file ${spec}_$t.json
# done 

# echo "Done: code/e2enew/lossy_lm.sh"

