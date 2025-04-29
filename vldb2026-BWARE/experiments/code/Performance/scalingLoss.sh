#!/bin/bash


cm="$SYSTEMDS_ROOT/target/systemds-3.2.0-SNAPSHOT-perf.jar"
main_class="org.apache.sysds.performance.micro.InformationLoss "

mem="-Xmx28g -Xms28g -Xmn2800m"
mkdir -p results/lossy_binning/
echo results/lossy_binning/santander_equi_width.csv
java $mem -cp $cm $main_class data/santander/train.csv equi-width > \
	results/lossy_binning/santander_equi_width.csv
echo results/lossy_binning/santander_equi_height.csv
java $mem -cp $cm $main_class data/santander/train.csv equi-height > \
  results/lossy_binning/santander_equi_height.csv
echo results/lossy_binning/santander_equi_height_approx.csv
java $mem -cp $cm $main_class data/santander/train.csv equi-height-approx > \
  results/lossy_binning/santander_equi_height_approx.csv

echo results/lossy_binning/crypto_equi_width.csv
java $mem -cp $cm $main_class data/crypto/train.csv equi-width > \
	results/lossy_binning/crypto_equi_width.csv
echo results/lossy_binning/crypto_equi_height.csv
java $mem -cp $cm $main_class data/crypto/train.csv equi-height > \
  results/lossy_binning/crypto_equi_height.csv
echo results/lossy_binning/crypto_equi_height_approx.csv
java $mem -cp $cm $main_class data/crypto/train.csv equi-height-approx > \
  results/lossy_binning/crypto_equi_height_approx.csv

