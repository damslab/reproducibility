#!/bin/bash

# Load Parameters
source parameters.sh

# Activate python environment
source "$VENV_PATH/bin/activate";

Algs=("kmeans pca")
networks=("FNN CNN")

UnsupervisedD="P2P"
SupervisedD="P2P"

logstart="results/other"

mkdir -p $logstart
mkdir -p "tmp/other"

for n in $networks; do
    printf "%s\t %s" "other - $n" " Tensorflow - rep:"
    mkdir -p $logstart
    if [ "$n" == "FNN" ]; then
        d="P2P"
    else
        d="mnist"
    fi
    fullLogname="$logstart/${n}_${d}_${HOSTNAME}.log"

    if [[ "$clear" -eq 1 ]]; then
        rm -f $fullLogname
    fi

    if [[ -f "$fullLogname" ]] && [[ "$clear" -eq 0 ]]; then
        printf "%s" " --skip-- "
    else
        for run in $(eval echo {1..$rep}); do

            if [ "$n" == "FNN" ]; then
                printf "."
                { time -p python code/other/FNN.py \
                    -x "data/${SupervisedD}_features.npy" \
                    -y "data/${SupervisedD}_labels.npy" \
                    -o "tmp/${x}_${UnsupervisedD}_TensorflowRes.res" \
                    ;} >>$fullLogname 2>&1
            else
                printf "."
                { time -p python code/other/CNN.py \
                    ;} >>$fullLogname 2>&1
            fi

        done
    fi
    printf "\n"
done

for x in $Algs; do
    printf "%s\t %s" "other  - $x" " ${UnsupervisedD} SKLEARN  - rep:"
    fullLogname="$logstart/${x}_${SupervisedD}_${HOSTNAME}_SKLEARN.log"
    if [[ "$clear" -eq 1 ]]; then
        rm -f $fullLogname
    fi
    if [[ -f "$fullLogname" ]] && [[ "$clear" -eq 0 ]]; then
        printf "%s" " --skip-- "
    else
        for run in $(eval echo {1..$rep}); do
            printf "."
            { time -p python code/other/$x.py \
                -x "data/${SupervisedD}_features.npy" \
                -y "data/${SupervisedD}_labels.npy" \
                -o "tmp/${x}_${UnsupervisedD}_SKLEARN.res" \
                ;} >>$fullLogname 2>&1
            # -v True \
            # -v 0 \
        done
    fi
    printf "\n"
done

for x in $SAlgs; do
    printf "%s\t %s" "other  - $x" " ${UnsupervisedD} SKLEARN - rep:"
    fullLogname="$logstart/${x}_${SupervisedD}_${HOSTNAME}_SKLEARN.log"
    if [[ "$clear" -eq 1 ]]; then
        rm -f $fullLogname
    fi
    if [[ -f "$fullLogname" ]] && [[ "$clear" -eq 0 ]]; then
        printf "%s" " --skip-- "
    else
        for run in $(eval echo {1..$rep}); do
            printf "."
            { time -p python code/other/$x.py \
                -x "data/${SupervisedD}_features.npy" \
                -y "data/${SupervisedD}_labels.npy" \
                -v True \
                -o "tmp/${x}_${UnsupervisedD}_SKLEARN.res" \
                ;} >>$fullLogname 2>&1
            # -v 0 \
        done
    fi
    printf "\n"
done
