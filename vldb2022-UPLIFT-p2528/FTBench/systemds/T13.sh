#!/bin/bash
# Set build, apply blocks to 10

nrow=10000000 #10M
ncols=10 #hardcoded inside data generator
ndist=1000000 #1M. Spill out of cpu caches

rm results/stringlen_dml_baseAll.dat
rm results/stringlen_dmlAll.dat
rm results/stringlen_skAll.dat

echo "Starting string length test"
echo "----------------------------"
# time calculated in milliseconds

source .venv/bin/activate
for nchar in {25..500..25}
do
  echo "String length: $nchar"
  python ../utils/dataGenPL.py $nrow $ndist $nchar

  config partransform stop
  runjava -f T13.dml
  # append the results to a central file
  cat results/stringlen_dml.dat >> results/stringlen_dml_baseAll.dat

  config partransform start
  runjava -f T13.dml
  # append the results to a central file
  cat results/stringlen_dml.dat >> results/stringlen_dmlAll.dat

  python T13_sk.py
  # append the results to a central file
  cat results/stringlen_sk.dat >> results/stringlen_skAll.dat
done

rm results/*.mtd


exit
