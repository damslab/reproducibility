#!/bin/bash

# source parameters.sh

logstart="results/algorithms/"

SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"
SYSTEMDS_DISTRIBUTED_OPTS_BASE="$SYSTEMDS_DISTRIBUTED_OPTS"
for d in $data; do
    if [[ "$d" =~ "infimnist" ]]; then
        folder="infimnist"
    elif [[ "$d" =~ "binarymnist" ]]; then
        folder="binarymnist"
    elif [[ "$d" =~ "census" ]]; then
        folder="census"
    else
        folder=$d
    fi

    for x in $algorithms; do
        for y in $techniques; do

            mkdir -p "$logstart/$x/$d/$HOSTNAME/"
            fullLogname="$logstart/$x/$d/$HOSTNAME/$y-hybrid.log"
            if [ ! -f "$fullLogname" ] || [ $clear == 1 ]; then
                rm -f $fullLogname
                for i in $(seq $exrep); do

                    printf "."
                    profile="hprof/$(date +"%Y-%m-%d-%T")-Algorithm-$HOSTNAME-$d-$x-$s-$y-$i.html"
                    # export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/build/libasyncProfiler.so=start,event=cpu,file=$profile"
                    # export SYSTEMDS_DISTRIBUTED_OPTS="$SYSTEMDS_DISTRIBUTED_OPTS_BASE "
                    # export SYSTEMDS_DISTRIBUTED_OPTS="\
                    #      --master yarn \
                    #      --deploy-mode client \
                    #      --driver-memory 110g \
                    #      --driver-cores 5 \
                    #      --conf spark.driver.extraJavaOptions=\"-XX:+UseG1GC -Xms110g -Xmn11g -Dlog4j.configuration=file:$LOG4JPROP\" \
                    #      --conf spark.executor.extraJavaOptions=\"-XX:+UseG1GC -Xms105g -Xmn10g\" \
                    #      --conf spark.executor.heartbeatInterval=10000000s \
                    #      --conf spark.executor.memoryOverhead=10000 \
                    #      --conf spark.yarn.archive=hdfs:///spark/libs/spark-libs.jar \
                    #      --conf spark.task.maxFailures=10 \
                    #      --conf spark.storage.memoryMapThreshold=150m \
                    #      --conf spark.default.parallelism=60 \
                    #      --conf spark.memory.fraction=.4 \
                    #      --files $LOG4JPROP \
                    #      --conf spark.network.timeout=10000001s \
                    #      --num-executors 6 \
                    #      --executor-memory 105g \
                    #      --executor-cores 32 \
                    #      "

                    #0.2 is unbarably slow



                    # Num instance per machine
                    # 32 -1 / 5 = 6

                    # Total executor memory = 105g / num instance per machine
                    # 17500m

                    # spark executprs memory = total executor memory * 0.9
                    # 15750m

                    # memOverhead = total executor memory * 0.1
                    #  1750m

                    # default parallelizm 
                    # executor intances * executor cores * 2 
                    # 6 * 32 * 2 = 384

                    export SYSTEMDS_DISTRIBUTED_OPTS="\
                         --master yarn \
                         --deploy-mode client \
                         --driver-memory 110g \
                         --driver-cores 5 \
                         --conf spark.driver.extraJavaOptions=\"-XX:+UseG1GC -Xms110g -Xmn11g -Dlog4j.configuration=file:$LOG4JPROP -agentpath:$HOME/Programs/profiler/build/libasyncProfiler.so=start,event=cpu,file=$profile\" \
                         --conf spark.executor.extraJavaOptions=\"-XX:+UseG1GC -Xms15g -Xmn175m\" \
                         --conf spark.executor.heartbeatInterval=10000000s \
                         --conf spark.executor.memoryOverhead=5000 \
                         --conf spark.yarn.archive=hdfs:///spark/libs/spark-libs.jar \
                         --conf spark.task.maxFailures=10 \
                         --conf spark.memory.fraction=.3 \
                         --files $LOG4JPROP \
                         --conf spark.network.timeout=10000001s \
                         --num-executors 32 \
                         --executor-memory 15g \
                         --executor-cores 5 \
                         "

                    # spark.memory.fraction.
                    # user.fraction = 1-spark.memory.fraction


                        #  --conf spark.storage.memoryMapThreshold=150m \
                        #  --conf spark.default.parallelism=384 \

                    perf stat -d -d -d \
                        systemds \
                        code/algorithms/$x.dml \
                        -config code/conf/$y.xml \
                        -stats 100 -debug \
                        -exec hybrid \
                        -seed $seed \
                        -args "data/$folder/train_$d.data" \
                        1 \
                        "results/algorithms/$x/$d/$y.csv" \
                        "data/$folder/train_${d}_labels.data" \
                        "data/$folder/test_${folder}.data" \
                        "data/$folder/test_${folder}_labels.data" \
                        >>$fullLogname 2>&1
                        # -explain \

                done

                rm -f $fullLogname.res
                echo "------------------------------------"
                echo "$d-$x-$y -- $HOSTNAME"
                cat $fullLogname | grep -E ' compress  |Total elapsed time| instructions |  cycles  | CPUs utilized ' | tee -a $fullLogname.res
                echo "$d-$x-$y -- $HOSTNAME"
                echo "------------------------------------"
            fi
        done
    done
done

SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"

SYSTEMDS_DISTRIBUTED_OPTS="$SYSTEMDS_DISTRIBUTED_OPTS_BASE"
