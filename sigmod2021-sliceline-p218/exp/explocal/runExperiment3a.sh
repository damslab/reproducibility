#!/bin/bash

#CMD="java -Xmx600g -Xms600g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "

#for all configs
for data in Adult USCensus Covtype KDD98
do 
  for alpha in 0.36 0.68 0.84 0.92 0.96 0.98 0.99
  do 
    #for all repetitions
    for rep in {1..1}
    do
	    start=$(date +%s%N)
	    $CMD -f exp/explocal/SlicingExp3.dml -exec singlenode -stats \
	      -args data/${data}_X.csv data/${data}_o_e.csv ${alpha} 0.01 results/Experiment3_${data}_a${alpha}.dat
	    end=$(date +%s%N)
	    echo ${data}","${alpha}","$((($end-$start) / 1000000 - 1500)) >> results/Experiment3a_times.dat
    done
  done 
done
