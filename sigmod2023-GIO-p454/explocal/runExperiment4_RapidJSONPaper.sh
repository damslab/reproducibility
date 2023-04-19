#!/bin/bash

config=$1
dataset=$2
log_file_name=$3
parallel=$4

declare -a field_list=("F1" "F2" "F3" "F4" "F5" "F6" "F7" "F8" "F9" "F10")

for field in "${field_list[@]}"; do
  if [ -d "data/${dataset}/${field}" ]; then       
        SCRIPT="./setup/RapidJSON/${config} data/${dataset}.dat data/${dataset}/${field}/${dataset}.schema ${field} ${parallel}"
        echo $SCRIPT

        #clean OS cache, need sudo privilege
        echo 3 >/proc/sys/vm/drop_caches && sync
        sleep 3

        start=$(date +%s%N)
        $SCRIPT
        end=$(date +%s%N)
        echo "RapidJSON,"${dataset}","${field}","$((($end - $start) / 1000000))","${parallel} >>results/$log_file_name.dat
  fi
done