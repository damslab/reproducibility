#!/bin/bash

echo -e "\n1.Top-k without SliceLine (sf = 1)"
echo "---------------------------------------"
runjava -f scripts/topkPuma.dml -stats -nvargs sep="," dirtyData=../data/puma/train.csv metaData=meta/meta_puma.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=1 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=FALSE output=.
cat pip.csv

echo -e "\nScore pipeline (batch size = 64)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/puma/train.csv  meta/meta_puma.csv ./ FALSE evalClassification 2 3 5 64
# 2, 3, 5, 64 are start index, end index, pipeline size, and batch size.
# 2nd and 3rd primitives together form the pruned mimimal set.

echo -e "\nScore pipeline (batch size = 128)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/puma/train.csv  meta/meta_puma.csv ./ FALSE evalClassification 2 3 5 128

echo -e "\nScore pipeline (batch size = 256)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/puma/train.csv  meta/meta_puma.csv ./ FALSE evalClassification 2 3 5 256

echo -e "\nScore pipeline (batch size = 512)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/puma/train.csv  meta/meta_puma.csv ./ FALSE evalClassification 2 3 5 512

echo -e "\nScore pipeline (batch size = 1024)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/puma/train.csv  meta/meta_puma.csv ./ FALSE evalClassification 2 3 5 1024

echo -e "\nScore pipeline (batch size = 2048)"
echo "-----------------------------------------"
runjava -f scripts/evaluate_batch.dml -stats -args "," ../data/puma/train.csv  meta/meta_puma.csv ./ FALSE evalClassification 2 3 5 2048


sed -i '/WARN\|INFO/d' outPumaPruning.log
