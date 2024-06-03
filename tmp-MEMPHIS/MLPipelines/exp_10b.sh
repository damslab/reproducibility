#!/bin/bash

# Scale movies_ratings with sf = 50
# Config: Operation memory = 0.19, buffer pool = 0.53, heap = 38gb, linage = 14%

rm pnmf.dat
rm pnmf_cp.dat
rm pnmf_cp_reuse.dat

echo "Starting matrix factorization using pnmf"
echo "---------------------------------------- "
# time calculated in milliseconds

for maxi in {5..50..5}
do
  for rep in {1..3}
  do
    echo "Number of iterations: $maxi, repetition: $rep"
    config2 all stop
    start=$(date +%s%N)
    runspark -f pnmf.dml -args $maxi -stats -explain
    end=$(date +%s%N)
    echo -e $maxi'\t'$((($end-$start)/1000000)) >> pnmf.dat

    config2 all start
    start=$(date +%s%N)
    runspark -f pnmf.dml -args $maxi -stats -explain
    end=$(date +%s%N)
    echo -e $maxi'\t'$((($end-$start)/1000000)) >> pnmf_cp.dat
    config2 all stop

    config2 all start
    start=$(date +%s%N)
    runspark -f pnmf.dml -args $maxi -stats -lineage reuse_full
    end=$(date +%s%N)
    echo -e $maxi'\t'$((($end-$start)/1000000)) >> pnmf_cp_reuse.dat
    config2 all stop
  done
done

exit

