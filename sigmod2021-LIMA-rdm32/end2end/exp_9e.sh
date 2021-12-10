#!/bin/bash

nrows=10000
cols=1000
newcols=90

rm respca_pipeline.dat
rm respca_pipeline_reuse.dat

echo "Starting (9e) Hyper-parameter tuning for PCA-LM pipeline "
echo "---------------------------------------------------------"
# time calculated in milliseconds

for nrows in {10000..100000..10000}
do
  for rep in {1..3}
  do
    echo "Number of rows: $nrows, repetition: $rep"
    start=$(date +%s%N)
    runjava -f pca_pipeline.dml -args $nrows -stats
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$newcols'\t'$((($end-$start)/1000000)) >> respca_pipeline.dat

    start=$(date +%s%N)
    runjava -f pca_pipeline.dml -args $nrows -lineage reuse_hybrid -stats
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$newcols'\t'$((($end-$start)/1000000)) >> respca_pipeline_reuse.dat
  done
done



exit

