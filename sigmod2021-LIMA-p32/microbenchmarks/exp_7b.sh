#!/bin/bash

nrows=50000
cols=1000

rm resmicromultirepeat.dat
rm resmicromultirepeat_reuse.dat
rm resmicromultirepeat_reuse_multilvl.dat

# time calculated in milliseconds

echo "Starting (7b) Multi-level Reuse microbenchmark"
echo "----------------------------------------------"

for nrep in {0..20..5}
do
  if [[ $nrep -eq 0 ]];
    then repc=$(($nrep+1))
    else repc=$nrep
  fi
  for rep in {1..3}
  do
    echo "$nrows num of rows and $rep repetition"
    start=$(date +%s%N)
    runjava -f micro_multi.dml -args $repc -stats 
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$repc'\t'$((($end-$start)/1000000)) >> resmicromultirepeat.dat

    start=$(date +%s%N)
    runjava -f micro_multi.dml -args $repc -lineage reuse_full -stats 
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$repc'\t'$((($end-$start)/1000000)) >> resmicromultirepeat_reuse.dat

    start=$(date +%s%N)
    runjava -f micro_multi.dml -args $repc -lineage reuse_multilevel -stats 
    end=$(date +%s%N)
    echo -e $nrows'\t'$cols'\t'$repc'\t'$((($end-$start)/1000000)) >> resmicromultirepeat_reuse_multilvl.dat
  done

done


exit
