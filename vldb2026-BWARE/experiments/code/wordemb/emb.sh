#!/bin/bash
export LOG4JPROP='code/logging/log4j-compression.properties'

SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"

echo "code/wordemb/emb.sh"
logstart="results/wordemb/emb"
logstart2="results/wordemb/emb_nn_real"


run() {
    conf="code/conf/$1.xml"
    mode=$2

    shift 2

    logDir="$logstart/$HOSTNAME/$conf/$mode"

    mkdir -p $logDir
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
            timeout $timeout \
            systemds \
            code/wordemb/emb.dml \
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



run2() {
    conf="code/conf/$1.xml"
    mode=$2

    shift 2

    logDir="$logstart2/$HOSTNAME/$conf/$mode"

    mkdir -p $logDir
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
            timeout $timeout \
            systemds \
            code/wordemb/emb_nn_real.dml \
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

run_tf() {
    logDir="$logstart/$HOSTNAME/tf"
    mkdir -p $logDir

    t=$IFS
    IFS="_"
    lname="$*"
    lname="${lname//'/'/'-'}"
    log="$logDir/$lname.log"
    IFS=$t


    echo -n "--- Log : $log "
    if [ -f "$log" ]; then
        mv $log "$log$(date +"%m-%d-%y-%r").log"
    fi
    for i in $(seq $exrep); do
        perf stat -d -d -d \
            timeout $timeout \
            python code/wordemb/tf_emb_real.py \
            --abstracts $1 \
            >>$log 2>&1
        echo -n "."
    done
    echo ""
}


run_tf2() {
    logDir="$logstart2/$HOSTNAME/tf2"
    mkdir -p $logDir

    t=$IFS
    IFS="_"
    lname="$*"
    lname="${lname//'/'/'-'}"
    log="$logDir/$lname.log"
    IFS=$t


    echo -n "--- Log : $log "
    if [ -f "$log" ]; then
        mv $log "$log$(date +"%m-%d-%y-%r").log"
    fi
    for i in $(seq $exrep); do
        perf stat -d -d -d \
            timeout $timeout \
            python code/wordemb/tf_emb_nn_real.py \
            --abstracts $1 \
            >>$log 2>&1
        echo -n "."
    done
    echo ""
}




for a in $as; do
    for w in $ws; do 
        run_tf "data/w2v/dblp_v14_abstracts_embedded_${w}_${a}.csv"
        run_tf2 "data/w2v/dblp_v14_abstracts_embedded_${w}_${a}.csv"
        # run ULAb16 singlenode \
        #     "data/w2v/dblp_v14_abstracts_embedded_${w}_${a}.bin" \
        #     "data/w2v/wiki-news-300d-1M.vec_$w.embedding.bin" 
        # run2 ULAb16 singlenode \
        #     "data/w2v/dblp_v14_abstracts_embedded_${w}_${a}.bin" \
        #     "data/w2v/wiki-news-300d-1M.vec_$w.embedding.bin" 

        # run MKLb16 singlenode \
        #     "data/w2v/dblp_v14_abstracts_embedded_${w}_${a}.bin" \
        #     "data/w2v/wiki-news-300d-1M.vec_$w.embedding.bin" 
        # run2 MKLb16 singlenode \
        #     "data/w2v/dblp_v14_abstracts_embedded_${w}_${a}.bin" \
        #     "data/w2v/wiki-news-300d-1M.vec_$w.embedding.bin" 

        # run AWAb16 singlenode \
        #     "data/w2v/dblp_v14_abstracts_embedded_${w}_${a}.bin" \
        #     "data/w2v/wiki-news-300d-1M.vec_$w.embedding.bin" 
        # run2 AWAb16 singlenode \
        #     "data/w2v/dblp_v14_abstracts_embedded_${w}_${a}.bin" \
        #     "data/w2v/wiki-news-300d-1M.vec_$w.embedding.bin" 
    done 
done 

