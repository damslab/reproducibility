#!/bin/bash

mainFolder="results/performance/$HOSTNAME"
mkdir -p $mainFolder

export LOG4JPROP='code/logging/log4j-off.properties'

OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"
# profileEnabled=1
profileEnabled=0
cm="$SYSTEMDS_ROOT/target/systemds-3.2.0-SNAPSHOT-perf.jar"

# Arguments
sparsities=("0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0")
rows=("500 1000 2000 4000 8000 16000")
cols=("5 10 25 50 100 250 500 1000 2000")
unique=("1 2 4 8 16 32 64 128 256 512 1024")
threads=("1 2 4 8 16 32 64")

# sparsities=("0.3 1.0")
# sparsities=("1.0")
# rows=("10000")
# rows=("50000")
# rows=("100000")
# cols=("100 1000 5000")
# cols=("10000")
# unique=("2 32")
# unique=("32")
# threads=("1 16")
# threads=("16")
# threads=("32")
# threads=("48")
# threads=("96")

sparsities=("0.01 0.38 1.0")
unique=("64 2048")
rows=("10000 1000000")
cols=("100 10000")
rows=("1000000")
cols=("10000")
threads=("1 6 12 18 24 36 48 72 96")
threads=("1 2 3 4 5 6 7 8 9 10 11 12 14 15 16 17 18 24 36 48 72 96")

# sparsities=("0.01")
sparsities=("1.0")
unique=("64")
rows=("100000")
cols=("1000")
# threads=("1 2 3 4")
threads=("1 8 16")
# threads=("4 12")
profileEnabled=1

run=9
repeats=10

## Apply
## Apply serialize
## Apply serialize write append
## Serialize Uncompressed

for r in $rows; do
    for c in $cols; do
        for u in $unique; do
            for s in $sparsities; do
                for t in $threads; do
                    sub_folder="WInM/$r/$c/$u/$t"
                    mkdir -p "$mainFolder/$sub_folder"
                    main_name="WInM-$r-$c-$u-$s-$t"
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

                    echo "Perf: $logFile.log --- Args: $run $r $c $u $s $t $repeats"

                    # execute new
                    if [ $profileEnabled == 1 ]; then
                        perf stat -d -d -d \
                            java $OPTS \
                            -Dlog4j.configuration=file:$LOG4JPROP -jar \
                            $cm $run $r $c $u $s $t $repeats \
                            >>$logFile.log 2>&1
                    else
                        java $OPTS \
                            -Dlog4j.configuration=file:$LOG4JPROP -jar \
                            $cm $run $r $c $u $s $t $repeats \
                            >>$logFile.log 2>&1
                    fi

                done
            done
        done
    done
done
