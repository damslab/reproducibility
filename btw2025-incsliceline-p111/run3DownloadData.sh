#!/bin/bash

# This script downloads all real datasets shown in Table 1 of the paper
# The remaining datasets are then created via replicating some of these datasets

mkdir -p data;
chmod 755 data;

# Adult
curl https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data -o data/Adult.csv;
sed -i '$d' data/Adult.csv; # fix empty line at end of file

# Covtype
curl https://archive.ics.uci.edu/ml/machine-learning-databases/covtype/covtype.data.gz -o data/covtype.data.gz;
gzip -d data/covtype.data.gz;
mv data/covtype.data data/Covtype.csv;

# KDD'98
curl https://archive.ics.uci.edu/ml/machine-learning-databases/kddcup98-mld/epsilon_mirror/cup98lrn.zip -o data/cup98lrn.zip;
unzip data/cup98lrn.zip -d data;
mv data/cup98LRN.txt data/KDD98.csv
rm data/cup98lrn.zip;
sed -i 's/-/ /g' data/KDD98.csv; # fix suffix - at 5th column (numerical)
# note: workaround for macOS issue: sed -i '' 's/-/ /g' data/KDD98.csv;

# US Census
# reused existing data because no longer existing in UCI repo
curl https://tubcloud.tu-berlin.de/s/yWafF6pnZ6Ywdok/download/USCensus.csv -o data/USCensus.csv

