#!/bin/bash

dataset=$1
log_file_name=$2
parallel=$3

# write header
if [[ ! -f results/$log_file_name.dat ]] ; then
  echo "dataset,query,example_nrows,time,parallel" >>results/$log_file_name.dat
fi

declare -a query_list=("Q1" "Q2")

for query in "${query_list[@]}"; do
  for examples in 200 300 400 500 600 700 800 900 1000; do      
      SCRIPT="$CMD  -DsampleRawFileName=data/${dataset}/${query}/sample-${dataset}${examples}.raw\
                    -DsampleMatrixFileName=data/${dataset}/${query}/sample-${dataset}${examples}.matrix\
                    -Dparallel=${parallel}\
                    -cp ./setup/SystemDS/lib/*:./setup/SystemDS/SystemDS.jar org.apache.sysds.runtime.iogen.EXP.GIOMatrixIdentification
              "
      echo $SCRIPT

      # clean OS cache, need sudo privilege
      echo 3 >/proc/sys/vm/drop_caches && sync
      sleep 3

      start=$(date +%s%N)
      $SCRIPT
      end=$(date +%s%N)
      echo ${dataset}","${query}","${examples}","$((($end - $start) / 1000000))","${parallel} >>results/$log_file_name.dat
    done    
  done
done
