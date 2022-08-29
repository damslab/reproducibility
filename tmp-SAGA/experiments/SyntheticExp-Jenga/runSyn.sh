#!/bin/bash

exp="topkSyn"
task=mar
for data in  food 
do
  for i in 0.1 0.2 0.3 0.4
  do 
    echo "executing " $data $i $task
    pathin=syntheticTopk/$data/$task/${data}_${task}_${i}.csv
    pathout=../archive/$exp/$data/$task/$i
    mkdir -p $pathout
    runjava singlenode  -f V1/topkTestMVI.dml -stats -nvargs  sep="," dirtyData=$pathin  metaData=meta/meta_${data}.csv\
      primitives=properties/primitivesMVI.csv parameters=properties/paramMVI.csv expectedIncrease=0.1 max_iter=5 sample=1 topk=3 rv=10 testCV=FALSE cvk=5\
      func="evalClassification" split=0.7 seed=-1 output=${pathout}/ 2>&1  | tee ${pathout}/screen.txt
    rm -v ${pathout}/*.mtd
  done 
done  


task=mcar
for data in  food 
do
  for i in 0.1 0.2 0.3 0.4
  do 
    echo "executing " $data $i $task
    pathin=syntheticTopk/$data/$task/${data}_${task}_${i}.csv
    pathout=../archive/$exp/$data/$task/$i
    mkdir -p $pathout
    runjava singlenode  -f V1/topkTestMVI.dml -stats -nvargs  sep="," dirtyData=$pathin  metaData=meta/meta_${data}.csv\
      primitives=properties/primitivesMVI.csv parameters=properties/paramMVI.csv expectedIncrease=0.1 max_iter=5 sample=1 topk=3 rv=10 testCV=FALSE cvk=5\
      func="evalClassification" split=0.7 seed=-1 output=${pathout}/ 2>&1  | tee ${pathout}/screen.txt
    rm -v ${pathout}/*.mtd
  done 
done  

