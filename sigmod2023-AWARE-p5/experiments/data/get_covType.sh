#/bin/bash

echo "Downloading Covtype"

# Change directory to data.
if [[ $(pwd) != *"data"* ]]; then
    cd "data"
fi

# Download file if not already downloaded.
if [[ ! -f "covtype/covtype.data" ]]; then
    mkdir -p covtype/
    wget -nv -O covtype/covtype.data.gz http://archive.ics.uci.edu/ml/machine-learning-databases/covtype/covtype.data.gz
    cd covtype/
    gunzip "covtype.data.gz"
    echo '{"format":csv,"header":false,"rows":581012,"cols":55,"value_type":"int"}' > covtype.data.mtd
    cd ..
else 
    echo "Covtype already downloaded"
fi

# Go out of data dir.
cd ..

# Activate python venv
source parameters.sh

if [[ ! -f "data/covtype/train_covtype.data" ]]; then
    systemds code/dataPrep/saveTrainCovType.dml &
else
    echo "Already setup  train_covtype"
fi

if [[ ! -f "data/covtypeNew/train_covtypeNew.data" ]]; then
    systemds code/dataPrep/saveTrainCovTypeNew.dml &
else
   echo "Already setup train_covtype new format ... (predicting cov type)"
fi

if [[ ! -f "data/covtype/removecol1.csv" ]]; then
    python code/dataPrep/make_csv_covtype.py &
else
    echo "Saving covtype training as csv already done."
fi

wait

echo "CovType Setup Done"

echo ""
echo ""