#/bin/bash

mkdir -p data/cat

# Cat in Dat dataset
if [[ ! -f "data/cat/train.csv" ]]; then
	cd data/cat
	kaggle competitions download cat-in-the-dat -f train.csv &
	kaggle competitions download cat-in-the-dat -f test.csv &
	wait
	unzip -p train.csv.zip > train_1.csv
	unzip -p test.csv.zip > test_1.csv
	rm train.csv.zip
	rm test.csv.zip
	kaggle competitions download cat-in-the-dat-ii -f train.csv &
	kaggle competitions download cat-in-the-dat-ii -f test.csv &
	wait
	unzip -p train.csv.zip > train_2.csv
	unzip -p test.csv.zip > test_2.csv
	rm train.csv.zip
	rm test.csv.zip
	sed -i -e 's/\.0//g' test_2.csv &
	sed -i -e 's/\.0//g' train_2.csv &
 	wait
	echo '{"data_type":"frame","format":"csv","sep":",","header":true}' >train_1.csv.mtd
	echo '{"data_type":"frame","format":"csv","sep":",","header":true}' >train_2.csv.mtd
	echo '{"data_type":"frame","format":"csv","sep":",","header":true}' >test_1.csv.mtd
	echo '{"data_type":"frame","format":"csv","sep":",","header":true}' >test_2.csv.mtd
	echo '{"data_type":"frame","format":"csv","sep":",","header":true}' >test.csv.mtd
	echo '{"data_type":"frame","format":"csv","sep":",","header":true}' >train.csv.mtd

	cd ../../

	## remove ID column
	awk '{sub(/[^,]*/,"");sub(/,/,"")} 1' data/cat/train_1.csv >data/cat/tmp.csv
	rm data/cat/train_1.csv
	mv data/cat/tmp.csv data/cat/train_1.csv
	awk '{sub(/[^,]*/,"");sub(/,/,"")} 1' data/cat/test_1.csv >data/cat/tmp.csv
	rm data/cat/test_1.csv
	mv data/cat/tmp.csv data/cat/test_1.csv
	awk '{sub(/[^,]*/,"");sub(/,/,"")} 1' data/cat/train_2.csv >data/cat/tmp.csv
	rm data/cat/train_2.csv
	mv data/cat/tmp.csv data/cat/train_2.csv
	awk '{sub(/[^,]*/,"");sub(/,/,"")} 1' data/cat/test_2.csv >data/cat/tmp.csv
	rm data/cat/test_2.csv
	mv data/cat/tmp.csv data/cat/test_2.csv

	cp data/cat/train_1.csv data/cat/train.csv
	cp data/cat/test_1.csv data/cat/test.csv
	tail -n+2 data/cat/train_2.csv >> data/cat/train.csv
	tail -n+2 data/cat/test_2.csv >> data/cat/test.csv
fi
