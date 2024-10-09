#!/bin/bash
# Takes ~48 hours to complete (w/ 3 reps)
# Configs used (current results):
# 1. 38gb driver, 8 executors
# 2. Operation memory 19%, buffer pool 53%. Lineage cache 14% 
# 3. Use -XX:+UseParallelGC/-XX:+UseConcMarkSweepGC for GC in driver

rows=540000
cols=2500

rm cvlm.dat
rm cvlm_async.dat
rm cvlm_reuse.dat
rm cvlm_async_reuse.dat
rm cvlm_reuse_lima.dat

echo "Starting grid search CVLM  "
echo "-------------------------- "
# time calculated in milliseconds

for scale in {0..10..1}
do
   if [[ $scale -eq 0 ]];
    then nrows=$(($rows/2))
    else nrows=$(($rows*$scale))
  fi
  for rep in {1..3}
  do
    echo "Number of rows: $nrows, repetition: $rep"
    config2 all stop
    start=$(date +%s%N)
    runspark -f cvlm.dml -args $nrows -stats
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> cvlm.dat

    config2 all start
    start=$(date +%s%N)
    runspark -f cvlm.dml -args $nrows -stats
    end=$(date +%s%N)
    config2 all stop
    echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> cvlm_async.dat

    # Disable multi-backend reuse configuration for LIMA
    start=$(date +%s%N)
    runspark -f cvlm.dml -args $nrows -stats -lineage reuse_full
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> cvlm_reuse_lima.dat

    start=$(date +%s%N)
    runspark -f cvlm.dml -args $nrows -stats -lineage reuse_multilevel
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> cvlm_reuse.dat

    config2 all start
    start=$(date +%s%N)
    runspark -f cvlm.dml -args $nrows -stats -lineage reuse_multilevel
    end=$(date +%s%N)
    config2 all stop
    echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> cvlm_async_reuse.dat
  done
done

exit

