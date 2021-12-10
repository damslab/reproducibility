#/bin/bash

source parameters.sh

source code/util/gitIdLog.sh


X_test="data/P2_features.data"
y_test="data/P2_labels.data"

eta=(0.01)
utype="BSP"
freq="EPOCH"
channels=1
hin=28
win=28
numWorkersNN=1

logGitIDs

date +%T
logstart="results/loc"

mkdir -p $logstart

for conf in $confs; do
    ## Unsupervised algorithms
    for x in $Algs; do
        printf "%s\t %s" "loc $conf - $x" " ${UnsupervisedD} - rep:"
        fullLogname="$logstart/${x}_${UnsupervisedD}_${HOSTNAME}_${conf}.log"
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
                    -stats \
                    -debug \
                    -config code/conf/$conf.xml \
                    -args "data/${UnsupervisedD}_features.data" \
                    FALSE \
                    "tmp/$x-$UnsupervisedD.res" \
                    ; } >>$fullLogname 2>&1
                # TRUE \
            done
        fi
        printf "\n"
    done
    ## Supervised algorithms
    for x in $SAlgs; do
        printf "%s\t %s" "loc ${conf} - $x" " $SupervisedD - rep:"
        fullLogname="$logstart/${x}_${SupervisedD}_${HOSTNAME}_${conf}.log"
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
                    "data/${SupervisedD}_features.data" \
                    "data/${SupervisedD}_labels.data" \
                    FALSE \
                    "tmp/$x-$SupervisedD.res" \
                    ; } >>$fullLogname 2>&1
            done
        fi

        printf "\n"
    done

    ## Neural networks
    networks=(${networks[@]})
    for netP in ${!networks[*]}; do
        n=${networks[$netP]}
        if [[ $n == "CNN" ]] || [[ $n == "CNN_NP" ]]; then
            prevD=$SupervisedD
            SupervisedD="mnist"
            X_test="data/mnist_test_features.data"
            y_test="data/mnist_test_labels.data"

        fi
        printf "%s\t %s" "loc - $n $conf" " ${SupervisedD} Dataset - rep:"
        mkdir -p $logstart
        fullLogname="$logstart/${n}_${SupervisedD}_${HOSTNAME}_$conf.log"

        if [[ "$clear" -eq 1 ]]; then
            rm -f $fullLogname
        fi
        if [[ -f "$fullLogname" ]] && [[ "$clear" -eq 0 ]]; then
            printf "%s" " --skip-- "
        else
            for run in $(eval echo {1..$rep}); do
                printf "."
                { time -p perf stat -d -d -d systemds \
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
                    features="data/${SupervisedD}_features.data" \
                    labels="data/${SupervisedD}_labels.data" \
                    ; } >>$fullLogname 2>&1
            done
        fi
        printf "\n"

        if [[ $n == "CNN" ]]; then
            SupervisedD=$prevD

            X_test="data/P2_features.data"
            y_test="data/P2_labels.data"
        fi
    done

done
