#!/bin/bash

nrows=100000
cols=1000
combi=90

rm respcanb_sk.dat
rm respcanb.dat
rm respcanb_reuse.dat

echo "Starting (10d) PCA naivebayes pipeline "
echo "---------------------------------------"
# time calculated in milliseconds

for nrows in {50000..400000..25000}
do
  for rep in {1..3}
  do
    echo "Number of rows: $nrows, repetition: $rep"
    source tf-venv/bin/activate
    start=$(date +%s%N)
    python3 pcaNB_sk.py $nrows
    end=$(date +%s%N)
    deactivate
    echo -e $nrows'\t'$cols'\t'$combi'\t'$((($end-$start)/1000000)) >> respcanb_sk.dat

    start=$(date +%s%N)
    runjava -f pcaNB.dml -args $nrows -stats
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$combi'\t'$((($end-$start)/1000000)) >> respcanb.dat

    start=$(date +%s%N)
    runjava -f pcaNB.dml -args $nrows -stats -lineage reuse_multilevel
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$combi'\t'$((($end-$start)/1000000)) >> respcanb_reuse.dat
  done
done


exit

