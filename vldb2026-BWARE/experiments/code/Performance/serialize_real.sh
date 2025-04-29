#!/bin/bash

mainFolder="results/performance/$HOSTNAME"
mkdir -p $mainFolder

export LOG4JPROP='code/logging/log4j-off.properties'

OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"
profileEnabled=1
# profileEnabled=0
cm="$SYSTEMDS_ROOT/target/systemds-3.2.0-SNAPSHOT-perf.jar"

run=14

name() {
    input=$1
    OIFS=$IFS
    IFS='/'
    inSplit=($input)
    inName=${inSplit[-1]}
    # echo $inName
    IFS=$OIFS
    echo "$inName"
    # return $inName
}

run() {
    input=$1
    spec=$2
    t=$3
    repeats=$4
    id=$5
    # name $input
    inname=$(name $input)
    inspec=$(name $spec)
  
    rm -fr tmp

    sub_folder="Serial_real"
    mkdir -p "$mainFolder/$sub_folder"
    main_name="Ser-$inname-$inspec-$t-$id"
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

    echo "Perf_real: $logFile.log --- Args: $run $t $repeats $inname $inspec " | tee $logFile.log

    # execute new
    if [ $profileEnabled == 1 ]; then
        perf stat -d -d -d \
            java $OPTS \
            -XX:CompileThreshold=10 \
            -Dlog4j.configuration=file:$LOG4JPROP -jar \
            $cm $run $t $repeats $input $spec $id\
            >>$logFile.log 2>&1
    else
        java $OPTS \
            -XX:CompileThreshold=10 \
            -Dlog4j.configuration=file:$LOG4JPROP -jar \
            $cm $run $t $repeats $input $spec $id\
            >>$logFile.log 2>&1
    fi
}


# run  1 10000 "tmp/perf-tmp.bin" -1

spec="code/scripts/specs/adult_spec2.json"
input="data/adult/adult.csv"
# run $input $spec 1 100 -1
# run $input $spec $SYSTEM_THREADS 1000 -1

input="data/cat/train.csv"
spec="code/scripts/specs/catindat_spec3.json"

# run $input $spec 1 20 -1
run $input $spec $SYSTEM_THREADS 10 -1

spec="code/scripts/specs/catindat_spec4.json"

# run $input $spec 1 20 -1
# run $input $spec $SYSTEM_THREADS 100 -1


## \red{TODO} figure out criteo
# spec="code/scripts/specs/criteo_fe1.json"
input="data/criteo/day_0_1000.tsv"
input="data/criteo/day_0_10000.tsv"
input="data/criteo/day_0_100000.tsv"

spec="code/scripts/specs/criteo_fe1.json"
# run $input $spec 1 10 -1
# run $input $spec $SYSTEM_THREADS 100 -1
spec="code/scripts/specs/criteo_fe2.json"
# run $input $spec 1 10 -1
# run $input $spec $SYSTEM_THREADS 100 -1
spec="code/scripts/specs/criteo_fe3.json"
# run $input $spec 1 10 -1
# run $input $spec $SYSTEM_THREADS 100 -1
spec="code/scripts/specs/criteo_fe4.json"
# run $input $spec 1 10 -1
# run $input $spec $SYSTEM_THREADS 100 -1
spec="code/scripts/specs/criteo_fe5.json"
# run $input $spec 1 10 -1
# run $input $spec $SYSTEM_THREADS 100 -1

##santader
input="data/santander/train.csv"
spec="code/scripts/specs/santander_spec1.json"
# run $input $spec 1 30 -1
# run $input $spec $SYSTEM_THREADS 30 -1

spec="code/scripts/specs/santander_spec2.json"
# run $input $spec 1 10 -1
# run $input $spec $SYSTEM_THREADS 100 -1

spec="code/scripts/specs/santander_spec3.json"
# run $input $spec 1 10 -1
# run $input $spec $SYSTEM_THREADS 100 -1





