#!/bin/bash
run() {
    log=results/wordemb/emb_nn/$HOSTNAME/torch/abstracts_${2}_words_${1}_abslength_${3}.log
    echo $log
    if [ -f "$log" ]; then
        mv $log "$log$(date +"%m-%d-%y-%r").log"
    fi
    for i in $(seq $exrep); do
        perf stat -d -d -d \
            timeout 72000 \
            python code/wordemb/torch_nn_emb.py \
            --words $1 --abstracts $2 --abstractlength $3 \
            >>$log 2>&1
    done
}

mkdir -p results/wordemb/emb_nn/$HOSTNAME/torch


for a in $as; do
    for w in $ws; do 
        for l in $al; do 
            run $w $a $l
        done 
    done 
done 

