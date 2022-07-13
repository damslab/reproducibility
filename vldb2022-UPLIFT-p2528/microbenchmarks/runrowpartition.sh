#!/bin/bash
# Note: This script doesn't work yet. 
# Set build, apply blocks to 10

nrow=100000000 #100M
ncols=4 #hardcoded inside data generator
ndist=1000000 #spill out of cpu caches

rm results/rowpart_dml_baseAll.dat
rm results/rowpart_dmlAll.dat

echo "Starting row partition test"
echo "----------------------------"
# time calculated in milliseconds

python dataGenPL.py $nrow $ndist 5

for nblk in 1 10 20 30 40 50 60 70 80 90 100
do
  echo "Block size: $nblk"
  config partransform start
  runjava -f rowpartition.dml
  # append the results to a central file
  cat results/rowpart_dml.dat >> results/rowpart_dml_baseAll.dat

  config partransform start
  runjava -f rowpartition.dml
  # append the results to a central file
  cat results/rowpart_dml.dat >> results/rowpart_dmlAll.dat

  python rowpart_sk.py
  # append the results to a central file
  cat results/rowpart_sk.dat >> results/rowpart_skAll.dat
done

rm results/*.mtd


exit
