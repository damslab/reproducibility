#!/bin/bash

config=$1
dataset=$2
log_file_name=$3
parallel=$4

declare -a query_list=("Q1" "Q2")
for query in "${query_list[@]}"; do  
  SCRIPT="python3.8 ${config} data/${dataset}.dat ${query} ${parallel}"
  echo $SCRIPT

  # clean OS cache, need sudo privilege
  echo 3 >/proc/sys/vm/drop_caches && sync
  sleep 3

  start=$(date +%s%N)
  $SCRIPT
  end=$(date +%s%N)
  echo "Python,"${dataset}","${query}","$((($end - $start) / 1000000))","${parallel} >>results/$log_file_name.dat
done
