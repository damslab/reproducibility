# Read Compressed matrix vs read binary matrix into algrotihm

logstart="results/e2e"
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"
SYSTEMDS_DISTRIBUTED_OPTS_BASE="$SYSTEMDS_DISTRIBUTED_OPTS"

echo "running:  code/e2e/E3_distributed.sh"

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
    
    export SYSTEMDS_DISTRIBUTED_OPTS="\
			--master yarn \
			--deploy-mode client \
			--driver-memory 200g \
			--conf spark.driver.extraJavaOptions=\"\
				-Xms200g -Xmn100g -Dlog4j.configuration=file:$LOG4JPROP				-agentpath:$HOME/Programs/profiler/lib/libasyncProfiler.so=start,event=cpu,file=$profile				\" \
			--conf spark.executor.extraJavaOptions=\"-Dlog4j.configuration=file:$LOG4JPROP\" \
			--conf spark.executor.heartbeatInterval=100s \
			--files $LOG4JPROP \
			--conf spark.network.timeout=512s \
			--num-executors 8 \
			--executor-memory 200g \
			--executor-cores 48 \
		"

    rm -fr $log

    echo $SYSTEMDS_DISTRIBUTED_OPTS >>$log

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
    export SYSTEMDS_DISTRIBUTED_OPTS="$SYSTEMDS_DISTRIBUTED_OPTS_BASE"
}

export SYSDS_DISTRIBUTED=0


spec="code/scripts/specs/criteo_full.json"

run criteo_kmeans_dist ULAb1 hybrid data/criteo/day_0.bin $spec

