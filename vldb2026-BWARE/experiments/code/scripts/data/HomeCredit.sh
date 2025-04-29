#/bin/bash

mkdir -p data/home/

source parameters.sh
if [[ ! -f "data/home/train.csv" ]]; then
    cd data/home
    kaggle competitions download home-credit-default-risk -f application_train.csv
    kaggle competitions download home-credit-default-risk -f application_test.csv
    unzip -p application_train.csv.zip >train.csv
    unzip -p application_test.csv.zip >test.csv
    echo '{"data_type":"frame","format":"csv","sep":",","header":true}' >train.csv.mtd
    echo '{"data_type":"frame","format":"csv","sep":",","header":true}' >test.csv.mtd
    rm -f t*.zip

		# remove id column
		awk '{sub(/[^,]*/,"");sub(/,/,"")} 1'  train.csv  > train2.csv
		rm train.csv
		mv train2.csv  train.csv

		awk '{sub(/[^,]*/,"");sub(/,/,"")} 1'  test.csv  > test2.csv
		rm test.csv
		mv test2.csv  test.csv
    cd ../../
fi
