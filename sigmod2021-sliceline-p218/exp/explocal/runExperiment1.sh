#!/bin/bash

#CMD="java -Xmx600g -Xms600g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "

#for all configs
for config in 1 2 3 4 5
do 
  #for all repetitions
  for rep in {1..3}
  do
    start=$(date +%s%N)
    $CMD -f exp/explocal/SlicingExp1_${config}.dml -exec singlenode -stats \
      -args data/Salaries_X.csv data/Salaries_o_e.csv ${config} results/Experiment1_p${config}.dat
    end=$(date +%s%N)
    echo ${config}","$((($end-$start) / 1000000 - 1500)) >> results/Experiment1_times.dat
  done 
done
