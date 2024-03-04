# Read Compressed matrix vs read binary matrix into algrotihm

logstart="results/e2e"
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"

echo "code/e2e/E2_augment.sh"

run() {
    alg=$1
    conf="code/conf/$2.xml"
    mode=$3

    shift 3

    logDir="$logstart/$alg/$conf/$mode/$HOSTNAME"
    mkdir -p "$logDir/perf"

    IFS="_"
    lname="$*"
    lname="${lname//'/'/'-'}"
    log="$logDir/$lname.log"
    IFS=" "
    echo $log $alg $conf $mode

    rm -fr $log

    for i in {1..3}; do
        profile="$logDir/perf/$lname_$i.html"
        export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/lib/libasyncProfiler.so=start,event=cpu,file=$profile"

        perf stat -d -d -d \
            systemds \
            code/e2e/$alg.dml \
            -config $conf \
            -stats 100 -debug \
            -exec $mode \
            -seed $seed \
            -args $* \
            >>$log 2>&1
        # -explain \
        export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"
    done

}

input="data/santander/train.csv"

spec="code/scripts/specs/santander_pass.json"
run santander_lm ULAb1 singlenode $input $spec
run santander_lm_2 ULAb1 singlenode $input $spec
run santander_lm_3 ULAb1 singlenode $input $spec
run santander_lm_4 ULAb1 singlenode $input $spec
run santander_lm_5 ULAb1 singlenode $input $spec
run santander_lm_6 ULAb1 singlenode $input $spec
run santander_lm_7 ULAb1 singlenode $input $spec
run santander_lm_8 ULAb1 singlenode $input $spec
run santander_lm_9 ULAb1 singlenode $input $spec
run santander_lm_10 ULAb1 singlenode $input $spec

run santander_lm TCLAb1 singlenode $input $spec
run santander_lm_2 TCLAb1 singlenode $input $spec
run santander_lm_3 TCLAb1 singlenode $input $spec
run santander_lm_4 TCLAb1 singlenode $input $spec
run santander_lm_5 TCLAb1 singlenode $input $spec
run santander_lm_6 TCLAb1 singlenode $input $spec
run santander_lm_7 TCLAb1 singlenode $input $spec
run santander_lm_8 TCLAb1 singlenode $input $spec
run santander_lm_9 TCLAb1 singlenode $input $spec
run santander_lm_10 TCLAb1 singlenode $input $spec

run santander_lm TAWAb1 singlenode $input $spec
run santander_lm_2 TAWAb1 singlenode $input $spec
run santander_lm_3 TAWAb1 singlenode $input $spec
run santander_lm_4 TAWAb1 singlenode $input $spec
run santander_lm_5 TAWAb1 singlenode $input $spec
run santander_lm_6 TAWAb1 singlenode $input $spec
run santander_lm_7 TAWAb1 singlenode $input $spec
run santander_lm_8 TAWAb1 singlenode $input $spec
run santander_lm_9 TAWAb1 singlenode $input $spec
run santander_lm_10 TAWAb1 singlenode $input $spec

spec="code/scripts/specs/santander_spec_eqh5.json"
run santander_lm ULAb1 singlenode $input $spec
run santander_lm_2 ULAb1 singlenode $input $spec
run santander_lm_3 ULAb1 singlenode $input $spec
run santander_lm_4 ULAb1 singlenode $input $spec
run santander_lm_5 ULAb1 singlenode $input $spec
run santander_lm_6 ULAb1 singlenode $input $spec
run santander_lm_7 ULAb1 singlenode $input $spec
run santander_lm_8 ULAb1 singlenode $input $spec
run santander_lm_9 ULAb1 singlenode $input $spec
run santander_lm_10 ULAb1 singlenode $input $spec

run santander_lm TCLAb1 singlenode $input $spec
run santander_lm_2 TCLAb1 singlenode $input $spec
run santander_lm_3 TCLAb1 singlenode $input $spec
run santander_lm_4 TCLAb1 singlenode $input $spec
run santander_lm_5 TCLAb1 singlenode $input $spec
run santander_lm_6 TCLAb1 singlenode $input $spec
run santander_lm_7 TCLAb1 singlenode $input $spec
run santander_lm_8 TCLAb1 singlenode $input $spec
run santander_lm_9 TCLAb1 singlenode $input $spec
run santander_lm_10 TCLAb1 singlenode $input $spec

