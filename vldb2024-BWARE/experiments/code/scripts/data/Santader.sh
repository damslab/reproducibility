#/bin/bash

mkdir -p data/santander

# Cat in Dat dataset
if [[ ! -f "data/santander/train.csv" ]]; then
  cd data/santander

  kaggle competitions download santander-customer-transaction-prediction -f train.csv &
  kaggle competitions download santander-customer-transaction-prediction -f test.csv &

  wait
  unzip -p train.csv.zip >train.csv &
  unzip -p test.csv.zip >test.csv &
  wait
  
  rm train.csv.zip
  rm test.csv.zip

  echo '{"data_type":"frame","format":"csv","sep":",","header":true}' > train.csv.mtd
  echo '{"data_type":"frame","format":"csv","sep":",","header":true}' > test.csv.mtd

  awk '{sub(/[^,]*/,"");sub(/,/,"")} 1' train.csv >train2.csv
  rm train.csv
  mv train2.csv train.csv

  cd ../..
fi
