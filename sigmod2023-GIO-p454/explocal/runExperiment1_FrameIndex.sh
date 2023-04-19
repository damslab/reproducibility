#!/bin/bash

dataset=$1
log_file_name=$2
parallel=$3

# write header to log file
if [[ ! -f results/$log_file_name.dat ]] ; then
  echo "dataset,query,example_nrows,time,parallel" >>results/$log_file_name.dat
fi

declare -a query_list=("Q1" "Q2" "Q3" "Q4" "Q5")

for query in "${query_list[@]}"; do
  if [ -d "data/${dataset}/${query}" ]; then
    for examples in 1000 2000 3000 4000 5000 6000 7000 8000 9000 10000; do            
            SCRIPT="$CMD  -DsampleRawFileName=data/${dataset}/${query}/sample-${dataset}${examples}.raw\
                          -DsampleFrameFileName=data/${dataset}/${query}/sample-${dataset}${examples}.frame\
                          -DschemaFileName=data/${dataset}/${query}/${dataset}.schema\
                          -Dparallel=${parallel}\
                          -cp ./setup/SystemDS/lib/*:./setup/SystemDS/SystemDS.jar org.apache.sysds.runtime.iogen.EXP.GIOFrameIdentificationIndex
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
  fi
done
