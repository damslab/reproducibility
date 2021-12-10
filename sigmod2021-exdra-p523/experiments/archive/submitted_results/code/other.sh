#/bin/bash

source parameters.sh

logstart="results/other"

mkdir -p $logstart
mkdir -p "tmp/other"

for n in $networks; do
    printf "%s\t %s" "loc - $n" " Dataset - rep:"
    mkdir -p $logstart
    if [ "$n" == "TwoNN" ]; then
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

            if [ "$n" == "TwoNN" ]; then
                printf "."
                { time -p python code/other/TwoNN.py \
                    -x "data/${SupervisedD}_features.npy" \
                    -y "data/${SupervisedD}_labels.npy" \
                    -o "tmp/${x}_${UnsupervisedD}_SKLEARN.res" \
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
    printf "%s\t %s" "fed ${numWorkers}W $conf - $x" " ${UnsupervisedD} SKLEARN Dataset - rep:"
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
    printf "%s\t %s" "fed ${numWorkers}W $conf - $x" " ${UnsupervisedD} SKLEARN Dataset - rep:"
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
