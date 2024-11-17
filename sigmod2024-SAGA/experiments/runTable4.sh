#echo
task=evalClassificationMSVM
sep=","
for test in EEG 
do
  for i in 1 2 3
  do
  echo $test "iteration " $i
  pathout=output/table2/
  mkdir -p $pathout
  ./runjava -f ./scripts/topkTest1.dml -stats -nvargs sep=$sep dirtyData=../data/$test/train.csv  metaData=./meta/meta_$test.csv\
    primitives=./properties/primitives.csv parameters=./properties/param.csv sample=1 topk=3 expectedIncrease=10 max_iter=15 rv=50\
    enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=-1 func=$task output=${pathout}/ 2>&1  

  ./runjava -f ./scripts/evaluatePip.dml -stats -args $sep ../data/$test/train.csv  ../data/$test/test.csv  ./meta/meta_$test.csv\
    ${pathout}/ FALSE $task ${pathout}/ 2>&1 | tee ${pathout}/screenEval.txt 
  done
done 
