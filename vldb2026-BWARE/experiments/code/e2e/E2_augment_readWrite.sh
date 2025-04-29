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
binary="data/santander/train.bin"
comp="data/santander/train.cla"


spec="code/scripts/specs/santander_pass.json"
run reformat_te ULAb1 singlenode $input $spec $binary "binary"
run reformat_te TCLAb1 singlenode $input $spec $comp "compressed"

run santander_lm_rw ULAb1 singlenode $binary
run santander_lm_rw_2 ULAb1 singlenode $binary
run santander_lm_rw_3 ULAb1 singlenode $binary
run santander_lm_rw_4 ULAb1 singlenode $binary
run santander_lm_rw_5 ULAb1 singlenode $binary
run santander_lm_rw_6 ULAb1 singlenode $binary
run santander_lm_rw_7 ULAb1 singlenode $binary
run santander_lm_rw_8 ULAb1 singlenode $binary
run santander_lm_rw_9 ULAb1 singlenode $binary
run santander_lm_rw_10 ULAb1 singlenode $binary

run santander_lm_rw TCLAb1 singlenode $comp
run santander_lm_rw_2 TCLAb1 singlenode $comp
run santander_lm_rw_3 TCLAb1 singlenode $comp
run santander_lm_rw_4 TCLAb1 singlenode $comp
run santander_lm_rw_5 TCLAb1 singlenode $comp
run santander_lm_rw_6 TCLAb1 singlenode $comp
run santander_lm_rw_7 TCLAb1 singlenode $comp
run santander_lm_rw_8 TCLAb1 singlenode $comp
run santander_lm_rw_9 TCLAb1 singlenode $comp
run santander_lm_rw_10 TCLAb1 singlenode $comp

run santander_lm_rw TAWAb1 singlenode $comp
run santander_lm_rw_2 TAWAb1 singlenode $comp
run santander_lm_rw_3 TAWAb1 singlenode $comp
run santander_lm_rw_4 TAWAb1 singlenode $comp
run santander_lm_rw_5 TAWAb1 singlenode $comp
run santander_lm_rw_6 TAWAb1 singlenode $comp
run santander_lm_rw_7 TAWAb1 singlenode $comp
run santander_lm_rw_8 TAWAb1 singlenode $comp
run santander_lm_rw_9 TAWAb1 singlenode $comp
run santander_lm_rw_10 TAWAb1 singlenode $comp

spec="code/scripts/specs/santander_spec_eqh5.json"
run reformat_te ULAb1 singlenode $input $spec $binary "binary"
run reformat_te TCLAb1 singlenode $input $spec $comp "compressed"

run santander_lm_rw ULAb1 singlenode $binary
run santander_lm_rw_2 ULAb1 singlenode $binary
run santander_lm_rw_3 ULAb1 singlenode $binary
run santander_lm_rw_4 ULAb1 singlenode $binary
run santander_lm_rw_5 ULAb1 singlenode $binary
run santander_lm_rw_6 ULAb1 singlenode $binary
run santander_lm_rw_7 ULAb1 singlenode $binary
run santander_lm_rw_8 ULAb1 singlenode $binary
run santander_lm_rw_9 ULAb1 singlenode $binary
run santander_lm_rw_10 ULAb1 singlenode $binary

run santander_lm_rw TCLAb1 singlenode $comp
run santander_lm_rw_2 TCLAb1 singlenode $comp
run santander_lm_rw_3 TCLAb1 singlenode $comp
run santander_lm_rw_4 TCLAb1 singlenode $comp
run santander_lm_rw_5 TCLAb1 singlenode $comp
run santander_lm_rw_6 TCLAb1 singlenode $comp
run santander_lm_rw_7 TCLAb1 singlenode $comp
run santander_lm_rw_8 TCLAb1 singlenode $comp
run santander_lm_rw_9 TCLAb1 singlenode $comp
run santander_lm_rw_10 TCLAb1 singlenode $comp

run santander_lm_rw TAWAb1 singlenode $comp
run santander_lm_rw_2 TAWAb1 singlenode $comp
run santander_lm_rw_3 TAWAb1 singlenode $comp
run santander_lm_rw_4 TAWAb1 singlenode $comp
run santander_lm_rw_5 TAWAb1 singlenode $comp
run santander_lm_rw_6 TAWAb1 singlenode $comp
run santander_lm_rw_7 TAWAb1 singlenode $comp
run santander_lm_rw_8 TAWAb1 singlenode $comp
run santander_lm_rw_9 TAWAb1 singlenode $comp
run santander_lm_rw_10 TAWAb1 singlenode $comp

