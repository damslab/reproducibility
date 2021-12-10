#!/bin/bash

nrows=1000000
cols=100
combi=90

rm resexample_cv.dat
rm resexample_cv_reuse.dat
rm resexample_cv_parfor.dat
rm resexample_cv_parfor_reuse.dat

echo "Starting (9c) Hyper-parameter tuning for Cross-Validated LM"
echo "-----------------------------------------------------------"
# time calculated in milliseconds

for nrows in {100000..1000000..100000}
do
  for rep in {1..3}
  do
    echo "Number of rows: $nrows, repetition: $rep"
    start=$(date +%s%N)
    runjava -f gridsearchLM_cv.dml -args $nrows -stats
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$combi'\t'$((($end-$start)/1000000)) >> resexample_cv.dat

    start=$(date +%s%N)
    runjava -f gridsearchLM_cv.dml -args $nrows -lineage reuse_hybrid -stats
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$combi'\t'$((($end-$start)/1000000)) >> resexample_cv_reuse.dat

    start=$(date +%s%N)
    runjava -f gridsearchLM_cv_parfor.dml -args $nrows -stats
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$combi'\t'$((($end-$start)/1000000)) >> resexample_cv_parfor.dat

    start=$(date +%s%N)
    runjava -f gridsearchLM_cv_parfor.dml -args $nrows -lineage reuse_hybrid -stats
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$combi'\t'$((($end-$start)/1000000)) >> resexample_cv_parfor_reuse.dat
 
  done
done


exit

