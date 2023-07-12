#!/bin/bash

config=$1
dataset=$2
log_file_name=$3
parallel=$4

declare -a query_list=("Q1" "Q2" "Q3" "Q4" "Q5")
for query in "${query_list[@]}"; do
  if [ -d "data/${dataset}/${query}" ]; then     
      SCRIPT="./setup/RapidJSON/${config} data/${dataset}.dat data/${dataset}/${query}/${dataset}.schema ${query} ${parallel}"
      echo $SCRIPT

      # clean OS cache, need sudo privilege
      echo 3 >/proc/sys/vm/drop_caches && sync
      sleep 3

      start=$(date +%s%N)
      $SCRIPT
      end=$(date +%s%N)
      echo "RapidJSON,"${dataset}","${query}","$((($end - $start) / 1000000))","${parallel} >>results/$log_file_name.dat    
  fi
done