#!/bin/bash

nrow=100000000 #100M
ncols=4 #hardcoded inside data generator
nchar=5

rm numdistinct_dml_baseAll.dat
rm numdistinct_dmlAll.dat
rm numdistinct_skAll.dat

echo "Starting #distinct values test"
echo "-------------------------------"
# time calculated in milliseconds

#source .venv/bin/activate
for ndist in {100000..1000000..100000} #100K to 1M
do
  echo "Number of distinct values: $ndist"
  python3 dataGenString_4c.py $nrow $ndist $nchar

  ./config partransform stop
  ./runjava -f T14.dml -stats
  # append the results to a central file
  cat numdistinct_dml.dat >> numdistinct_dml_baseAll.dat

  ./config partransform start
  ./runjava -f T14.dml -stats
  # append the results to a central file
  cat numdistinct_dml.dat >> numdistinct_dmlAll.dat

  python3 ../scikit-learn/T14_sk.py
  # append the results to a central file
  cat numdistinct_sk.dat >> numdistinct_skAll.dat
done
#deactivate


exit
