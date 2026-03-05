#!/bin/bash

# Run without SliceLine
#echo -e "\n1.Top-k without SliceLine (sf = 1)"
#echo "---------------------------------------"
#runjava -f scripts/topkNashville.dml -stats -nvargs sep="," dirtyData=../data/NashvilleTrafficAccidents/train.csv metaData=meta/meta_NashvilleTrafficAccidents.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=1 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=FALSE output=.
#cat pip.csv

#echo -e "\n2.Evaluate test without SliceLine (sf = 1)"
#echo "-----------------------------------------------"
#runjava -f scripts/evaluatePip.dml -stats -args "," ../data/NashvilleTrafficAccidents/train.csv ../data/NashvilleTrafficAccidents/test.csv meta/meta_NashvilleTrafficAccidents.csv ./ FALSE evalClassification .

echo -e "\n1.Top-k without SliceLine (sf = 0.5)"
echo "---------------------------------------"
runjava -f scripts/topkNashville.dml -stats -nvargs sep="," dirtyData=../data/NashvilleTrafficAccidents/train.csv metaData=meta/meta_NashvilleTrafficAccidents.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.5 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=FALSE output=.
cat pip.csv

echo -e "\n2.Evaluate test without SliceLine (sf = 0.5)"
echo "-----------------------------------------------"
runjava -f scripts/evaluatePip.dml -stats -args "," ../data/NashvilleTrafficAccidents/train.csv ../data/NashvilleTrafficAccidents/test.csv meta/meta_NashvilleTrafficAccidents.csv ./ FALSE evalClassification .

echo -e "\n1.Top-k without SliceLine (sf = 0.1)"
echo "---------------------------------------"
runjava -f scripts/topkNashville.dml -stats -nvargs sep="," dirtyData=../data/NashvilleTrafficAccidents/train.csv metaData=meta/meta_NashvilleTrafficAccidents.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.1 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=FALSE output=.
cat pip.csv

echo -e "\n2.Evaluate test without SliceLine (sf = 0.1)"
echo "-----------------------------------------------"
runjava -f scripts/evaluatePip.dml -stats -args "," ../data/NashvilleTrafficAccidents/train.csv ../data/NashvilleTrafficAccidents/test.csv meta/meta_NashvilleTrafficAccidents.csv ./ FALSE evalClassification .

echo -e "\n1.Top-k without SliceLine (sf = 0.01)"
echo "---------------------------------------"
runjava -f scripts/topkNashville.dml -stats -nvargs sep="," dirtyData=../data/NashvilleTrafficAccidents/train.csv metaData=meta/meta_NashvilleTrafficAccidents.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.01 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=FALSE output=.
cat pip.csv

echo -e "\n2.Evaluate test without SliceLine (sf = 0.01)"
echo "-----------------------------------------------"
runjava -f scripts/evaluatePip.dml -stats -args "," ../data/NashvilleTrafficAccidents/train.csv ../data/NashvilleTrafficAccidents/test.csv meta/meta_NashvilleTrafficAccidents.csv ./ FALSE evalClassification .

echo -e "\n1.Top-k without SliceLine (sf = 0.001)"
echo "---------------------------------------"
runjava -f scripts/topkNashville.dml -stats -nvargs sep="," dirtyData=../data/NashvilleTrafficAccidents/train.csv metaData=meta/meta_NashvilleTrafficAccidents.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.001 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=FALSE output=.
cat pip.csv

echo -e "\n2.Evaluate test without SliceLine (sf = 0.001)"
echo "-----------------------------------------------"
runjava -f scripts/evaluatePip.dml -stats -args "," ../data/NashvilleTrafficAccidents/train.csv ../data/NashvilleTrafficAccidents/test.csv meta/meta_NashvilleTrafficAccidents.csv ./ FALSE evalClassification .

#----------------------------------------------------------------------

# Run with SliceLine
#echo -e "\n3.Top-k with SliceLine (sf = 1)"
#echo "------------------------------------"
#runjava -f scripts/topkNashville.dml -stats -nvargs sep="," dirtyData=../data/NashvilleTrafficAccidents/train.csv metaData=meta/meta_NashvilleTrafficAccidents.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=1 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=TRUE output=.
#cat pip.csv

#echo -e "\n4.Evaluate test with SliceLine (sf = 1)"
#echo "-----------------------------------------"
#runjava -f scripts/evaluatePip.dml -stats -args "," ../data/NashvilleTrafficAccidents/train.csv ../data/NashvilleTrafficAccidents/test.csv meta/meta_NashvilleTrafficAccidents.csv ./ FALSE evalClassification .

echo -e "\n3.Top-k with SliceLine (sf = 0.5)"
echo "--------------------------------------"
runjava -f scripts/topkNashville.dml -stats -nvargs sep="," dirtyData=../data/NashvilleTrafficAccidents/train.csv metaData=meta/meta_NashvilleTrafficAccidents.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.5 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=TRUE output=.
cat pip.csv

echo -e "\n4.Evaluate test with SliceLine (sf = 0.5)"
echo -e "-------------------------------------------"
runjava -f scripts/evaluatePip.dml -stats -args "," ../data/NashvilleTrafficAccidents/train.csv ../data/NashvilleTrafficAccidents/test.csv meta/meta_NashvilleTrafficAccidents.csv ./ FALSE evalClassification .

echo -e "\n3.Top-k with SliceLine (sf = 0.1)"
echo "--------------------------------------"
runjava -f scripts/topkNashville.dml -stats -nvargs sep="," dirtyData=../data/NashvilleTrafficAccidents/train.csv metaData=meta/meta_NashvilleTrafficAccidents.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.1 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=TRUE output=.
cat pip.csv

echo -e "\n4.Evaluate test with SliceLine (sf = 0.1)"
echo "-------------------------------------------"
runjava -f scripts/evaluatePip.dml -stats -args "," ../data/NashvilleTrafficAccidents/train.csv ../data/NashvilleTrafficAccidents/test.csv meta/meta_NashvilleTrafficAccidents.csv ./ FALSE evalClassification .

echo -e "\n3.Top-k with SliceLine (sf = 0.01)"
echo "--------------------------------------"
runjava -f scripts/topkNashville.dml -stats -nvargs sep="," dirtyData=../data/NashvilleTrafficAccidents/train.csv metaData=meta/meta_NashvilleTrafficAccidents.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.01 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=TRUE output=.
cat pip.csv

echo -e "\n4.Evaluate test with SliceLine (sf = 0.01)"
echo "-------------------------------------------"
runjava -f scripts/evaluatePip.dml -stats -args "," ../data/NashvilleTrafficAccidents/train.csv ../data/NashvilleTrafficAccidents/test.csv meta/meta_NashvilleTrafficAccidents.csv ./ FALSE evalClassification .

echo -e "\n3.Top-k with SliceLine (sf = 0.001)"
echo "--------------------------------------"
runjava -f scripts/topkNashville.dml -stats -nvargs sep="," dirtyData=../data/NashvilleTrafficAccidents/train.csv metaData=meta/meta_NashvilleTrafficAccidents.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.001 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=TRUE output=.
cat pip.csv

echo -e "\n4.Evaluate test with SliceLine (sf = 0.001)"
echo "-------------------------------------------"
runjava -f scripts/evaluatePip.dml -stats -args "," ../data/NashvilleTrafficAccidents/train.csv ../data/NashvilleTrafficAccidents/test.csv meta/meta_NashvilleTrafficAccidents.csv ./ FALSE evalClassification .

sed -i '/WARN\|INFO/d' outNashville.log 
