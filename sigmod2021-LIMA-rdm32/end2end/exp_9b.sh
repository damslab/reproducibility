#!/bin/bash

nrows=1000000
cols=100
combi=900

rm resexample.dat
rm resexample_reuse.dat
rm resexample_parfor.dat
rm resexample_parfor_reuse.dat

echo "Starting (9b) Hyper-parameter tuning for LM"
echo "--------------------------------------------"
# time calculated in milliseconds

for nrows in {100000..1000000..100000}
do
  for rep in {1..3}
  do
    echo "Number of rows: $nrows, repetition: $rep"
    start=$(date +%s%N)
    runjava -f gridsearchLM.dml -args $nrows -stats
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$combi'\t'$((($end-$start)/1000000)) >> resexample.dat

    start=$(date +%s%N)
    runjava -f gridsearchLM.dml -args $nrows -stats -lineage reuse_hybrid 
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$combi'\t'$((($end-$start)/1000000)) >> resexample_reuse.dat

    start=$(date +%s%N)
    runjava -f gridsearchLM_parfor.dml -args $nrows -stats
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$combi'\t'$((($end-$start)/1000000)) >> resexample_parfor.dat

    start=$(date +%s%N)
    runjava -f gridsearchLM_parfor.dml -args $nrows -lineage reuse_hybrid -stats
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$combi'\t'$((($end-$start)/1000000)) >> resexample_parfor_reuse.dat
  done
done


exit

