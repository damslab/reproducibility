#!/bin/bash

rows="2 8 32 128 512 2048"
cols=784
iter="1000000 250000 62500 15625 3906 976"

rm reslinTime.dat 
rm reslinTime_lineage.dat 
rm reslinTime_reuse.dat 
rm reslinTime_dedup_reuse.dat 
rm reslinTime_dedup.dat
# time calculated in milliseconds

echo "Starting (6a) Runtime Overhead microbenchmark"
echo "----------------------------------------------"

set $iter
for i in $rows
do
  for rep in {1..3}
  do
    start=$(date +%s%N)
    runjava -f micro_linCost.dml -args $i $1
    end=$(date +%s%N)
    echo -e $i'\t'$cols'\t'$1'\t'$((($end-$start)/1000000)) >> reslinTime.dat

    start=$(date +%s%N)
    runjava -f micro_linCost.dml -lineage -args $i $1 
    end=$(date +%s%N)
    echo -e $i'\t'$cols'\t'$1'\t'$((($end-$start)/1000000)) >> reslinTime_lineage.dat

    start=$(date +%s%N)
    runjava -f micro_linCost.dml -lineage reuse_full -args $i $1 
    end=$(date +%s%N)
    echo -e $i'\t'$cols'\t'$1'\t'$((($end-$start)/1000000)) >> reslinTime_reuse.dat

    start=$(date +%s%N)
    runjava -f micro_linCost.dml -lineage dedup -args $i $1 
    end=$(date +%s%N)
    echo -e $i'\t'$cols'\t'$1'\t'$((($end-$start)/1000000)) >> reslinTime_dedup.dat
  done
  shift
done

exit

