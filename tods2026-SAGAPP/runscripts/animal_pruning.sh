#!/bin/bash

echo -e "\nTop-k with SliceLine (sf = 1)"
echo "---------------------------------------"
runjava -f scripts/topkAnimal.dml -stats -nvargs sep="," dirtyData=../data/AnimalShelter/train.csv metaData=meta/meta_AnimalShelter.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=1 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=TRUE output=.
cat pip.csv

echo -e "\nScore pipeline (batch size = 64)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/AnimalShelter/train.csv  meta/meta_AnimalShelter.csv ./ FALSE evalClassification 3 4 4 64
# 3, 4, 4, 64 are start index, end index, pipeline size, and batch size.
# 3rd and 4th primitives together form the pruned mimimal set.

echo -e "\nScore pipeline (batch size = 128)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/AnimalShelter/train.csv  meta/meta_AnimalShelter.csv ./ FALSE evalClassification 3 4 4 128

echo -e "\nScore pipeline (batch size = 256)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/AnimalShelter/train.csv  meta/meta_AnimalShelter.csv ./ FALSE evalClassification 3 4 4 256

echo -e "\nScore pipeline (batch size = 512)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/AnimalShelter/train.csv  meta/meta_AnimalShelter.csv ./ FALSE evalClassification 3 4 4 512

echo -e "\nScore pipeline (batch size = 1024)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/AnimalShelter/train.csv  meta/meta_AnimalShelter.csv ./ FALSE evalClassification 3 4 4 1024

echo -e "\nScore pipeline (batch size = 2048)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/AnimalShelter/train.csv  meta/meta_AnimalShelter.csv ./ FALSE evalClassification 3 4 4 2048


sed -i '/WARN\|INFO/d' outAnimalPruning.log
