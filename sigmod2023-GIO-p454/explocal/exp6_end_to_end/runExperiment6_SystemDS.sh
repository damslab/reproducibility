#!/bin/bash

dataset=$1
log_file_name=$2
config_name=$3
parallel=$4

SCRIPT="$CMD  -DdataFileName=data/${dataset}.dat\
              -Dparallel=${parallel}\
              -DschemaFileName=data/${dataset}/${dataset}.schema\
              -DschemaMapFileName=data/${dataset}/${dataset}.schemaMap\
              -cp ./setup/SystemDS/lib/*:./setup/SystemDS/SystemDS.jar org.apache.sysds.runtime.iogen.EXP.SystemDS
       "
echo $SCRIPT

# clean OS cache, need sudo privilege
echo 3 >/proc/sys/vm/drop_caches && sync
sleep 3

start=$(date +%s%N)
$SCRIPT
end=$(date +%s%N)
echo ${config_name}","${dataset}","$((($end - $start) / 1000000))","${parallel} >>results/$log_file_name.dat    