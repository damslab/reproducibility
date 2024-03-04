#!/bin/bash

mainFolder="results/performance/$HOSTNAME"
mkdir -p $mainFolder

export LOG4JPROP='code/logging/log4j-off.properties'

OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"
profileEnabled=1
# profileEnabled=0
cm="$SYSTEMDS_ROOT/target/systemds-3.2.0-SNAPSHOT-perf.jar"

run=12

run() {
    r=$1
    c=$2
    u=$3
    s=$4
    t=$5
    repeats=$6
    id=$7
    file=$8

    rm -fr tmp

    sub_folder="Serial"
    mkdir -p "$mainFolder/$sub_folder"
    main_name="Ser-$r-$c-$u-$s-$t-$run-$id"
    logFile="$mainFolder/$sub_folder/$main_name"
    if [ $profileEnabled == 1 ]; then
        mkdir -p "$mainFolder/$sub_folder/perf/"
        profile="$mainFolder/$sub_folder/perf/$main_name.html"
        OPTS="$OPTS_BASE -agentpath:$HOME/Programs/profiler/lib/libasyncProfiler.so=start,event=cpu,file=$profile"
    else
        OPTS="$OPTS_BASE"
    fi
    # remove old
    rm -f $logFile.log

    echo "Perf: $logFile.log --- Args: $run $r $c $u $s $t $repeats $id $file" | tee $logFile.log

    # execute new
    if [ $profileEnabled == 1 ]; then
        perf stat -d -d -d \
            java $OPTS \
            -XX:CompileThreshold=10 \
            -Dlog4j.configuration=file:$LOG4JPROP -jar \
            $cm $run $r $c $u $s $t $repeats $id $file\
            >>$logFile.log 2>&1
    else
        java $OPTS \
            -XX:CompileThreshold=10 \
            -Dlog4j.configuration=file:$LOG4JPROP -jar \
            $cm $run $r $c $u $s $t $repeats $id $file\
            >>$logFile.log 2>&1
    fi
}

# run 1000 100 64 1.0 1 1000 -1 "tmp/perf-tmp.bin"
# run 1000 10 64 1.0 1 1000 -1 "tmp/perf-tmp.bin"
# run 1000 100 64 1.0 1 1000 -1 "tmp/perf-tmp.bin"

# 80KB
run 1000 10 64 1.0 1 10000 -1 "tmp/perf-tmp.bin"
run 1000 10 64 1.0 $SYSTEM_THREADS 10000 -1 "tmp/perf-tmp.bin"

# # 800KB
run 1000 100 64 1.0 1 10000 -1 "tmp/perf-tmp.bin"
run 1000 100 64 1.0 $SYSTEM_THREADS 10000 -1 "tmp/perf-tmp.bin"

# # 8 MB
# # 12 minutes for 5000 make it 6 minutes with 2500 
run 1000 1000 64 1.0 1 2500 -1 "tmp/perf-tmp.bin"
run 1000 1000 64 1.0 $SYSTEM_THREADS 5000 -1 "tmp/perf-tmp.bin"

# # 80 MB
run 10000 1000 64 1.0 1 250 -1 "tmp/perf-tmp.bin"
run 10000 1000 64 1.0 $SYSTEM_THREADS 500 -1 "tmp/perf-tmp.bin"
# # 10 minutes for 500 lets reduce to 250 making it ~5 minuts

# # 800 MB
# # 85 minutes for 500 lets make it less.
# # 15 minutes
run 100000 1000 64 1.0 1 50 -1 "tmp/perf-tmp.bin"
run 100000 1000 64 1.0 $SYSTEM_THREADS 500 -1 "tmp/perf-tmp.bin"

# # 8 GB
# ## 3 hours to run 100. so 30 minutes to run 10 ... 10 should be okay.
# # 23 minutes
run 1000000 1000 64 1.0 1 10 -1 "tmp/perf-tmp.bin"
run 1000000 1000 64 1.0 $SYSTEM_THREADS 100 -1 "tmp/perf-tmp.bin"

# # 80 GB
# ## 8 hours to run... 100 iterations sooo lets do only 10 next time
run 10000000 1000 64 1.0 $SYSTEM_THREADS 10 -1 "tmp/perf-tmp.bin"
run 10000000 1000 64 1.0 1 6 -1 "tmp/perf-tmp.bin"

# ## only full serialization
# # run 10000000 1000 64 1.0 $SYSTEM_THREADS 6 3 "tmp/perf-tmp.bin"