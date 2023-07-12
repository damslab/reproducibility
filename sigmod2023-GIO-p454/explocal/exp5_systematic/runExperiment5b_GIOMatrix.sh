#!/bin/bash

dataset=$1
log_file_name=$2
parallel=$3

# write header
if [[ ! -f results/$log_file_name.dat ]] ; then
  echo "baseline,dataset,field,time,parallel" >>results/$log_file_name.dat
fi

example_nrows=200
declare -a field_list=("F0" "F1" "F2" "F3" "F4" "F5" "F6" "F7" "F8" "F9" "F10" "F11" "F12" "F13" "F14" "F15" "F16" "F17" "F18" "F19" "F20" "F21"
"F22" "F23" "F24" "F25" "F26" "F27" "F28")

for field in "${field_list[@]}"; do
  if [ -d "data/${dataset}/${field}" ]; then        
        SCRIPT="$CMD -DsampleRawFileName=data/${dataset}/${field}/sample-${dataset}${example_nrows}.raw\
                    -DsampleMatrixFileName=data/${dataset}/${field}/sample-${dataset}${example_nrows}.matrix\
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
        echo "GIO,"${dataset}","${field}","$((($end - $start) / 1000000))","${parallel} >>results/$log_file_name.dat
  fi
done
