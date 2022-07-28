#!/bin/bash

# Usage: ./getAndPrep.sh <ID>
# e.g. ./getAndPrep.sh T2
# Note: Setup Kaggle API credentials to download the Kaggle datasets

# Adult dataset
if [ "$1" = "T1" ]; then
  rm adult.data
  wget https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data
fi

# KDD 98 dataset
if [ "$1" = "T2" ]; then
  rm KDD98.csv
  wget https://kdd.ics.uci.edu/databases/kddcup98/epsilon_mirror/cup98lrn.txt.Z
  gzip -d cup98lrn.txt.Z
  mv cup98lrn.txt KDD98.csv
  sed -i 's/-//g' KDD98.csv #remove hyphens
fi

# Criteo dataset for day 21
if [ "$1" = "T3" -o "$1" = "T4" -o "$1" = "T15" ]; then
  curl https://storage.googleapis.com/criteo-cail-datasets/day_21.gz -o criteo_day21.gz
  gzip -d criteo_day21.gz;
  if [ "$1" = "T3" -o "$1" = "T4" ]; then
    rm criteo_day21_10M
    # Copy first 10M rows
    head -10000000 criteo_day21 >> criteo_day21_10M
    # Replace tab with comma
    sed -i 's/\t/,/g' criteo_day21_10M
  fi
  if [ "$1" = "T15" ]; then
    rm criteo_day21_5M
    # Copy first 5M rows
    head -5000000 criteo_day21 >> criteo_day21_5M
    # Replace tab with comma
    sed -i 's/\t/,/g' criteo_day21_5M
  fi
  rm *.gz
fi

# Santander bank dataset
if [ "$1" = "T5" ]; then
  rm santander.csv
  kaggle competitions download santander-customer-transaction-prediction -f train.csv
  unzip -p train.csv.zip > santander.csv
  rm *.zip
fi

# Crypto forcasting dataset
if [ "$1" = "T6" -o "$1" = "T7" ]; then
  rm crypto.csv
  kaggle competitions download g-research-crypto-forecasting -f train.csv
  unzip -p train.csv.zip > crypto.csv
  rm *.zip
fi

# Home credit default risk dataset
if [ "$1" = "T8" ]; then
  rm homeCreditTrain.csv homeCreditTest.csv
  kaggle competitions download home-credit-default-risk -f application_train.csv
  kaggle competitions download home-credit-default-risk -f application_test.csv
  unzip -p application_train.csv.zip > homeCreditTrain.csv
  unzip -p application_test.csv.zip > homeCreditTest.csv
  rm *.zip
fi

# Cat in Dat dataset
if [ "$1" = "T9" ]; then
  rm catindattrain.csv
  kaggle competitions download cat-in-the-dat -f train.csv
  unzip -p train.csv.zip > catindattrain.csv
  rm *.zip
fi

# AMiner citation dataset
if [ "$1" = "T10" -o "$1" = "T11" ]; then
  rm AminerCitation_small.txt
  wget wget https://lfs.aminer.cn/lab-datasets/citation/citation-network1.zip
  unzip -p citation-network1.zip > AminerCitation_small.txt
  if [ "$1" = "T10" ]; then
    rm AminerAbstract.csv
    python aminerPL.py
  fi
  if [ "$1" = "T11" ]; then
    rm AminerAbstractSequence.csv
    python aminerseq.py
  fi
  rm *.zip
fi

# Synthetic dataset
if [ "$1" = "T12" ]; then
  rm data1.csv data2.csv
  python dataGenFloat.py 100000 100000
  python dataGenString.py 100000 10000 5
fi

# Synthetic datasets
if [ "$1" = "T13" -o "$1" = "T14" ]; then
  echo 'This synthetic dataset is dynamically created by the run script'
  echo 'No prior data prep is required'
fi

exit

