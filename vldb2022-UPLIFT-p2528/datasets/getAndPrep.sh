#!/bin/bash

# Usage: ./getAndPrep.sh <ID>
# e.g. ./getAndPrep.sh T2
# Note: Setup Kaggle API credentials to download the Kaggle datasets (https://github.com/Kaggle/kaggle-api)
# pip install kaggle
# Add ~/.local/bin to PATH
# Update KAGGLE_USERNAME and KAGGLE_KEY fields in .bash_profile or .bashrc

# Adult dataset
if [ "$1" = "T1" ]; then
  rm adult.data
  wget https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data
  sed -i '$ d' adult.data #remove empty line
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
  # https://criteo.wetransfer.com/downloads/4bbea9b4a54baddea549d71271a38e2c20230428071257/d4f0d2/grid
  mv day_21.gz criteo_day21.gz
  gzip -d criteo_day21.gz;
  if [ "$1" = "T3" -o "$1" = "T4" ]; then
    rm criteo_day21_10M
    rm criteo_day21_10M_cleaned
    # Copy first 10M rows
    head -10000000 criteo_day21 >> criteo_day21_10M
    # Replace tab with comma
    sed -i 's/\t/,/g' criteo_day21_10M
    python3 criteo_prep.py 10
  fi
  if [ "$1" = "T15" ]; then
    rm criteo_day21_5M
    # Copy first 5M rows
    head -5000000 criteo_day21 >> criteo_day21_5M
    # Replace tab with comma
    sed -i 's/\t/,/g' criteo_day21_5M
    python3 criteo_prep.py 5
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
    python3 aminerPL.py
  fi
  if [ "$1" = "T11" ]; then
    rm AminerAbstractSequence.csv 
    rm -rf wiki.en.vec wiki_metaframe wiki_embeddings_csv wiki_embeddings wiki_embeddings_csv.mtd wiki_words
    python3 aminerseq.py
    wget https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.en.vec
    python3 wiki_prep.py
    sed -i 's/['\''\"]//g' wiki_metaframe
    ./runjava -f wiki_csv2bin.dml
  fi
  rm *.zip
fi

# Synthetic dataset
if [ "$1" = "T12" ]; then
  rm data1.csv data2.csv
  python3 dataGenFloat.py 100000 100000
  python3 dataGenString.py 100000 10000 5
fi

# Synthetic datasets
if [ "$1" = "T13" -o "$1" = "T14" ]; then
  echo 'This synthetic dataset is dynamically created by the run script'
  echo 'No prior data prep is required'
fi

exit

