#!/bin/bash

source parameters.sh

export SYSDS_DISTRIBUTED=1
export SYSDS_DISTRIBUTED=0

logstart="results/algorithms/"

SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"
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
        #     for y in $techniques; do

        #         mkdir -p "$logstart/$x/$d/$HOSTNAME/"
        #         fullLogname="$logstart/$x/$d/$HOSTNAME/$y-hybrid-csv.log"
        #         if [ ! -f "$fullLogname" ] || [ $clear == 1 ]; then
        #             rm -f $fullLogname
        #             if [ $sysds == 1 ]; then
        #                 source loadSysDSSettings.sh
        #                 for i in $(seq $exrep); do
        #                     profile="hprof/$(date +"%Y-%m-%d-%T")-Alg-csv-$HOSTNAME-$d-$x-$y-$i.html"
        #                     export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/build/libasyncProfiler.so=start,event=cpu,file=$profile"
        #                     printf "."
        #                     perf stat -d -d -d \
        #                         systemds \
        #                         code/algorithms/${x}ml.dml \
        #                         -config code/conf/$y.xml \
        #                         -stats 100 -debug \
        #                         -exec hybrid \
        #                         -seed $seed \
        #                          -args "data/$folder/train_$d.csv" \
        #                         1 \
        #                         "results/algorithms/$x/$d/$y.csv" \
        #                         "data/$folder/train_${d}_labels.csv" \
        #                         "data/$folder/test_${folder}.csv" \
        #                         "data/$folder/test_${folder}_labels.csv" \
        #                         >>$fullLogname 2>&1

        #                 done

        #                 rm -f $fullLogname.res
        #                 echo "------------------------------------"
        #                 echo "$d-$x-$y -- $HOSTNAME"
        #                 cat $fullLogname | grep -E ' compress  |Total elapsed time| instructions |  cycles  | CPUs utilized ' | tee -a $fullLogname.res
        #                 echo "$d-$x-$y -- $HOSTNAME"
        #                 echo "------------------------------------"
        #             fi
        #         fi
        #     done

            mkdir -p "$logstart/$x/$d/$HOSTNAME/"
        # for y in $sysmltechniques; do

            # fullLognamesysml="$logstart/$x/$d/$HOSTNAME/$y-hybrid-sysml.log"

            # if [ ! -f "$fullLognamesysml" ] || [ $clear == 1 ]; then
            #     if [ $sysml == 1 ]; then

            #         source loadSysMLSettings.sh
            #         rm -f $fullLognamesysml
            #         for i in $(seq $exrep); do
            #             printf "."
            #             profile="hprof/$(date +"%Y-%m-%d-%T")-Alg-SYSML-$HOSTNAME-$d-$x-$y-$i.html"
            #             export SYSTEMML_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/build/libasyncProfiler.so=start,event=cpu,file=$profile"

            #             perf stat -d -d -d \
            #                 java ${SYSTEMML_STANDALONE_OPTS} \
            #                 -cp ${sysmlClassPath} \
            #                 -Dlog4j.configuration=file:${LOG4JPROP_SYSML} \
            #                 org.apache.sysml.api.DMLScript \
            #                 -f code/algorithms/${x}ml.dml \
            #                 -config code/conf/$y.xml \
            #                 -stats 100 \
            #                 -exec hybrid \
            #                 -args "data/$folder/train_$d.csv" \
            #                 1 \
            #                 "results/algorithms/$x/$d/$y-sysml.csv" \
            #                 "data/$folder/train_${d}_labels.csv" \
            #                 "data/$folder/test_${folder}.csv" \
            #                 "data/$folder/test_${folder}_labels.csv" \
            #                 >>$fullLognamesysml 2>&1

            #         done
            #         echo "------------------------------------"
            #         rm -f $fullLognamesysml.res
            #         echo "$HOSTNAME - $d-$x-$s-$y"
            #         cat $fullLognamesysml.spark | grep -E 'compress |Total elapsed time| instructions | cycles  | CPUs utilized ' | tee -a $fullLognamesysml.res
            #         echo "$HOSTNAME - $d-$x-$s-$y"
            #         echo "------------------------------------"
            #     fi
            # fi

            # ULA ULA ULA ULA

            # fullLognamesysml="$logstart/$x/$d/$HOSTNAME/ula-hybrid-sysml-spark.log"

            # if [ ! -f "$fullLognamesysml" ] || [ $clear == 1 ]; then
            #     if [ $sysml == 1 ]; then

            #         source loadSysMLSettings.sh
            #         rm -f $fullLognamesysml
            #         for i in $(seq $exrep); do
            #             printf "."
            #             profile="hprof/$(date +"%Y-%m-%d-%T")-Alg-SYSML-$HOSTNAME-$d-$x-ula-$i.html"
            #             export SYSTEMML_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/build/libasyncProfiler.so=start,event=cpu,file=$profile"

            #             perf stat -d -d -d \
            #                 spark-submit \
            #                 --master yarn \
            #                 --deploy-mode client \
            #                 --driver-memory 110g \
            #                 --conf spark.driver.extraJavaOptions="-Xms110g -Xmn11g" \
            #                 --conf spark.executor.heartbeatInterval=100s \
            #                 --conf spark.network.timeout=512s \
            #                 --num-executors 6 \
            #                 --executor-memory 105g \
            #                 --executor-cores 32 \
            #                 $HOME/github/systemml/target/SystemML.jar \
            #                 -f code/algorithms/${x}ml.dml \
            #                 -config code/conf/sysmlb16.xml \
            #                 -stats 100 \
            #                 -args "data/census/train_census_enc_sysML_128x.data" \
            #                 1 \
            #                 "results/algorithms/$x/$d/ula-sysml-spark.csv" \
            #                 "data/census/train_census_enc_sysML_128x_labels.data" \
            #                 "data/census/test_census.csv" \
            #                 "data/census/test_census_labels.csv" \
            #                 >>$fullLognamesysml 2>&1

            #                 # -exec hybrid \
            #                 # --files $LOG4JPROP_SYSML \
            #                 # --conf spark.driver.extraJavaOptions="-Xms110g -Xmn11g -Dlog4j.configuration=file:$LOG4JPROP_SYSML" \
            #                 # --conf spark.executor.extraJavaOptions="-Dlog4j.configuration=file:$LOG4JPROP_SYSML" \
            #                 # -cp ${sysmlClassPath} \
            #         done

            #         echo "------------------------------------"
            #         rm -f $fullLognamesysml.res
            #         echo "$HOSTNAME - $d-$x-$s-ula"
            #         cat $fullLognamesysml | grep -E 'compress |Total elapsed time| instructions | cycles  | CPUs utilized ' | tee -a $fullLognamesysml.res
            #         echo "$HOSTNAME - $d-$x-$s-ula"
            #         echo "------------------------------------"
            #     fi
            # fi


            fullLognamesysml="$logstart/$x/$d/$HOSTNAME/cla-hybrid-sysml-spark.log"

            if [ ! -f "$fullLognamesysml" ] || [ $clear == 1 ]; then
                if [ $sysml == 1 ]; then

                    source loadSysMLSettings.sh
                    rm -f $fullLognamesysml
                    for i in $(seq $exrep); do
                        printf "."
                        profile="hprof/$(date +"%Y-%m-%d-%T")-Alg-SYSML-$HOSTNAME-$d-$x-cla-$i.html"
                        export SYSTEMML_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/build/libasyncProfiler.so=start,event=cpu,file=$profile"

                        perf stat -d -d -d \
                            spark-submit \
                            --master yarn \
                            --deploy-mode client \
                            --driver-memory 110g \
                            --conf spark.driver.extraJavaOptions="-Xms110g -Xmn11g" \
                            --conf spark.executor.heartbeatInterval=100s \
                            --conf spark.network.timeout=512s \
                            --num-executors 6 \
                            --executor-memory 105g \
                            --executor-cores 32 \
                            $HOME/github/systemml/target/SystemML.jar \
                            -f code/algorithms/${x}ml.dml \
                            -config code/conf/cla-sysmlb16.xml \
                            -stats 100 \
                            -args "data/census/train_census_enc_sysML_128x.data" \
                            1 \
                            "results/algorithms/$x/$d/cla-sysml-spark.csv" \
                            "data/census/train_census_enc_sysML_128x_labels.data" \
                            "data/census/test_census.csv" \
                            "data/census/test_census_labels.csv" \
                            >>$fullLognamesysml 2>&1

                            # -exec hybrid \
                            # --files $LOG4JPROP_SYSML \
                            # --conf spark.driver.extraJavaOptions="-Xms110g -Xmn11g -Dlog4j.configuration=file:$LOG4JPROP_SYSML" \
                            # --conf spark.executor.extraJavaOptions="-Dlog4j.configuration=file:$LOG4JPROP_SYSML" \
                            # -cp ${sysmlClassPath} \
                    done

                    echo "------------------------------------"
                    rm -f $fullLognamesysml.res
                    echo "$HOSTNAME - $d-$x-$s-cla"
                    cat $fullLognamesysml | grep -E 'compress |Total elapsed time| instructions | cycles  | CPUs utilized ' | tee -a $fullLognamesysml.res
                    echo "$HOSTNAME - $d-$x-$s-cla"
                    echo "------------------------------------"
                fi
            fi
        # done
    done
done

SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"
