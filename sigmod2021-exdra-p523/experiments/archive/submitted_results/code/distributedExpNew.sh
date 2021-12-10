#/bin/bash

source parameters.sh

date +%T

for conf in $confs; do

    source parameters.sh


    
    address=(${address[@]})


    sleep 4

    ports=(${ports[@]})

    
    ## Startup workers and create data if nessesary
    echo "Starting Workers."
    for index in ${!address[*]}; do
        if [ "${address[$index]}" == "localhost" ]; then
            ./code/startWorker.sh ${ports[$index]} $conf &
        else
            ssh ${address[$index]} " cd ${remoteDir}; ./code/startWorker.sh ${ports[$index]}" $conf &
        fi
    done
    wait
    sleep 4


    if [ "$HOSTNAME" = "XPS-15-7590" ]; then
        echo "Overwrite XPS"
        address=("localhost localhost localhost localhost localhost localhost localhost")
        # address=("localhost")
        # address=(${address[@]})
    fi

    address=(${address[@]})

    d="siemens"
    for index in ${!address[*]}; do
        numWorkers=$((index + 1))
        if ((numWorkers > 0)); then
            logstart="results/fed${numWorkers}"
            mkdir -p $logstart
            for x in $Algs; do
                printf "%s\t %s" "fed ${numWorkers}W $conf - $x" " ${UnsupervisedD} $conf Dataset - rep:"
                fullLogname="$logstart/${x}_${UnsupervisedD}_${HOSTNAME}_$conf.log"
                if [[ "$clear" -eq 1 ]]; then
                    rm -f $fullLogname
                fi
                if [[ -f "$fullLogname" ]] && [[ "$clear" -eq 0 ]]; then
                    printf "%s" " --skip-- "
                else
                    for run in $(eval echo {1..$rep}); do
                        printf "."
                        { time -p systemds \
                            code/exp/$x.dml \
                            -stats 100 \
                            -debug \
                            -config code/conf/$conf.xml \
                            -args "data/fed_${UnsupervisedD}_features_${numWorkers}.json" \
                            FALSE \
                            "tmp/fed_${UnsupervisedD}_${numWorkers}.res" \
                            ;} >>$fullLogname 2>&1
                    done
                fi
                printf "\n"
            done
            for x in $SAlgs; do
                printf "%s\t %s" "fed ${numWorkers}W ${conf} - $x" " ${SupervisedD} $conf  Dataset - rep:"
                fullLogname="$logstart/${x}_${SupervisedD}_${HOSTNAME}_$conf.log"
                if [[ "$clear" -eq 1 ]]; then
                    rm -f $fullLogname
                fi
                if [[ -f "$fullLogname" ]] && [[ "$clear" -eq 0 ]]; then
                    printf "%s" " --skip-- "
                else
                    for run in $(eval echo {1..$rep}); do
                        printf "."
                        { time -p systemds \
                            code/exp/$x.dml \
                            -stats 100 \
                            -debug \
                            -config code/conf/$conf.xml \
                            -args \
                            "data/fed_${SupervisedD}_features_${numWorkers}.json" \
                            "data/${SupervisedD}_labels.data" \
                            FALSE \
                            "tmp/$x-$SupervisedD.res" \
                            ;} >>$fullLogname 2>&1
                            # "data/fed_${SupervisedD}_labels_${numWorkers}.json" \
                    done
                fi

                printf "\n"
            done

            for netP in ${!networks[*]}; do
                n=${networks[$netP]}
                if [[ $n == "CNN" ]]; then
                    prevD=$SupervisedD
                    SupervisedD="mnist"
                    X_test="data/mnist_test_features.data"
                    y_test="data/mnist_test_labels.data"

                fi
                logstart="results/fed${numWorkers}"
                mkdir -p $logstart
                printf "%s\t %s" "fed ${numWorkers}W ${conf} - $n" " ${SupervisedD} Dataset - rep:"
                fullLogname="$logstart/${n}_${SupervisedD}_${HOSTNAME}_${conf}.log"
                if [[ "$clear" -eq 1 ]]; then
                    rm -f $fullLogname
                fi
                if [[ -f "$fullLogname" ]] && [[ "$clear" -eq 0 ]]; then
                    printf "%s" " --skip-- "
                else
                    for run in $(eval echo {1..$rep}); do
                        printf "."
                        { time -p systemds \
                            code/exp/$n.dml \
                            -stats 100 -debug \
                            -config code/conf/$conf.xml \
                            -nvargs \
                            X_test=$X_test \
                            y_test=$y_test \
                            epochs=${epochs[$netP]} \
                            batch_size=${batch_size[$netP]} \
                            eta=${eta[$netP]} \
                            utype=$utype \
                            freq=$freq \
                            channels=$channels \
                            hin=$hin \
                            win=$win \
                            numWorkers=$numWorkersNN \
                            features="data/fed_${SupervisedD}_features_${numWorkers}.json" \
                            labels="data/fed_${SupervisedD}_labels_${numWorkers}.json" \
                            ;} >>$fullLogname 2>&1
                    done
                fi
                printf "\n"
                if [[ $n == "CNN" ]]; then
                    SupervisedD=$prevD
                    X_test="data/P2P_features.data"
                    y_test="data/P2P_labels.data"
                fi

            done
        fi
    done

    if [ "$HOSTNAME" = "XPS-15-7590" ]; then
        source parameters.sh
        address=(${address[@]})
    fi

    ## Close workers
    for index in ${!address[*]}; do
        if [ "${address[$index]}" != "localhost" ]; then
            ssh ${address[$index]} " cd ${remoteDir}; ./code/stopWorker.sh" &
        fi
    done
    ./code/stopWorker.sh
    wait
done
