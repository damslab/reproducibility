#!/bin/bash

row=67000 #1gb

rm trace2.dat
rm trace2_40_900m.dat
rm trace2_40_5g.dat
rm trace2_40_30g.dat

echo "Starting microbenchmark trace"
echo "----------------------------- "
# time calculated in milliseconds

# Vary data size [2gb, 10gb] and cache size (5gb, 30gb) 
# Instruction count = 1M, reuse = 40%
for scale in {2..10..2}
do
  nrow=$(($row*$scale))
  for rep in {1..1}
  do
    echo "Number of rows: $nrow, repetition: $rep"
    config2 all stop
    start=$(date +%s%N)
    runsparkinf -f lineageThroughputSP2.dml -args $nrow -stats
    end=$(date +%s%N)
    echo -e $nrow'\t'$((($end-$start)/1000000)) >> trace2.dat

    config2 all start
    start=$(date +%s%N)
    runsparkinf -f lineageThroughputSP2.dml -args $nrow -stats -lineage reuse_full
    end=$(date +%s%N)
    echo -e $nrow'\t'$((($end-$start)/1000000)) >> trace2_40_900m.dat

    config2 all start
    start=$(date +%s%N)
    runsparkinf -f lineageThroughputSP2.dml -args $nrow -stats -lineage reuse_full
    end=$(date +%s%N)
    echo -e $nrow'\t'$((($end-$start)/1000000)) >> trace2_40_5g.dat

    start=$(date +%s%N)
    runsparkinf -f lineageThroughputSP2.dml -args $nrow -stats -lineage reuse_full
    end=$(date +%s%N)
    echo -e $nrow'\t'$((($end-$start)/1000000)) >> trace2_40_30g.dat
  done
done

exit

