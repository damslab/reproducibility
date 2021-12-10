#!/bin/bash

rows=100000
cols=1000
sp=1.0

rm resGridL2svm.dat
rm resGridL2svm_reuse.dat
# time calculated in milliseconds

echo "Starting (9a) Hyper-parameter tuning for L2SVM"
echo "----------------------------------------------"

for j in {0..70..10}
do
  if [[ $j -eq 0 ]];
    then num_lamda=$(($j+1))
    else num_lamda=$j
  fi
  echo "Number of lamdas = $num_lamda"
  echo "-----------------------------"
  for rep in {1..3}
    do
    start=$(date +%s%N)
    runjava -f gridsearchl2svm.dml -stats -args $rows $cols $sp $num_lamda
    end=$(date +%s%N)
    echo -e $rows'\t'$cols'\t'$num_lamda'\t'$((($end-$start)/1000000)) >> resGridL2svm.dat

    start=$(date +%s%N)
    runjava -f gridsearchl2svm.dml -lineage reuse_hybrid -stats -args $rows $cols $sp $num_lamda
    end=$(date +%s%N)
    echo -e $rows'\t'$cols'\t'$num_lamda'\t'$((($end-$start)/1000000)) >> resGridL2svm_reuse.dat
  done
done

exit

