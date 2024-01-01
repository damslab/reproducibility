#!/bin/bash

rm trace1.dat
rm trace1_lineage.dat
rm trace1_probe.dat
rm trace1_20.dat
rm trace1_40.dat
rm trace1_40_inf.dat

echo "Starting microbenchmark trace1"
echo "----------------------------- "
# time calculated in milliseconds

# Vary instruction count [1M, 5M] and reuse (0%, 20%, 40%) 
# Data size = 8MB (10000X100) 
for scale in {1..5..1}
do
  for rep in {1..3}
  do
    echo "Number of Millions: $scale, repetition: $rep"
    config2 all stop
    start=$(date +%s%N)
    runsparkinf -f lineageThroughputSP1.dml -args $scale 0 
    end=$(date +%s%N)
    echo -e $scale'\t'$((($end-$start)/1000000)) >> trace1.dat

    start=$(date +%s%N)
    runsparkinf -f lineageThroughputSP1.dml -args $scale 0 -lineage
    end=$(date +%s%N)
    echo -e $scale'\t'$((($end-$start)/1000000)) >> trace1_lineage.dat

    start=$(date +%s%N)
    runsparkinf -f lineageThroughputSP1.dml -args $scale 0 -lineage reuse_full
    end=$(date +%s%N)
    echo -e $scale'\t'$((($end-$start)/1000000)) >> trace1_probe.dat

    config2 all start
    start=$(date +%s%N)
    runsparkinf -f lineageThroughputSP1.dml -args $scale 0.2 -lineage reuse_full
    end=$(date +%s%N)
    echo -e $scale'\t'$((($end-$start)/1000000)) >> trace1_20.dat

    start=$(date +%s%N)
    runsparkinf -f lineageThroughputSP1.dml -args $scale 0.4 -lineage reuse_full
    end=$(date +%s%N)
    echo -e $scale'\t'$((($end-$start)/1000000)) >> trace1_40.dat

    start=$(date +%s%N)
    runsparkinf -f lineageThroughputSP1.dml -args $scale 0.4 -lineage reuse_full
    end=$(date +%s%N)
    echo -e $scale'\t'$((($end-$start)/1000000)) >> trace1_40_inf.dat
  done
done

exit

