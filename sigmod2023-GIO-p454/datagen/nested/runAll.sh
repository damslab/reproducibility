#!/usr/bin/env bash

aminer_in_path="/home/saeed/Documents/Datasets/AMiner/"
yelp_in_path="/home/saeed/Documents/Datasets/yelp/yelp-json.dat"
rewastef_in_path="na"
sample_nrows="200,300,400,500,600,700,800,900,1000"
out_path="/home/saeed/Documents/tmp/Examples/" #"../data/"

mkdir -p $out_path
./makeClean.sh

# cleanup
#rm -rf ../data/yelp-json
#rm -rf ../data/yelp-csv
#rm -rf ../data/aminer-author-json
#rm -rf ../data/aminer-paper-json
#rm -rf ../data/higgs-csv
#rm -rf ../data/mnist8m-libsm
#rm -rf ../data/susy-libsvm
#rm -rf ../data/relat9-mm
#rm -rf ../data/queen-mm
#rm -rf ../data/moliere-mm


#./aminer.sh $aminer_in_path $sample_nrows $out_path
#./matrix.sh $sample_nrows $out_path
./yelp.sh $yelp_in_path $sample_nrows $out_path
#./rewastef.sh $rewastef_in_path $sample_nrows $out_path

#rm -rf ../data/yelp-json.dat
#rm -rf ../data/yelp-csv.dat
#rm -rf ../data/aminer-author-json.dat
#rm -rf ../data/aminer-paper-json.dat
#
#mv ../data/yelp-json/yelp-json.dat ../data/
#mv ../data/yelp-csv/yelp-csv.dat ../data/
#mv ../data/aminer-author-json/aminer-author-json.dat ../data/
#mv ../data/aminer-paper-json/aminer-paper-json.dat ../data/

