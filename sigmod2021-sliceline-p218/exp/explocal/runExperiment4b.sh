#!/bin/bash

#CMD="java -Xmx600g -Xms600g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "

#for all configs
for data in KDD98 USCensus Covtype Adult
do 
  for blksz in 16
  do 
    #for all repetitions
    for rep in {1..3}
    do
	    start=$(date +%s%N)
	    $CMD -f exp/explocal/SlicingExp4.dml -exec singlenode -stats \
	      -args data/${data}_X.csv data/${data}_o_e.csv ${blksz}
	    end=$(date +%s%N)
	    echo ${data}","${blksz}","$((($end-$start) / 1000000 - 1500)) >> results/Experiment4b_times.dat
    done
  done 
done
