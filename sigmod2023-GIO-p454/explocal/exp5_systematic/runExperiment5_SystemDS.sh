#!/bin/bash

config=$1
dataset=$2
log_file_name=$3
parallel=$4
example_nrows=200

#declare -a field_list=("F0" "F1" "F2" "F3" "F4" "F5" "F6" "F7" "F8" "F9" "F10" "F11" "F12" "F13" "F14" "F15" "F16" "F17" "F18" "F19" "F20" "F21"
#"F22" "F23" "F24" "F25" "F26" "F27" "F28" "F29" "F30" "F31" "F32")

declare -a field_list=("F10")

for field in "${field_list[@]}"; do
  if [ -d "data/${dataset}/${field}" ]; then        
        SCRIPT="$CMD    -DsampleRawFileName=data/${dataset}/${field}/sample-${dataset}${example_nrows}.raw\
                        -DsampleFrameFileName=data/${dataset}/${field}/sample-${dataset}${example_nrows}.frame\
                        -DdataFileName=data/${dataset}.dat\
                        -Dconfig=${config}\
                        -DschemaFileName=data/${dataset}/${field}/${dataset}.schema\
                        -DschemaMapFileName=data/${dataset}/${field}/${dataset}.schemaMap\
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
        echo "SystemDS+"${config}","${dataset}","${field}","$((($end - $start) / 1000000))","${parallel} >>results/$log_file_name.dat
  fi
done
