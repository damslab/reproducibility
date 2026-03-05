#!/bin/bash
#
# Run without SliceLine
echo -e "\n1.Top-k without SliceLine (sf = 0.1)"
echo "-----------------------------------------"
runjava -f scripts/topkEEGResnet.dml -stats -nvargs sep="," dirtyData=../data/EEG/train.csv metaData=meta/meta_EEG.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.1 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=FALSE cvk=3 split=0.7 seed=42 func=evalResnet sliceline=FALSE output=.
cat pip.csv
cat evalHp.csv

echo -e "\n1.Top-k without SliceLine (sf = 0.01)"
echo "-----------------------------------------"
runjava -f scripts/topkEEGResnet.dml -stats -nvargs sep="," dirtyData=../data/EEG/train.csv metaData=meta/meta_EEG.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.01 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=FALSE cvk=3 split=0.7 seed=42 func=evalResnet sliceline=FALSE output=.
cat pip.csv
cat evalHp.csv


# Run with SliceLine
echo -e "\n3.Top-k with SliceLine (sf = 0.1)"
echo "--------------------------------------"
runjava -f scripts/topkEEGResnet.dml -stats -nvargs sep="," dirtyData=../data/EEG/train.csv metaData=meta/meta_EEG.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.5 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=FALSE cvk=3 split=0.7 seed=42 func=evalResnet sliceline=TRUE output=.
cat pip.csv
cat evalHp.csv

echo -e "\n3.Top-k with SliceLine (sf = 0.1)"
echo "--------------------------------------"
runjava -f scripts/topkEEGResnet.dml -stats -nvargs sep="," dirtyData=../data/EEG/train.csv metaData=meta/meta_EEG.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.1 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=FALSE cvk=3 split=0.7 seed=42 func=evalResnet sliceline=TRUE output=.
cat pip.csv
cat evalHp.csv

echo -e "\n3.Top-k with SliceLine (sf = 0.01)"
echo "---------------------------------------"
runjava -f scripts/topkEEGResnet.dml -stats -nvargs sep="," dirtyData=../data/EEG/train.csv metaData=meta/meta_EEG.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.01 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=FALSE cvk=3 split=0.7 seed=42 func=evalResnet sliceline=TRUE output=.
cat pip.csv
cat evalHp.csv


sed -i '/WARN\|INFO/d' outEEGResnet.log 
