
task=evalClassification
sep=","
dataset=EEG
input=rep/$dataset
for i in 1 2 3 4 5 6 7
do
  echo $input$i.csv 
  pathout=$exp_num/$dataset/4/
  mkdir -p $pathout
  start=$(date +%s%N)
  time -p ./runjava singlenode -f scripts/topkTest1.dml -nvargs sep=$sep dirtyData=$input$i.csv  metaData=meta/meta_$dataset.csv\
  primitives=properties/primitives.csv parameters=properties/param.csv sample=1 topk=3 expectedIncrease=10 max_iter=15 rv=50 seed=42 testCV=TRUE cvk=3 split=0.7 func=$task output=/tmp/
	end=$(date +%s%N)
	echo $i '\t' $((($end-$start)/1000000)) >> result/${dataset}_parallelism4_vldb.dat 
done | tee ${pathout}all.txt
