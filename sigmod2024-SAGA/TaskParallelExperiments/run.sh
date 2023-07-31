hdfs dfs -mkdir TP-Data
hdfs dfs -put data/ TP-Data/
hdfs dfs -put meta/ TP-Data/
hdfs dfs -put properties/  TP-Data/

exp_num="task-parallel"
task=evalClassification
sep=","
test=AnimalShelter

echo $test "iteration "
pathout=archive/$exp_num/$test
rm -r $pathout
mkdir -p $pathout

time -p ./sparkDML.sh -exec singlenode -f topk_cleaning/topkTest1.dml -stats 30 -nvargs sep=$sep dirtyData=TP-Data/data/$test/train.csv \
  metaData=TP-Data/meta/meta_$test.csv  primitives=TP-Data/properties/primitives.csv parameters=TP-Data/properties/param.csv sample=1 topk=3 \
  expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 qu=0.9 ql=0.1 func=$task output=${pathout}// 2>&1  


