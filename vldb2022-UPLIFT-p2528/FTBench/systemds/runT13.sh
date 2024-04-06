#!/bin/bash

nrow=10000000 #10M
ncols=10 #hardcoded inside data generator
ndist=1000000 #1M. Don't fit in the cpu caches

rm stringlen_dml_baseAll.dat
rm stringlen_dmlAll.dat
rm stringlen_skAll.dat

echo "Starting string length test"
echo "----------------------------"
# time calculated in milliseconds

#source .venv/bin/activate
for nchar in {25..500..25}
do
  echo "String length: $nchar"
  python3 dataGenString_10c.py $nrow $ndist $nchar        #multi-threaded
#  python3 dataGen_single_threaded.py $nrow $ndist $nchar  #single-threaded

  ./config partransform stop
  ./runjava -f T13.dml
  # append the results to a central file
  cat stringlen_dml.dat >> stringlen_dml_baseAll.dat

  ./config partransform start
  ./runjava -f T13.dml
  # append the results to a central file
  cat stringlen_dml.dat >> stringlen_dmlAll.dat

  python3 ../scikit-learn/T13_sk.py
  # append the results to a central file
  cat stringlen_sk.dat >> stringlen_skAll.dat
done


exit
