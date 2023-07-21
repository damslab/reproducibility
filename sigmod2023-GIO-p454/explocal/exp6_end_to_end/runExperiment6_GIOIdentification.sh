#!/bin/bash

dataset=$1
log_file_name=$2
parallel=$3

if [[ ! -f results/$log_file_name.dat ]] ; then
    echo "dataset,time,parallel" >>results/$log_file_name.dat
fi

SCRIPT="$CMD  -DsampleRawFileName=data/${dataset}/sample-${dataset}200.raw\
              -DsampleFrameFileName=data/${dataset}/sample-${dataset}200.frame\
              -DschemaFileName=data/${dataset}/${dataset}.schema\
              -Dparallel=${parallel}\
              -cp ./setup/JavaBaselines/lib/*:./setup/JavaBaselines/JavaBaselines.jar at.tugraz.benchmark.GIOFrameIdentification
       "
echo $SCRIPT

# clean OS cache, need sudo privilege
echo 3 >/proc/sys/vm/drop_caches && sync
sleep 3

start=$(date +%s%N)
$SCRIPT
end=$(date +%s%N)
echo "GIO,"${dataset}","$((($end - $start) / 1000000))","${parallel} >>results/$log_file_name.dat      