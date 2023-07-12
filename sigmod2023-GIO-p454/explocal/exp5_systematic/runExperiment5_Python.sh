#!/bin/bash

config=$1
dataset=$2
log_file_name=$3
parallel=$4

declare -a field_list=("F0" "F1" "F2" "F3" "F4" "F5" "F6" "F7" "F8" "F9" "F10" "F11" "F12" "F13" "F14" "F15" "F16" "F17" "F18" "F19" "F20" "F21" "F22" "F23" "F24" "F25" "F26" "F27" "F28" "F29" "F30" "F31" "F32")

for field in "${field_list[@]}"; do
  if [ -d "data/${dataset}/${field}" ]; then       
        SCRIPT="python3.8 ${config} data/${dataset}.dat ${field} ${parallel}"
        echo $SCRIPT

        # clean OS cache, need sudo privilege
        echo 3 >/proc/sys/vm/drop_caches && sync
        sleep 3

        start=$(date +%s%N)
        $SCRIPT
        end=$(date +%s%N)
        echo "Python,"${dataset}","${field}","$((($end - $start) / 1000000))","${parallel} >>results/$log_file_name.dat
  fi
done
