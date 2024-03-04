#/bin/bash

# https://gitlab.com/scilab/forge/rdataset/-/blob/master/doc/car/Salaries.html?ref_type=heads

mkdir -p data/salaries/

if [[ ! -f "data/salaries/train.csv" ]]; then
	wget https://gitlab.com/scilab/forge/rdataset/-/raw/master/csv/car/Salaries.csv?ref_type=heads \
		-O data/salaries/train.csv

	echo '{"data_type":"frame","format":"csv","sep":",","header":true}' >data/salaries/train.csv.mtd
	awk '{sub(/[^,]*/,"");sub(/,/,"")} 1' data/salaries/train.csv >data/salaries/tmp.csv
	rm data/salaries/train.csv
	sed -i 's/\"//g' data/salaries/train.csv
	mv data/salaries/tmp.csv data/salaries/train.csv
fi
