#!/bin/bash
# Configs used (current results):
# 1. 38gb driver, 8 executors
# 2. Operation memory 19%, buffer pool 53%. Lineage cache 14% 
# 3. Use -XX:+UseParallelGC/-XX:+UseConcMarkSweepGC for GC in driver

rows=425000
cols=1500

rm automl.dat
rm automl_reusefull.dat
rm automl_reusemulti.dat
rm automl_helix.dat
rm automl_lima.dat

echo "Starting hyperband l2svm, multilogreg "
echo "------------------------------------- "
# time calculated in milliseconds

for scale in {1..4..1}
do
  nrows=$(($rows*$scale))
  for rep in {1..3} #3
  do
    echo "Number of rows: $nrows, repetition: $rep"
    config2 all stop
    start=$(date +%s%N)
    runspark -f hyperband.dml -args $nrows -stats
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> automl.dat

    start=$(date +%s%N)
    runspark -f hyperband_helix.dml -args $nrows -stats
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> automl_helix.dat

    # Disable multi-backend configuration for LIMA
    start=$(date +%s%N)
    runspark -f hyperband.dml -args $nrows -stats -lineage reuse_full
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> automl_lima.dat


    config2 all start
    start=$(date +%s%N)
    runspark -f hyperband.dml -args $nrows -stats -lineage reuse_full
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> automl_reusefull.dat

    start=$(date +%s%N)
    runspark -f hyperband.dml -args $nrows -stats -lineage reuse_multilevel
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> automl_reusemulti.dat
  done
done

exit

