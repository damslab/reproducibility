#echo
task=evalClassification 
sep=","
for test in  EEG 
do
  for resource in 10 20 30 40 50  
  do
  pathout=res/$test/
  mkdir -p $pathout
  start=$(date +%s%N)
  time -p runjava -f ../scripts/topkTest1.dml -stats -nvargs sep=$sep dirtyData=../data/$test/train.csv  metaData=../meta/meta_$test.csv\
    primitives=../properties/primitives.csv parameters=../properties/param.csv sample=1 topk=1 expectedIncrease=10 max_iter=15 rv=$resource\
    enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=$task output=${pathout}/  
  end=$(date +%s%N)
  echo $resource'\t'"$(cat ${pathout}/bestAcc.csv)" >> ${pathout}/bestAcc.dat 
  echo $resource'\t'$((($end-$start)/1000000)) >> ${pathout}/time.dat 
  done 
done

