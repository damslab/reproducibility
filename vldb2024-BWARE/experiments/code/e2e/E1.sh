# Read Compressed matrix vs read binary matrix into algrotihm

logstart="results/e2e"
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"

echo "code/e2e/E1.sh"

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
    profile="$logDir/perf/$lname.html"
    IFS=" "
    echo $log $alg $conf $mode
    export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/lib/libasyncProfiler.so=start,event=cpu,file=$profile"

    rm -fr $log

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
}

spec="code/scripts/specs/criteo_full.json"

input="data/criteo/day_0_1000.tsv"

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec

input="data/criteo/day_0_10000.tsv"

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec

input="data/criteo/day_0_100000.tsv"

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec

input="data/criteo/day_0_300000.tsv"

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec

input="data/criteo/day_0_1000000.tsv"

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec

input="data/criteo/day_0_3000000.tsv"

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec

input="data/criteo/day_0_10000000.tsv"

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec

input="data/criteo/day_0_30000000.tsv"

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec

input="data/criteo/day_0_100000000.tsv"

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec

input="data/criteo/day_0"

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec

