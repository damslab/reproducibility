#!/bin/bash

mkdir -p data/softdefect

if [[ ! -f "data/softdefect/train.csv" ]]; then 
	cd data/softdefect 
	kaggle competitions download -c playground-series-s3e23
	unzip playground-series-s3e23.zip
	echo '{"data_type":"frame","format":"csv","sep":",","header":true}' > test.csv.mtd
	echo '{"data_type":"frame","format":"csv","sep":",","header":true}' > train.csv.mtd
	awk '{sub(/[^,]*/,"");sub(/,/,"")} 1' test.csv >tmp.csv
	mv tmp.csv test.csv
	awk '{sub(/[^,]*/,"");sub(/,/,"")} 1' train.csv >tmp.csv
	mv tmp.csv train.csv
	cd ../..
fi 