spec="code/scripts/specs/santander_spec_eqh10.json"
run reformat_te ULAb1 singlenode $input $spec $binary "binary"
run reformat_te TCLAb1 singlenode $input $spec $comp "compressed"

run santander_lm_rw ULAb1 singlenode $binary
run santander_lm_rw_2 ULAb1 singlenode $binary
run santander_lm_rw_3 ULAb1 singlenode $binary
run santander_lm_rw_4 ULAb1 singlenode $binary
run santander_lm_rw_5 ULAb1 singlenode $binary
run santander_lm_rw_6 ULAb1 singlenode $binary
run santander_lm_rw_7 ULAb1 singlenode $binary
run santander_lm_rw_8 ULAb1 singlenode $binary
run santander_lm_rw_9 ULAb1 singlenode $binary
run santander_lm_rw_10 ULAb1 singlenode $binary

run santander_lm_rw TCLAb1 singlenode $comp
run santander_lm_rw_2 TCLAb1 singlenode $comp
run santander_lm_rw_3 TCLAb1 singlenode $comp
run santander_lm_rw_4 TCLAb1 singlenode $comp
run santander_lm_rw_5 TCLAb1 singlenode $comp
run santander_lm_rw_6 TCLAb1 singlenode $comp
run santander_lm_rw_7 TCLAb1 singlenode $comp
run santander_lm_rw_8 TCLAb1 singlenode $comp
run santander_lm_rw_9 TCLAb1 singlenode $comp
run santander_lm_rw_10 TCLAb1 singlenode $comp

run santander_lm_rw TAWAb1 singlenode $comp
run santander_lm_rw_2 TAWAb1 singlenode $comp
run santander_lm_rw_3 TAWAb1 singlenode $comp
run santander_lm_rw_4 TAWAb1 singlenode $comp
run santander_lm_rw_5 TAWAb1 singlenode $comp
run santander_lm_rw_6 TAWAb1 singlenode $comp
run santander_lm_rw_7 TAWAb1 singlenode $comp
run santander_lm_rw_8 TAWAb1 singlenode $comp
run santander_lm_rw_9 TAWAb1 singlenode $comp
run santander_lm_rw_10 TAWAb1 singlenode $comp

spec="code/scripts/specs/santander_spec_eqh50.json"
run reformat_te ULAb1 singlenode $input $spec $binary "binary"
run reformat_te TCLAb1 singlenode $input $spec $comp "compressed"

run santander_lm_rw ULAb1 singlenode $binary
run santander_lm_rw_2 ULAb1 singlenode $binary
run santander_lm_rw_3 ULAb1 singlenode $binary
run santander_lm_rw_4 ULAb1 singlenode $binary
run santander_lm_rw_5 ULAb1 singlenode $binary
run santander_lm_rw_6 ULAb1 singlenode $binary
run santander_lm_rw_7 ULAb1 singlenode $binary
run santander_lm_rw_8 ULAb1 singlenode $binary
run santander_lm_rw_9 ULAb1 singlenode $binary
run santander_lm_rw_10 ULAb1 singlenode $binary

run santander_lm_rw TCLAb1 singlenode $comp
run santander_lm_rw_2 TCLAb1 singlenode $comp
run santander_lm_rw_3 TCLAb1 singlenode $comp
run santander_lm_rw_4 TCLAb1 singlenode $comp
run santander_lm_rw_5 TCLAb1 singlenode $comp
run santander_lm_rw_6 TCLAb1 singlenode $comp
run santander_lm_rw_7 TCLAb1 singlenode $comp
run santander_lm_rw_8 TCLAb1 singlenode $comp
run santander_lm_rw_9 TCLAb1 singlenode $comp
run santander_lm_rw_10 TCLAb1 singlenode $comp

run santander_lm_rw TAWAb1 singlenode $comp
run santander_lm_rw_2 TAWAb1 singlenode $comp
run santander_lm_rw_3 TAWAb1 singlenode $comp
run santander_lm_rw_4 TAWAb1 singlenode $comp
run santander_lm_rw_5 TAWAb1 singlenode $comp
run santander_lm_rw_6 TAWAb1 singlenode $comp
run santander_lm_rw_7 TAWAb1 singlenode $comp
run santander_lm_rw_8 TAWAb1 singlenode $comp
run santander_lm_rw_9 TAWAb1 singlenode $comp
run santander_lm_rw_10 TAWAb1 singlenode $comp

