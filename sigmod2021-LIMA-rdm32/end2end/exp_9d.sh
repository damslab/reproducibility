#!/bin/bash

nrows=50000
cols=1000
nclass=20

rm resenswp.dat
rm resenswp_reuse.dat

echo "Starting (9d) Tune weights for Ensemble Learning"
echo "------------------------------------------------"
# time calculated in milliseconds

for nweights in {1000..5000..1000}
do
  for rep in {1..3}
  do
    echo "Number of weights: $nweights, repetition: $rep"
    start=$(date +%s%N)
    runjava -f enswp_voting.dml -args $nrows $cols $nclass $nweights -stats
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$nweights'\t'$((($end-$start)/1000000)) >> resenswp.dat

    start=$(date +%s%N)
    runjava -f enswp_voting.dml -args $nrows $cols $nclass $nweights -lineage reuse_hybrid -stats

    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$nweights'\t'$((($end-$start)/1000000)) >> resenswp_reuse.dat
  done
done



exit

