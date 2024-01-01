#!/bin/bash

rm trace3.dat
rm trace3_lineage.dat
rm trace3_probe.dat
rm trace3_20.dat
rm trace3_40.dat
rm trace3_80.dat

echo "Starting microbenchmark trace3"
echo "----------------------------- "
# time calculated in milliseconds

# Vary data size [800B, 80MB] and reuse (0%, 20%, 40%, 80%) 
# Instruction count = 2M, cache size = 5gb
for config in {1..6..1}
do
  for rep in {1..3}
  do
    echo "Configuration: $config, repetition: $rep"
    config2 all stop
    start=$(date +%s%N)
    runsparkinf -f lineageThroughputSP3.dml -args $config 0 
    end=$(date +%s%N)
    echo -e $config'\t'$((($end-$start)/1000000)) >> trace3.dat

    start=$(date +%s%N)
    runsparkinf -f lineageThroughputSP3.dml -args $config 0 -lineage
    end=$(date +%s%N)
    echo -e $config'\t'$((($end-$start)/1000000)) >> trace3_lineage.dat

    start=$(date +%s%N)
    runsparkinf -f lineageThroughputSP3.dml -args $config 0 -lineage reuse_full
    end=$(date +%s%N)
    echo -e $config'\t'$((($end-$start)/1000000)) >> trace3_probe.dat

    config2 all start
    start=$(date +%s%N)
    runsparkinf -f lineageThroughputSP3.dml -args $config 0.2 -lineage reuse_full
    end=$(date +%s%N)
    echo -e $config'\t'$((($end-$start)/1000000)) >> trace3_20.dat

    start=$(date +%s%N)
    runsparkinf -f lineageThroughputSP3.dml -args $config 0.4 -lineage reuse_full
    end=$(date +%s%N)
    echo -e $config'\t'$((($end-$start)/1000000)) >> trace3_40.dat

    start=$(date +%s%N)
    runsparkinf -f lineageThroughputSP3.dml -args $config 0.8 -lineage reuse_full
    end=$(date +%s%N)
    echo -e $config'\t'$((($end-$start)/1000000)) >> trace3_80.dat
  done
done

exit

