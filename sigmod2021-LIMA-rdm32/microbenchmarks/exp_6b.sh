#!/bin/bash

rows="2 4 8 128 512 2048"
cols=784
iter="10000 5000 2500 156 39 9"

rm reslinMem.dat 
rm reslinMem_lineage.dat 
rm reslinMem_dedup.dat
rm stdout
# Mem calculated in bytes

echo "Starting (6b) Space Overhead microbenchmark"
echo "--------------------------------------------"

set $iter
for i in $rows
do
  for rep in {1..3}
  do
    runjava_mem -f micro_linCost.dml -stats -args $i $1 >> stdout

    runjava_mem -f micro_linCost.dml -stats -lineage -args $i $1 >> stdout

    runjava_mem -f micro_linCost.dml -stats -lineage dedup -args $i $1 >> stdout 
  done
  shift
done

#Extract the numbers from the output file
grep "Max memory" stdout|sed -n '1~3'p|awk '{print $3}'>reslinMem.dat
grep "Max memory" stdout|sed -n '2~3'p|awk '{print $3}'>reslinMem_lineage.dat
grep "Max memory" stdout|sed -n '3~3'p|awk '{print $3}'>reslinMem_dedup.dat
#Note: sed option first~step -> every step'th line starting with line first

rm stdout
