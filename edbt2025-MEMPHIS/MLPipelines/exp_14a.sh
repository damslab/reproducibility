#!/bin/bash
# Configs used (current results):
# 1. 38gb driver, 8 executors
# 2. Operation memory 19%, buffer pool 53%. Lineage cache 14% 
# 3. Use -XX:+UseParallelGC/-XX:+UseConcMarkSweepGC for GC in driver

rows=60000
cols=170

rm clean.dat
rm clean_noparfor.dat
rm clean_reuse.dat
rm clean_lima

echo "Starting cleaningalo enumeration  "
echo "----------------------------------- "
# time calculated in milliseconds

for scale in {1..100..20}
do
  runsparkinf -f aps_prep.dml -args $scale
  nrows=$(($rows*$scale))
  for rep in {1..3}
  do
    echo "Number of rows: $nrows, repetition: $rep"
    config2 all stop
    start=$(date +%s%N)
    runspark -f topkclean_aps_base.dml -stats
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> clean.dat

    start=$(date +%s%N)
    runspark -f topkclean_aps.dml -stats
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> clean_noparfor.dat

    # Disable multi-backend configuration for LIMA
    start=$(date +%s%N)
    runspark -f topkclean_aps.dml -stats -lineage reuse_full
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> clean_lima.dat

    config2 all start
    start=$(date +%s%N)
    runspark -f topkclean_aps.dml -stats -lineage reuse_multilevel
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> clean_reuse.dat
  done
done

exit

