#!/bin/bash

dataset=$1
log_file_name=$2
parallel=$3

SCRIPT="python3.8 setup/Python/frameHL7Reader.py data/${dataset}.dat All"
echo $SCRIPT

# clean OS cache, need sudo privilege
echo 3 >/proc/sys/vm/drop_caches && sync
sleep 3

start=$(date +%s%N)
$SCRIPT
end=$(date +%s%N)
echo "Python,"${dataset}","$((($end - $start) / 1000000))","${parallel} >>results/$log_file_name.dat