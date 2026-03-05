#!/bin/bash

echo -e "\n3.Top-k with SliceLine (sf = 0.5)"
echo "--------------------------------------"
runjava -f scripts/topkNashville.dml -stats -nvargs sep="," dirtyData=../data/NashvilleTrafficAccidents/train.csv metaData=meta/meta_NashvilleTrafficAccidents.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.5 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=TRUE output=.
cat pip.csv

echo -e "\nScore pipeline (batch size = 32)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/NashvilleTrafficAccidents/train.csv  meta/meta_NashvilleTrafficAccidents.csv ./ FALSE evalClassification 5 6 6 32

echo -e "\nScore pipeline (batch size = 64)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/NashvilleTrafficAccidents/train.csv  meta/meta_NashvilleTrafficAccidents.csv ./ FALSE evalClassification 5 6 6 64
echo -e "\nScore pipeline (batch size = 128)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/NashvilleTrafficAccidents/train.csv  meta/meta_NashvilleTrafficAccidents.csv ./ FALSE evalClassification 5 6 6 128
echo -e "\nScore pipeline (batch size = 256)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/NashvilleTrafficAccidents/train.csv  meta/meta_NashvilleTrafficAccidents.csv ./ FALSE evalClassification 5 6 6 256
echo -e "\nScore pipeline (batch size = 512)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/NashvilleTrafficAccidents/train.csv  meta/meta_NashvilleTrafficAccidents.csv ./ FALSE evalClassification 5 6 6 512
echo -e "\nScore pipeline (batch size = 1024)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/NashvilleTrafficAccidents/train.csv  meta/meta_NashvilleTrafficAccidents.csv ./ FALSE evalClassification 5 6 6 1024
echo -e "\nScore pipeline (batch size = 2048)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/NashvilleTrafficAccidents/train.csv  meta/meta_NashvilleTrafficAccidents.csv ./ FALSE evalClassification 5 6 6 2048


sed -i '/WARN\|INFO/d' outNashvillePruning.log
