#!/bin/bash

mkdir -p results/diskSpeed/
logfile=results/diskSpeed/$HOSTNAME-diskspeed.log
tmp=tmp/disktest.dat

run() {
    rep=$1
    size=$2
    echo $rep $size | tee -a $logfile
    sync
    for r in {1..30}; do
        rm -f $tmp
        a=$(dd if=/dev/zero of=$tmp bs=${size} count=$rep |& grep copied)
        echo $a | tee -a $logfile
        # sleep 6
        sync
    done
    wait
}

rm -f $logfile
touch $logfile

## write 16 Gb in each test.

run 1 80K
run 1 800K
run 1 8M
run 1 80M
run 1 800M
run 4 2G
run 40 2G

rm -f $tmp
