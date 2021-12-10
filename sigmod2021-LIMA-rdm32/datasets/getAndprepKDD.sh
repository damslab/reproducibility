#!/bin/bash

# Download the dataset
rm KDD98.csv
wget https://kdd.ics.uci.edu/databases/kddcup98/epsilon_mirror/cup98lrn.txt.Z
gzip -d cup98lrn.txt.Z
mv cup98lrn.txt KDD98.csv
sed -i 's/-//g' KDD98.csv #remove hyphens

# Prepare and save for experiments
config parallelio stop
runjava -f KDD_prep.dml -stats
config parallelio start