run santander_lm TAWAb1 singlenode $input $spec
run santander_lm_2 TAWAb1 singlenode $input $spec
run santander_lm_3 TAWAb1 singlenode $input $spec
run santander_lm_4 TAWAb1 singlenode $input $spec
run santander_lm_5 TAWAb1 singlenode $input $spec
run santander_lm_6 TAWAb1 singlenode $input $spec
run santander_lm_7 TAWAb1 singlenode $input $spec
run santander_lm_8 TAWAb1 singlenode $input $spec
run santander_lm_9 TAWAb1 singlenode $input $spec
run santander_lm_10 TAWAb1 singlenode $input $spec

spec="code/scripts/specs/santander_spec_eqh10.json"
run santander_lm ULAb1 singlenode $input $spec
run santander_lm_2 ULAb1 singlenode $input $spec
run santander_lm_3 ULAb1 singlenode $input $spec
run santander_lm_4 ULAb1 singlenode $input $spec
run santander_lm_5 ULAb1 singlenode $input $spec
run santander_lm_6 ULAb1 singlenode $input $spec
run santander_lm_7 ULAb1 singlenode $input $spec
run santander_lm_8 ULAb1 singlenode $input $spec
run santander_lm_9 ULAb1 singlenode $input $spec
run santander_lm_10 ULAb1 singlenode $input $spec

run santander_lm TCLAb1 singlenode $input $spec
run santander_lm_2 TCLAb1 singlenode $input $spec
run santander_lm_3 TCLAb1 singlenode $input $spec
run santander_lm_4 TCLAb1 singlenode $input $spec
run santander_lm_5 TCLAb1 singlenode $input $spec
run santander_lm_6 TCLAb1 singlenode $input $spec
run santander_lm_7 TCLAb1 singlenode $input $spec
run santander_lm_8 TCLAb1 singlenode $input $spec
run santander_lm_9 TCLAb1 singlenode $input $spec
run santander_lm_10 TCLAb1 singlenode $input $spec

run santander_lm TAWAb1 singlenode $input $spec
run santander_lm_2 TAWAb1 singlenode $input $spec
run santander_lm_3 TAWAb1 singlenode $input $spec
run santander_lm_4 TAWAb1 singlenode $input $spec
run santander_lm_5 TAWAb1 singlenode $input $spec
run santander_lm_6 TAWAb1 singlenode $input $spec
run santander_lm_7 TAWAb1 singlenode $input $spec
run santander_lm_8 TAWAb1 singlenode $input $spec
run santander_lm_9 TAWAb1 singlenode $input $spec
run santander_lm_10 TAWAb1 singlenode $input $spec

spec="code/scripts/specs/santander_spec_eqh50.json"
run santander_lm ULAb1 singlenode $input $spec
run santander_lm_2 ULAb1 singlenode $input $spec
run santander_lm_3 ULAb1 singlenode $input $spec
run santander_lm_4 ULAb1 singlenode $input $spec
run santander_lm_5 ULAb1 singlenode $input $spec
run santander_lm_6 ULAb1 singlenode $input $spec
run santander_lm_7 ULAb1 singlenode $input $spec
run santander_lm_8 ULAb1 singlenode $input $spec
run santander_lm_9 ULAb1 singlenode $input $spec
run santander_lm_10 ULAb1 singlenode $input $spec

run santander_lm TCLAb1 singlenode $input $spec
run santander_lm_2 TCLAb1 singlenode $input $spec
run santander_lm_3 TCLAb1 singlenode $input $spec
run santander_lm_4 TCLAb1 singlenode $input $spec
run santander_lm_5 TCLAb1 singlenode $input $spec
run santander_lm_6 TCLAb1 singlenode $input $spec
run santander_lm_7 TCLAb1 singlenode $input $spec
run santander_lm_8 TCLAb1 singlenode $input $spec
run santander_lm_9 TCLAb1 singlenode $input $spec
run santander_lm_10 TCLAb1 singlenode $input $spec

