#!/bin/bash

# Download the dataset
rm aps_failure_training_set.csv aps_failure_test_set.csv
wget https://archive.ics.uci.edu/ml/machine-learning-databases/00421/aps_failure_training_set.csv
wget https://archive.ics.uci.edu/ml/machine-learning-databases/00421/aps_failure_test_set.csv
sed -i -e 1,20d aps_failure_training_set.csv #remove description
sed -i -e 1,20d aps_failure_test_set.csv

# Prepare and save for experiments
config parallelio stop
runjava -f APS_prep.dml -stats
config parallelio start
