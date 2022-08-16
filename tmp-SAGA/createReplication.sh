exp_num="data"
dataset=EEG1

pathout=$exp_num/
mkdir -p $pathout

runjava singlenode -f scripts/replication.dml -args data/${dataset}.csv ${pathout}/EEG 2>&1 | tee ${pathout}screen.txt
rm -v ${pathout}/*.mtd

