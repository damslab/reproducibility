#!/bin/bash
# Change to RC, DC, FH.

rows="500 1500 5000 15000 50000 150000 500000 1500000 5000000"

rm results/res_FH_rows_baseAll.dat
rm results/res_FH_rows_dmlAll.dat

echo "Starting speedup with #rows test"
echo "---------------------------------"
# time calculated in milliseconds

for nrow in $rows
do
  #ndist=$(($nrow/50))
  ndist=10000
  echo "Number of rows: $nrow, Number of distincts: $ndist"
  time python dataGenPL.py $nrow $ndist 5

  config partransform stop
  runjava -f micro_FH_rows.dml -stats
  # append the results to a central file
  cat results/res_FH_rows.dat >> results/res_FH_rows_baseAll.dat

  config partransform start
  runjava -f micro_FH_rows.dml -stats
  # append the results to a central file
  cat results/res_FH_rows.dat >> results/res_FH_rows_dmlAll.dat
done

rm results/*.mtd


exit
