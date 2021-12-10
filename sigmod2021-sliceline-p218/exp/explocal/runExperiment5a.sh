#!/bin/bash

#CMD="java -Xmx600g -Xms600g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "

#for all configs
for scale in 1 2 3 4 5 6 7 8 9 10
do 
  #for all repetitions
  for rep in {1..3}
  do
	    start=$(date +%s%N)
	    $CMD -f exp/explocal/SlicingExp4.dml -exec singlenode -stats \
	      -args data/USCensus_X${scale}.bin data/USCensus_o_e${scale}.bin 4
	    end=$(date +%s%N)
	    echo "USCensus,"${scale}","$((($end-$start) / 1000000 - 1500)) >> results/Experiment5a_times.dat
  done
done 
