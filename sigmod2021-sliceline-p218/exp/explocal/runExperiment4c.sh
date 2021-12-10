#!/bin/bash

#for all configs
for data in Adult
do 
    #for all repetitions
    for rep in {1..3}
    do
	    start=$(date +%s%N)
	    time Rscript exp/explocal/slicefinder.R data/Adult_X.csv data/Adult_o_e.csv 16
	    end=$(date +%s%N)
	    echo ${data}","$((($end-$start) / 1000000 - 1500)) >> results/Experiment4c_times.dat
    done
done