run santander_lm TAWAb1 singlenode $input $spec
run santander_lm_2 TAWAb1 singlenode $input $spec
run santander_lm_3 TAWAb1 singlenode $input $spec
run santander_lm_4 TAWAb1 singlenode $input $spec
run santander_lm_5 TAWAb1 singlenode $input $spec
run santander_lm_6 TAWAb1 singlenode $input $spec
run santander_lm_7 TAWAb1 singlenode $input $spec
run santander_lm_8 TAWAb1 singlenode $input $spec
run santander_lm_9 TAWAb1 singlenode $input $spec
run santander_lm_10 TAWAb1 singlenode $input $spec

spec="code/scripts/specs/santander_spec_eqh100.json"
run santander_lm ULAb1 singlenode $input $spec
run santander_lm_2 ULAb1 singlenode $input $spec
run santander_lm_3 ULAb1 singlenode $input $spec
run santander_lm_4 ULAb1 singlenode $input $spec
run santander_lm_5 ULAb1 singlenode $input $spec
run santander_lm_6 ULAb1 singlenode $input $spec
run santander_lm_7 ULAb1 singlenode $input $spec
run santander_lm_8 ULAb1 singlenode $input $spec
run santander_lm_9 ULAb1 singlenode $input $spec
run santander_lm_10 ULAb1 singlenode $input $spec

run santander_lm TCLAb1 singlenode $input $spec
run santander_lm_2 TCLAb1 singlenode $input $spec
run santander_lm_3 TCLAb1 singlenode $input $spec
run santander_lm_4 TCLAb1 singlenode $input $spec
run santander_lm_5 TCLAb1 singlenode $input $spec
run santander_lm_6 TCLAb1 singlenode $input $spec
run santander_lm_7 TCLAb1 singlenode $input $spec
run santander_lm_8 TCLAb1 singlenode $input $spec
run santander_lm_9 TCLAb1 singlenode $input $spec
run santander_lm_10 TCLAb1 singlenode $input $spec

run santander_lm TAWAb1 singlenode $input $spec
run santander_lm_2 TAWAb1 singlenode $input $spec
run santander_lm_3 TAWAb1 singlenode $input $spec
run santander_lm_4 TAWAb1 singlenode $input $spec
run santander_lm_5 TAWAb1 singlenode $input $spec
run santander_lm_6 TAWAb1 singlenode $input $spec
run santander_lm_7 TAWAb1 singlenode $input $spec
run santander_lm_8 TAWAb1 singlenode $input $spec
run santander_lm_9 TAWAb1 singlenode $input $spec
run santander_lm_10 TAWAb1 singlenode $input $spec

spec="code/scripts/specs/santander_spec_eqh255.json"
run santander_lm ULAb1 singlenode $input $spec
run santander_lm_2 ULAb1 singlenode $input $spec
run santander_lm_3 ULAb1 singlenode $input $spec
run santander_lm_4 ULAb1 singlenode $input $spec
run santander_lm_5 ULAb1 singlenode $input $spec
run santander_lm_6 ULAb1 singlenode $input $spec
run santander_lm_7 ULAb1 singlenode $input $spec
run santander_lm_8 ULAb1 singlenode $input $spec
run santander_lm_9 ULAb1 singlenode $input $spec
run santander_lm_10 ULAb1 singlenode $input $spec

run santander_lm TCLAb1 singlenode $input $spec
run santander_lm_2 TCLAb1 singlenode $input $spec
run santander_lm_3 TCLAb1 singlenode $input $spec
run santander_lm_4 TCLAb1 singlenode $input $spec
run santander_lm_5 TCLAb1 singlenode $input $spec
run santander_lm_6 TCLAb1 singlenode $input $spec
run santander_lm_7 TCLAb1 singlenode $input $spec
run santander_lm_8 TCLAb1 singlenode $input $spec
run santander_lm_9 TCLAb1 singlenode $input $spec
run santander_lm_10 TCLAb1 singlenode $input $spec

run santander_lm TAWAb1 singlenode $input $spec
run santander_lm_2 TAWAb1 singlenode $input $spec
run santander_lm_3 TAWAb1 singlenode $input $spec
run santander_lm_4 TAWAb1 singlenode $input $spec
run santander_lm_5 TAWAb1 singlenode $input $spec
run santander_lm_6 TAWAb1 singlenode $input $spec
run santander_lm_7 TAWAb1 singlenode $input $spec
run santander_lm_8 TAWAb1 singlenode $input $spec
run santander_lm_9 TAWAb1 singlenode $input $spec
run santander_lm_10 TAWAb1 singlenode $input $spec
