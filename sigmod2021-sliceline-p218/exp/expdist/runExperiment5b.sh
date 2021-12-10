#!/bin/bash

start=$(date +%s%N)
./exp/expdist/sparkDML.sh SystemDS.jar -f exp/expdist/SlicingExp5b.dml -exec singlenode -stats \
  -args /data/USCensus_X1.bin /data/USCensus_o_e1.bin 4 "for"
end=$(date +%s%N)
echo "USCensus,1,"$((($end-$start) / 1000000 - 1500)) >> results/Experiment5b_times.dat

start=$(date +%s%N)
./exp/expdist/sparkDML.sh SystemDS.jar -f exp/expdist/SlicingExp5b.dml -exec singlenode -stats \
  -args /data/USCensus_X1.bin /data/USCensus_o_e1.bin 4 "parfor-l"
end=$(date +%s%N)
echo "USCensus,2,"$((($end-$start) / 1000000 - 1500)) >> results/Experiment5b_times.dat

start=$(date +%s%N)
# NOTE: modifications needed to force SystemDS to remote parfor AND otherwise singlenode operations
# ./exp/expdist/sparkDML.sh SystemDSremote.jar -f exp/expdist/SlicingExp5b.dml -exec singlenode -stats \
#  -args /data/USCensus_X1.bin /data/USCensus_o_e1.bin 4 "parfor-r"
./exp/expdist/sparkDML.sh SystemDS.jar -f exp/expdist/SlicingExp5b.dml -exec hybrid -stats \
  -args /data/USCensus_X1.bin /data/USCensus_o_e1.bin 4 "parfor-r"
end=$(date +%s%N)
echo "USCensus,3,"$((($end-$start) / 1000000 - 1500)) >> results/Experiment5b_times.dat
