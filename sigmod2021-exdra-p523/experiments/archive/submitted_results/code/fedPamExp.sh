#/bin/bash

source parameters.sh

date +%T

address=(${address[@]})
ports=(${ports[@]})
networks=(${networks[@]})

for conf in $confs; do

    ## Startup workers and create data if nessesary
    echo "Starting Workers."
    for index in ${!address[*]}; do
        if [ "${address[$index]}" == "localhost" ]; then
            ./code/startWorker.sh ${ports[$index]} "$conf" &
        else
            ssh ${address[$index]} " cd ${remoteDir}; ./code/startWorker.sh ${ports[$index]}" "$conf" &
        fi
    done
    wait

    for netP in ${!networks[*]}; do
        n=${networks[$netP]}

        d="mnist"
        for index in ${!address[*]}; do
            numWorkers=$((index + 1))
            if ((numWorkers == 2)); then
                logstart="results/fed${numWorkers}"
                mkdir -p $logstart
                printf "%s\t %s" "fed ${numWorkers}W ${conf} - $n" " $d Dataset - rep:"
                fullLogname="$logstart/${n}_${d}_${HOSTNAME}_${conf}.log"
                if [ "$n" == "TwoNN" ] || [ "$n" == "CNN" ] || [ "$n" == "TwoNN_forced2" ]; then
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
                                features="data/fed_${d}_features_${numWorkers}.json" \
                                labels="data/fed_${d}_labels_${numWorkers}.json" \
                                ;} >>$fullLogname 2>&1
                        done
                    fi
                fi
                printf "\n"
            fi
        done
    done

    ## Close workers
    for index in ${!address[*]}; do
        if [ "${address[$index]}" != "localhost" ]; then
            ssh ${address[$index]} " cd ${remoteDir}; ./code/stopWorker.sh" &
        fi
    done
    ./code/stopWorker.sh
    wait
    sleep 3

done
