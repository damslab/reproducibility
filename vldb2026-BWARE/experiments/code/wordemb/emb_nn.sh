#!/bin/bash
export LOG4JPROP='code/logging/log4j-compression.properties'

SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"

echo "code/wordemb/emb_nn.sh"
logstart="results/wordemb/emb_nn"

profileEnabled=1

run() {
    conf="code/conf/$1.xml"
    mode=$2

    shift 2

    logDir="$logstart/$HOSTNAME/$conf/$mode"

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
            if [ -f "$profile" ]; then
              mv $profile "$profile$(date +"%m-%d-%y-%r").html"
            fi
            export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/lib/libasyncProfiler.so=start,event=cpu,file=$profile"
        fi

        perf stat -d -d -d \
            timeout 7200 \
            systemds \
            code/wordemb/emb_nn.dml \
            -config $conf \
            -stats 100 -debug \
            -exec $mode \
            -seed $seed \
            -args $* \
            >>$log 2>&1
        echo -n "."

        export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"
    done
    echo ""
}

for a in $as; do
    for w in $ws; do 
        for l in $al; do
            # run ULAb16 singlenode $a $w $l
            # run MKLb16 singlenode $a $w $l
            run AWAb16 singlenode $a $w $l
        done 
    done 
done 
