#!/bin/bash

# https://archive.ics.uci.edu/ml/datasets/KDD+Cup+1998+Data

mkdir -p data/kdd98/

source parameters.sh

if [[ ! -f "data/kdd98/cup98val.csv" ]]; then
	# if [[ ! -f "data/kdd98/cup98lrn.txt.Z" ]]; then
	wget -O data/kdd98/cup98lrn.txt.Z https://kdd.ics.uci.edu/databases/kddcup98/epsilon_mirror/cup98lrn.txt.Z &
	wget -O data/kdd98/cup98val.txt.Z https://kdd.ics.uci.edu/databases/kddcup98/epsilon_mirror/cup98val.txt.Z &
	wget -O data/kdd98/cup98tar.csv https://kdd.ics.uci.edu/databases/kddcup98/epsilon_mirror/valtargt.txt &
	
	wait

	cd data/kdd98/
	gzip -d cup98lrn.txt.Z &
	gzip -d cup98val.txt.Z &

	wait 

	# Rename to CSV
	mv cup98lrn.txt cup98lrn.csv
	mv cup98val.txt cup98val.csv

	sed -i 's/-//g' cup98lrn.csv #remove hyphens
	sed -i 's/-//g' cup98val.csv #remove hyphens
	sed -i 's/ //g' cup98lrn.csv #remove whitespaces
	sed -i 's/ //g' cup98val.csv #remove whitespaces

	cd ../../
	python3 code/scripts/data/kdd_clean.py data/kdd98/cup98lrn.csv >> data/kdd98/cup98lrn2.csv
	python3 code/scripts/data/kdd_clean_val.py data/kdd98/cup98val.csv >> data/kdd98/cup98val2.csv
	cd data/kdd98/

	rm cup98lrn.csv 
	rm cup98val.csv
	mv cup98val2.csv cup98val.csv
	mv cup98lrn2.csv cup98lrn.csv


	echo '{"data_type":"frame","format":"csv","sep":",","header":true}' >cup98lrn.csv.mtd
	echo '{"data_type":"frame","format":"csv","sep":",","header":true}' >cup98val.csv.mtd

	# Fix validation to be like train with label column
	cd ../../
	python3 code/scripts/data/kdd_joinVal.py
	cd data/kdd98/
	rm cup98val.csv
	mv cup98valj.csv cup98val.csv
	cd ../../

	rm data/kdd98/cup98tar.csv

fi
