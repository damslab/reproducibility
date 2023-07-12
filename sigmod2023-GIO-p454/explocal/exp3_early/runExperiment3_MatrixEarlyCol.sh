#!/bin/bash

dataset=$1
log_file_name=$2
parallel=$3

for examples in 100 200 300 400 500 600 700 800 900 1000; do      
      SCRIPT="$CMD  -DsampleRawFileName=data/${dataset}/sample-${dataset}${examples}.raw\
                    -DsampleMatrixFileName=data/${dataset}/sample-${dataset}${examples}.matrix\
                    -Dparallel=${parallel}\
                    -cp ./setup/JavaBaselines/lib/*:./setup/JavaBaselines/JavaBaselines.jar at.tugraz.benchmark.GIOMatrixEarly
              "
      echo $SCRIPT

      # clean OS cache, need sudo privilege
      echo 3 >/proc/sys/vm/drop_caches && sync
      sleep 3

      start=$(date +%s%N)
      $SCRIPT
      end=$(date +%s%N)
      echo "OLDGIO,"${dataset}","${examples}","$((($end - $start) / 1000000))","${parallel} >>results/$log_file_name.dat
    done    
  done