spec="code/scripts/specs/santander_spec_eqh100.json"
run reformat_te ULAb1 singlenode $input $spec $binary "binary"
run reformat_te TCLAb1 singlenode $input $spec $comp "compressed"

run santander_lm_rw ULAb1 singlenode $binary
run santander_lm_rw_2 ULAb1 singlenode $binary
run santander_lm_rw_3 ULAb1 singlenode $binary
run santander_lm_rw_4 ULAb1 singlenode $binary
run santander_lm_rw_5 ULAb1 singlenode $binary
run santander_lm_rw_6 ULAb1 singlenode $binary
run santander_lm_rw_7 ULAb1 singlenode $binary
run santander_lm_rw_8 ULAb1 singlenode $binary
run santander_lm_rw_9 ULAb1 singlenode $binary
run santander_lm_rw_10 ULAb1 singlenode $binary

run santander_lm_rw TCLAb1 singlenode $comp
run santander_lm_rw_2 TCLAb1 singlenode $comp
run santander_lm_rw_3 TCLAb1 singlenode $comp
run santander_lm_rw_4 TCLAb1 singlenode $comp
run santander_lm_rw_5 TCLAb1 singlenode $comp
run santander_lm_rw_6 TCLAb1 singlenode $comp
run santander_lm_rw_7 TCLAb1 singlenode $comp
run santander_lm_rw_8 TCLAb1 singlenode $comp
run santander_lm_rw_9 TCLAb1 singlenode $comp
run santander_lm_rw_10 TCLAb1 singlenode $comp

run santander_lm_rw TAWAb1 singlenode $comp
run santander_lm_rw_2 TAWAb1 singlenode $comp
run santander_lm_rw_3 TAWAb1 singlenode $comp
run santander_lm_rw_4 TAWAb1 singlenode $comp
run santander_lm_rw_5 TAWAb1 singlenode $comp
run santander_lm_rw_6 TAWAb1 singlenode $comp
run santander_lm_rw_7 TAWAb1 singlenode $comp
run santander_lm_rw_8 TAWAb1 singlenode $comp
run santander_lm_rw_9 TAWAb1 singlenode $comp
run santander_lm_rw_10 TAWAb1 singlenode $comp

spec="code/scripts/specs/santander_spec_eqh255.json"
run reformat_te ULAb1 singlenode $input $spec $binary "binary"
run reformat_te TCLAb1 singlenode $input $spec $comp "compressed"

run santander_lm_rw ULAb1 singlenode $binary
run santander_lm_rw_2 ULAb1 singlenode $binary
run santander_lm_rw_3 ULAb1 singlenode $binary
run santander_lm_rw_4 ULAb1 singlenode $binary
run santander_lm_rw_5 ULAb1 singlenode $binary
run santander_lm_rw_6 ULAb1 singlenode $binary
run santander_lm_rw_7 ULAb1 singlenode $binary
run santander_lm_rw_8 ULAb1 singlenode $binary
run santander_lm_rw_9 ULAb1 singlenode $binary
run santander_lm_rw_10 ULAb1 singlenode $binary

run santander_lm_rw TCLAb1 singlenode $comp
run santander_lm_rw_2 TCLAb1 singlenode $comp
run santander_lm_rw_3 TCLAb1 singlenode $comp
run santander_lm_rw_4 TCLAb1 singlenode $comp
run santander_lm_rw_5 TCLAb1 singlenode $comp
run santander_lm_rw_6 TCLAb1 singlenode $comp
run santander_lm_rw_7 TCLAb1 singlenode $comp
run santander_lm_rw_8 TCLAb1 singlenode $comp
run santander_lm_rw_9 TCLAb1 singlenode $comp
run santander_lm_rw_10 TCLAb1 singlenode $comp

run santander_lm_rw TAWAb1 singlenode $comp
run santander_lm_rw_2 TAWAb1 singlenode $comp
run santander_lm_rw_3 TAWAb1 singlenode $comp
run santander_lm_rw_4 TAWAb1 singlenode $comp
run santander_lm_rw_5 TAWAb1 singlenode $comp
run santander_lm_rw_6 TAWAb1 singlenode $comp
run santander_lm_rw_7 TAWAb1 singlenode $comp
run santander_lm_rw_8 TAWAb1 singlenode $comp
run santander_lm_rw_9 TAWAb1 singlenode $comp
run santander_lm_rw_10 TAWAb1 singlenode $comp