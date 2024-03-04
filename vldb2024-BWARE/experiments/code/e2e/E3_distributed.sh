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

export SYSDS_DISTRIBUTED=1


# run criteo_writePreprocessed ULAb1 hybrid $input $spec tmp/test.csv
# run criteo_writePreprocessed ULAb1 hybrid $input $spec tmp/X.csv tmp/y.csv binary

# run criteo_writeSchema ULAb1 hybrid $input tmp/data.csv binary

# run criteo_writeSchema ULAb1 hybrid data/criteo/day_0_1000000.tsv data/criteo/day_0_1m.bin binary
# run criteo_writeSchema ULAb1 spark data/criteo/day_0_1000000.tsv data/criteo/day_0_1m.bin binary

# run criteo_writeSchema ULAb1 hybrid data/criteo/day_23 data/criteo/day_23.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/day_0 data/criteo/day_0.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_1 data/criteo/days_1_1.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_2 data/criteo/days_1_2.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_3 data/criteo/days_1_3.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_4 data/criteo/days_1_4.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_5 data/criteo/days_1_5.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_6 data/criteo/days_1_6.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_7 data/criteo/days_1_7.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_8 data/criteo/days_1_8.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_9 data/criteo/days_1_9.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_10 data/criteo/days_1_10.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_11 data/criteo/days_1_11.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_12 data/criteo/days_1_12.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_13 data/criteo/days_1_13.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_14 data/criteo/days_1_14.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_15 data/criteo/days_1_15.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_16 data/criteo/days_1_16.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_17 data/criteo/days_1_17.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_18 data/criteo/days_1_18.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_19 data/criteo/days_1_19.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_20 data/criteo/days_1_20.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_21 data/criteo/days_1_21.bin binary
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_22 data/criteo/days_1_22.bin binary

# test="data/criteo/day_23.bin"
spec="code/scripts/specs/criteo_full.json"

# run criteo_kmeans_dist ULAb1 hybrid data/criteo/day_0_10000.tsv $spec
run criteo_kmeans_dist ULAb1 hybrid data/criteo/day_0_10000000.tsv $spec
# run criteo_kmeans_dist TAWAb1 hybrid data/criteo/day_0_10000000.tsv $spec

# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_1.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_2.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_3.bin $spec 
# run criteo_kmeans_dist TAWAb1 hybrid data/criteo/days_1_1.bin $spec 
# run criteo_kmeans_dist TAWAb1 hybrid data/criteo/days_1_2.bin $spec 
# run criteo_kmeans_dist TAWAb1 hybrid data/criteo/days_1_3.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_4.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_6.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_7.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_8.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_9.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_10.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_11.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_12.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_13.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_14.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_15.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_16.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_17.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_18.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_19.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_20.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_21.bin $spec 
# run criteo_kmeans_dist ULAb1 hybrid data/criteo/days_1_22.bin $spec 



## DO NOT RUN THE COMPRESSED IT FILLS UP THE DISTRIBUTED HDFS DISK!!!!
# run criteo_writeSchema ULAb1 hybrid data/criteo/day_0.bin data/criteo/day_0.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_1.bin data/criteo/days_1_1.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_2.bin data/criteo/days_1_2.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_3.bin data/criteo/days_1_3.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_4.bin data/criteo/days_1_4.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_5.bin data/criteo/days_1_5.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_6.bin data/criteo/days_1_6.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_7.bin data/criteo/days_1_7.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_8.bin data/criteo/days_1_8.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_9.bin data/criteo/days_1_9.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_10.bin data/criteo/days_1_10.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_11.bin data/criteo/days_1_11.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_12.bin data/criteo/days_1_12.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_13.bin data/criteo/days_1_13.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_14.bin data/criteo/days_1_14.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_15.bin data/criteo/days_1_15.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_16.bin data/criteo/days_1_16.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_17.bin data/criteo/days_1_17.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_18.bin data/criteo/days_1_18.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_19.bin data/criteo/days_1_19.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_20.bin data/criteo/days_1_20.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_21.bin data/criteo/days_1_21.cla compressed
# run criteo_writeSchema ULAb1 hybrid data/criteo/days_1_22.bin data/criteo/days_1_22.cla compressed
