#!/bin/bash

#CMD="java -Xmx600g -Xms600g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "

#for all configs
for data in Adult USCensus Covtype KDD98
do 
  #for all repetitions
  for rep in {1..3}
  do
    start=$(date +%s%N)
    $CMD -f exp/explocal/SlicingExp2.dml -exec singlenode -stats \
      -args data/${data}_X.csv data/${data}_o_e.csv ${data} results/Experiment2_${data}.dat
    end=$(date +%s%N)
    echo ${data}","$((($end-$start) / 1000000 - 1500)) >> results/Experiment2_times.dat
  done 
done
