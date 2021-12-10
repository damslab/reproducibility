#!/bin/bash

rows=100000
cols=1000
sp=1.0

rm resmicrotsmm.dat
rm resmicrotsmm_preuse.dat
rm resmicrotsmm_preuse_comp.dat

# time calculated in milliseconds

echo "Starting (7a) Partial Reuse microbenchmark"
echo "------------------------------------------"

for nrows in {10000..100000..10000}
do
  for rep in {1..2}
  do
    echo "$nrows num of rows and $rep th repetition"
    config compassisted stop
    start=$(date +%s%N)
    runjava -f micro_tsmmcbind_comp.dml -args $nrows -stats 
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$sp'\t'$((($end-$start)/1000000)) >> resmicrotsmm.dat

    start=$(date +%s%N)
    runjava -f micro_tsmmcbind_comp.dml -args $nrows -lineage reuse_partial -stats 
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$sp'\t'$((($end-$start)/1000000)) >> resmicrotsmm_preuse.dat

    config compassisted start 
    start=$(date +%s%N)
    runjava -f micro_tsmmcbind_comp.dml -args $nrows -lineage reuse_full -stats 
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$sp'\t'$((($end-$start)/1000000)) >> resmicrotsmm_preuse_comp.dat

  done

done


exit

