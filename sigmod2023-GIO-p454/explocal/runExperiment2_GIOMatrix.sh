#!/bin/bash

dataset=$1
log_file_name=$2
parallel=$3

# write header
if [[ ! -f results/$log_file_name.dat ]] ; then
  echo "baseline,dataset,query,time,parallel" >>results/$log_file_name.dat
fi
  
example_nrows=200
declare -a query_list=("Q1" "Q2")

for query in "${query_list[@]}"; do    
    SCRIPT="$CMD -DsampleRawFileName=data/${dataset}/${query}/sample-${dataset}${example_nrows}.raw\
                 -DsampleMatrixFileName=data/${dataset}/${query}/sample-${dataset}${example_nrows}.matrix\
                 -DdataFileName=data/${dataset}.dat\
                 -Dparallel=${parallel}\
                 -cp ./setup/SystemDS/lib/*:./setup/SystemDS/SystemDS.jar org.apache.sysds.runtime.iogen.EXP.GIOMatrix
                  "
      echo $SCRIPT

      # clean OS cache, need sudo privilege
      echo 3 >/proc/sys/vm/drop_caches && sync
      sleep 3

      start=$(date +%s%N)
      $SCRIPT
      end=$(date +%s%N)
      echo "GIO,"${dataset}","${query}","$((($end - $start) / 1000000))","${parallel} >>results/$log_file_name.dat
done
