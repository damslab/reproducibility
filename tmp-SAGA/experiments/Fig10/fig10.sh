#echo
task=evalClassification 
sep=","
for test in  EEG 
do
  for iter in 5 10 15 20 25  
  do
  pathout=res/$test/
  mkdir -p $pathout
  start=$(date +%s%N)
  time -p runjava -f ../scripts/topkTest1.dml -stats -nvargs sep=$sep dirtyData=../data/$test/train.csv  metaData=../meta/meta_$test.csv\
    primitives=../properties/primitives.csv parameters=../properties/param.csv sample=1 topk=1 expectedIncrease=10 max_iter=$iter rv=50\
    enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=$task output=${pathout}/  
  end=$(date +%s%N)
  echo $iter'\t'"$(cat ${pathout}/bestAcc.csv)" >> ${pathout}/bestAcc.dat 
  echo $iter'\t'$((($end-$start)/1000000)) >> ${pathout}/time.dat 
  done 
done

