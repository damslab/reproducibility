#!/bin/bash

# Run without SliceLine
echo -e "\nTop-k without SliceLine (sf = 1)"
echo "---------------------------------------"
runjava -f scripts/topkAnimal.dml -stats -nvargs sep="," dirtyData=../data/AnimalShelter/train.csv metaData=meta/meta_AnimalShelter.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=1 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=FALSE output=.
cat pip.csv

echo -e "\nEvaluate test without SliceLine (sf = 1)"
echo "-----------------------------------------------"
runjava -f scripts/evaluatePip.dml -stats -args "," ../data/AnimalShelter/train.csv ../data/AnimalShelter/test.csv meta/meta_AnimalShelter.csv ./ FALSE evalClassification .

echo -e "\nTop-k without SliceLine (sf = 0.5)"
echo "---------------------------------------"
runjava -f scripts/topkAnimal.dml -stats -nvargs sep="," dirtyData=../data/AnimalShelter/train.csv metaData=meta/meta_AnimalShelter.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.5 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=FALSE output=.
cat pip.csv

echo -e "\nEvaluate test without SliceLine (sf = 0.5)"
echo "-----------------------------------------------"
runjava -f scripts/evaluatePip.dml -stats -args "," ../data/AnimalShelter/train.csv ../data/AnimalShelter/test.csv meta/meta_AnimalShelter.csv ./ FALSE evalClassification .

echo -e "\nTop-k without SliceLine (sf = 0.1)"
echo "---------------------------------------"
runjava -f scripts/topkAnimal.dml -stats -nvargs sep="," dirtyData=../data/AnimalShelter/train.csv metaData=meta/meta_AnimalShelter.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.1 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=FALSE output=.
cat pip.csv

echo -e "\nEvaluate test without SliceLine (sf = 0.1)"
echo "-----------------------------------------------"
runjava -f scripts/evaluatePip.dml -stats -args "," ../data/AnimalShelter/train.csv ../data/AnimalShelter/test.csv meta/meta_AnimalShelter.csv ./ FALSE evalClassification .

echo -e "\nTop-k without SliceLine (sf = 0.01)"
echo "---------------------------------------"
runjava -f scripts/topkAnimal.dml -stats -nvargs sep="," dirtyData=../data/AnimalShelter/train.csv metaData=meta/meta_AnimalShelter.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.01 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=FALSE output=.
cat pip.csv

echo -e "\nEvaluate test without SliceLine (sf = 0.01)"
echo "-----------------------------------------------"
runjava -f scripts/evaluatePip.dml -stats -args "," ../data/AnimalShelter/train.csv ../data/AnimalShelter/test.csv meta/meta_AnimalShelter.csv ./ FALSE evalClassification .

echo -e "\nTop-k without SliceLine (sf = 0.001)"
echo "---------------------------------------"
runjava -f scripts/topkAnimal.dml -stats -nvargs sep="," dirtyData=../data/AnimalShelter/train.csv metaData=meta/meta_AnimalShelter.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.001 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=FALSE output=.
cat pip.csv

echo -e "\nEvaluate test without SliceLine (sf = 0.001)"
echo "-----------------------------------------------"
runjava -f scripts/evaluatePip.dml -stats -args "," ../data/AnimalShelter/train.csv ../data/AnimalShelter/test.csv meta/meta_AnimalShelter.csv ./ FALSE evalClassification .



# Run with SliceLine
echo -e "\nTop-k with SliceLine (sf = 1)"
echo "---------------------------------------"
runjava -f scripts/topkAnimal.dml -stats -nvargs sep="," dirtyData=../data/AnimalShelter/train.csv metaData=meta/meta_AnimalShelter.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=1 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=TRUE output=.
cat pip.csv

echo -e "\nEvaluate test with SliceLine (sf = 1)"
echo "-----------------------------------------------"
runjava -f scripts/evaluatePip.dml -stats -args "," ../data/AnimalShelter/train.csv ../data/AnimalShelter/test.csv meta/meta_AnimalShelter.csv ./ FALSE evalClassification .

echo -e "\nTop-k with SliceLine (sf = 0.5)"
echo "---------------------------------------"
runjava -f scripts/topkAnimal.dml -stats -nvargs sep="," dirtyData=../data/AnimalShelter/train.csv metaData=meta/meta_AnimalShelter.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.5 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=TRUE output=.
cat pip.csv

echo -e "\nEvaluate test with SliceLine (sf = 0.5)"
echo "-----------------------------------------------"
runjava -f scripts/evaluatePip.dml -stats -args "," ../data/AnimalShelter/train.csv ../data/AnimalShelter/test.csv meta/meta_AnimalShelter.csv ./ FALSE evalClassification .

echo -e "\nTop-k with SliceLine (sf = 0.1)"
echo "---------------------------------------"
runjava -f scripts/topkAnimal.dml -stats -nvargs sep="," dirtyData=../data/AnimalShelter/train.csv metaData=meta/meta_AnimalShelter.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.1 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=TRUE output=.
cat pip.csv

echo -e "\nEvaluate test with SliceLine (sf = 0.1)"
echo "-----------------------------------------------"
runjava -f scripts/evaluatePip.dml -stats -args "," ../data/AnimalShelter/train.csv ../data/AnimalShelter/test.csv meta/meta_AnimalShelter.csv ./ FALSE evalClassification .

echo -e "\nTop-k with SliceLine (sf = 0.01)"
echo "---------------------------------------"
runjava -f scripts/topkAnimal.dml -stats -nvargs sep="," dirtyData=../data/AnimalShelter/train.csv metaData=meta/meta_AnimalShelter.csv primitives=properties/primitives.csv parameters=properties/param.csv sample=0.01 topk=3 expectedIncrease=10 max_iter=15 rv=50 enablePruning=TRUE testCV=TRUE cvk=3 split=0.7 seed=42 func=evalClassification sliceline=TRUE output=.
cat pip.csv

echo -e "\nEvaluate test with SliceLine (sf = 0.01)"
echo "-----------------------------------------------"
runjava -f scripts/evaluatePip.dml -stats -args "," ../data/AnimalShelter/train.csv ../data/AnimalShelter/test.csv meta/meta_AnimalShelter.csv ./ FALSE evalClassification .


sed -i '/WARN\|INFO/d' outAnimal.log
