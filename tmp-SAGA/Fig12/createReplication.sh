exp_num="data"


mkdir -p rep

runjava singlenode -f scripts/replication.dml -args ../data/EEG/train.csv ../data/EEG/test.csv 
rm -v ${pathout}/*.mtd

