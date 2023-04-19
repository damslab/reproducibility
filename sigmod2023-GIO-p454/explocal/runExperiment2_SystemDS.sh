#!/bin/bash

config=$1
dataset=$2
log_file_name=$3
parallel=$4
example_nrows=200

declare -a query_list=("Q1" "Q2" "Q3" "Q4" "Q5")
for query in "${query_list[@]}"; do
  if [ -d "data/${dataset}/${query}" ]; then      
      SCRIPT="$CMD     -DsampleRawFileName=data/${dataset}/${query}/sample-${dataset}${example_nrows}.raw\
                       -DsampleFrameFileName=data/${dataset}/${query}/sample-${dataset}${example_nrows}.frame\
                       -DdataFileName=data/${dataset}.dat\
                       -Dconfig=${config}\
                       -DschemaFileName=data/${dataset}/${query}/${dataset}.schema\
                       -DschemaMapFileName=data/${dataset}/${query}/${dataset}.schemaMap\
                       -Dparallel=${parallel}\
                       -cp ./setup/SystemDS/lib/*:./setup/SystemDS/SystemDS.jar org.apache.sysds.runtime.iogen.EXP.SystemDS
               "
      echo $SCRIPT
     
      # clean OS cache, need sudo privilege
      echo 3 >/proc/sys/vm/drop_caches && sync
      sleep 3

      start=$(date +%s%N)
      $SCRIPT
      end=$(date +%s%N)
      echo "SystemDS+"${config}","${dataset}","${query}","$((($end - $start) / 1000000))","${parallel} >>results/$log_file_name.dat
  fi
done
