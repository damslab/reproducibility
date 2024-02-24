#!/bin/bash

nrow=100000000 #100M
ncols=4 #hardcoded inside data generator
ndist=1000000 #spill out of cpu caches

rm rowpart_RC_dmlAll.dat
rm rowpart_BinH_dmlAll.dat
rm rowpart_BinW_dmlAll.dat
rm rowpart_FH_dmlAll.dat
rm rowpart_dml.dat

echo "Starting row partition test"
echo "----------------------------"
# time calculated in milliseconds

python3 dataGenString_4c.py $nrow $ndist 5
python3 dataGenFloat_4c.py $nrow $nrow
./config partransform start

for nBblk in 1 2 4 8 16 32 64 128
do
  nAblk=$((nBblk*2))
  echo "Block size: $nBblk/$nAblk"
  ./config buildblocks $nBblk
  ./config applyblocks $nAblk

  # append the results to a central file
  ./runjava -f rowpartition.dml -args 1 -stats
  cat rowpart_dml.dat >> rowpart_RC_dmlAll.dat
  ./runjava -f rowpartition.dml -args 2 -stats
  cat rowpart_dml.dat >> rowpart_BinH_dmlAll.dat
  ./runjava -f rowpartition.dml -args 3 -stats
  cat rowpart_dml.dat >> rowpart_BinW_dmlAll.dat
  ./runjava -f rowpartition.dml -args 4 -stats
  cat rowpart_dml.dat >> rowpart_FH_dmlAll.dat

done

./config buildblocks -1
./config applyblocks -1

rm *.mtd
rm rowpart_dml.dat
rm data.csv data2.csv

exit
