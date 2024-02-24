#!/bin/bash

threads="1 2 4 8 16 32"

rm res_RC_*.dat
rm res_DC_*.dat
rm res_FH_*.dat

echo "Starting speedup with #threads test"
echo "------------------------------------"
# time calculated in milliseconds

python3 dataGenString_100c.py 5000000 100000 5
./config partransform start
for nth in $threads
do
  echo "Thread count: $nth"
  ./config transformthreads $nth

  ./runjava -f micro_RC_threads.dml -args $nth -stats
  ./runjava -f micro_DC_threads.dml -args $nth -stats
  ./runjava -f micro_FH_threads.dml -args $nth -stats
done

./config transformthreads -1 
rm *.mtd

exit
