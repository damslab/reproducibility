#!/bin/bash

export LOG4JPROP='code/logging/log4j-compression.properties'

logstart="results/pipeline"
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"

echo "code/e2enew/pipeline.sh"
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

removetmp(){
    rm -fr $1.tmp
    rm -fr $1.tmp.dict
    rm -fr $1.tmp.mtd
    rm -fr $1.tmp.tmp
    rm -fr $1.tmp.tmp.dict
    rm -fr $1.tmp.tmp.mtd
}

makeData() {
   exrept=$exrep
   exrep=1
   run mtd_detect ULAb16 singlenode $1
   run mtd_compress ULAb16 singlenode $1
   exrep=$exrept
}


# regression



# # #  KDD
# file="data/kdd98/cup98lrn.csv"
# spec="code/scripts/specs/kdd"
# # makeData $file
# run regress_lm_pipeline ULAb16  singlenode $file.bin $spec
# run regress_lm_pipeline AWAb16  singlenode $file.cla $spec
# run regress_lm_pipeline TAWAb16 singlenode $file.cla $spec

# # # # Adult
# file="data/adult/adult.csv"
# spec="code/scripts/specs/adult"
# run binary_lm_pipeline_last ULAb16 singlenode $file.bin $spec
# run binary_lm_pipeline_last AWAb16 singlenode $file.cla $spec
# run binary_lm_pipeline_last TAWAb16 singlenode $file.cla $spec



# # # # Crypto
# file="data/crypto/train.csv"
# # # file="data/crypto/train_10000.csv"
# spec="code/scripts/specs/crypto"
# # makeData $file
# run regress_lm_pipeline ULAb16 singlenode $file.bin $spec
# run regress_lm_pipeline AWAb16 singlenode $file.cla $spec
# run regress_lm_pipeline TAWAb16 singlenode $file.cla $spec




# # # Cat
file="data/cat/train.csv"
spec="code/scripts/specs/catindat"
# makeData $file
# run binary_lm_pipeline_last ULAb16 singlenode $file.bin $spec
run binary_lm_pipeline_last AWAb16 singlenode $file.cla $spec
# run binary_lm_pipeline_last TAWAb16 singlenode $file.cla $spec


# # # # Sanatander
# file="data/santander/train.csv"
# spec="code/scripts/specs/santander"
# makeData $file
# run binary_lm_pipeline_1 ULAb16 singlenode $file.bin $spec
# run binary_lm_pipeline_1 AWAb16 singlenode $file.cla $spec
# run binary_lm_pipeline_1 TAWAb16 singlenode $file.cla $spec

# # # # Home
file="data/home/train.csv"
spec="code/scripts/specs/home"
# makeData $file
# run binary_lm_pipeline_1 ULAb16 singlenode $file.bin $spec
run binary_lm_pipeline_1 AWAb16 singlenode $file.cla $spec
# run binary_lm_pipeline_1 TAWAb16 singlenode $file.cla $spec

# # # #  Criteo
# file="data/criteo/day_0_10000000.tsv"
# spec="code/scripts/specs/criteo"
# makeData $file
# run binary_lm_pipeline_1 ULAb16 singlenode $file.bin $spec
# run binary_lm_pipeline_1 AWAb16 singlenode $file.cla $spec
# run binary_lm_pipeline_1 TAWAb16 singlenode $file.cla $spec