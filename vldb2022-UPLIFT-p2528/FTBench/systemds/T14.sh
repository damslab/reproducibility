#!/bin/bash
# Set build, apply blocks to 10

nrow=100000000 #100M
ncols=4 #hardcoded inside data generator
nchar=5

rm results/numdistinct_dml_baseAll.dat
rm results/numdistinct_dmlAll.dat
rm results/numdistinct_skAll.dat

echo "Starting #distinct values test"
echo "-------------------------------"
# time calculated in milliseconds

source .venv/bin/activate
for ndist in {100000..1000000..100000} #100K to 1M
do
  echo "Number of distinct values: $ndist"
  python ../utils/dataGenPL.py $nrow $ndist $nchar

  config partransform stop
  runjava -f T14.dml -stats
  # append the results to a central file
  cat results/numdistinct_dml.dat >> results/numdistinct_dml_baseAll.dat

  config partransform start
  runjava -f T14.dml -stats
  # append the results to a central file
  cat results/numdistinct_dml.dat >> results/numdistinct_dmlAll.dat

  python T14_sk.py
  # append the results to a central file
  cat results/numdistinct_sk.dat >> results/numdistinct_skAll.dat
done
deactivate

rm results/*.mtd


exit
