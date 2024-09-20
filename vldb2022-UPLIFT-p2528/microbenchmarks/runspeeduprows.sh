#!/bin/bash

rows="500 1500 5000 15000 50000 150000 500000 1500000 5000000"

rm res*rows.dat

echo "Starting speedup with #rows test"
echo "---------------------------------"
# time calculated in milliseconds

for nrow in $rows
do
  #ndist=$(($nrow/50))
  ndist=10000
  echo "Number of rows: $nrow, Number of distincts: $ndist"
  python3 dataGenString_100c.py $nrow $ndist 5

  ./config partransform stop
  ./runjava -f micro_RC_rows.dml -stats
  ./runjava -f micro_DC_rows.dml -stats
  ./runjava -f micro_FH_rows.dml -stats
  # append the results to a central file
  cat res_RC_rows.dat >> res_RC_rows_baseAll.dat
  cat res_DC_rows.dat >> res_DC_rows_baseAll.dat
  cat res_FH_rows.dat >> res_FH_rows_baseAll.dat

  ./config partransform start
  ./runjava -f micro_RC_rows.dml -stats
  ./runjava -f micro_DC_rows.dml -stats
  ./runjava -f micro_FH_rows.dml -stats
  # append the results to a central file
  cat res_RC_rows.dat >> res_RC_rows_dmlAll.dat
  cat res_DC_rows.dat >> res_DC_rows_dmlAll.dat
  cat res_FH_rows.dat >> res_FH_rows_dmlAll.dat
done

rm *.mtd


exit
