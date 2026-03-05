#!/bin/bash

echo -e "\n1.Top-k without SliceLine (sf = 1)"
echo "---------------------------------------"
# Enable SliceLine (scale factor = 1.0) as that produces the best accuracy
runjava -f scripts/topkMovie.dml -stats -nvargs sep="," dirtyData=../data/movie/train.csv metaData=meta/meta_movie.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=1 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=TRUE output=.
cat pip.csv

# Rename the csv and csv.mtd files and copy them to this folder

echo -e "\nScore pipeline (batch size = 64)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/movie/train.csv  meta/meta_movie.csv ./ FALSE evalClassification 10 11 11 64 
# Last four parameters are start index, end index, pipeline size, and batch size.

echo -e "\nScore pipeline (batch size = 128)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/movie/train.csv  meta/meta_movie.csv ./ FALSE evalClassification 10 11 11 128 

echo -e "\nScore pipeline (batch size = 256)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/movie/train.csv  meta/meta_movie.csv ./ FALSE evalClassification 10 11 11 256 

echo -e "\nScore pipeline (batch size = 512)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/movie/train.csv  meta/meta_movie.csv ./ FALSE evalClassification 10 11 11 512 

echo -e "\nScore pipeline (batch size = 1024)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/movie/train.csv  meta/meta_movie.csv ./ FALSE evalClassification 10 11 11 1024 

echo -e "\nScore pipeline (batch size = 2048)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/movie/train.csv  meta/meta_movie.csv ./ FALSE evalClassification 10 11 11 2048 


sed -i '/WARN\|INFO/d' outMoviePruning.log
