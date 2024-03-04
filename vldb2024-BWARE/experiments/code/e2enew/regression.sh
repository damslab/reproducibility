#!/bin/bash

export LOG4JPROP='code/logging/log4j-compression.properties'

logstart="results/regression"
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"

echo "code/e2enew/regression.sh"
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
            timeout 200 \
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

# regression

# # # Crypto
file="data/crypto/train.csv"
spec="code/scripts/specs/crypto_full.json"

# removetmp $file.bin
run mtd_detect ULAb16 singlenode $file 
run regress_lm ULAb16 singlenode $file.bin $spec
# removetmp $file.bin

# removetmp $file.cla
run mtd_compress ULAb16 singlenode $file 
run regress_lm TAWAb16 singlenode $file.cla $spec
# removetmp $file.cla






# # #  KDD
file="data/kdd98/cup98lrn.csv"
spec="code/scripts/specs/kdd_full.json"

# removetmp $file.bin
run mtd_detect ULAb16 singlenode $file 
run regress_lm ULAb16 singlenode $file.bin $spec
# removetmp $file.bin


# removetmp $file.cla
run mtd_compress ULAb16 singlenode $file 
run regress_lm TAWAb16 singlenode $file.cla $spec
# removetmp $file.cla





