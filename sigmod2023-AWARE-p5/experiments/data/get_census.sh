#/bin/bash

# Change directory to data.
if [[ pwd != *"data"* ]]; then
    cd "data"
fi

# Download file if not already downloaded.
if [[ ! -f "census/census.csv" ]]; then
    mkdir -p census/
    wget -nv -O census/census.csv https://archive.ics.uci.edu/ml/machine-learning-databases/census1990-mld/USCensus1990.data.txt
fi

# if [[ ! -f "census/census.csv.mtd" ]]; then
#     echo '{"format":csv,"header":true,"rows":2458285,"cols":69,"value_type":"int"}' > census/census.csv.mtd
# fi

# cd ..
if [[ ! -f "data/census/train_census.data.mtd" ]]; then
    systemds code/dataPrep/saveTrainCensus.dml &
fi

if [[ ! -f "data/census/train_census_enc.data.mtd" ]] then
    systemds code/dataPrep/dataprepUSCensus.dml
fi


# if [[ ! -f "data/covtypeNew/train_covtypeNew.data" ]]; then
#     systemds code/dataPrep/saveTrainCovTypeNew.dml &
# fi

# if [[ ! -f "data/covtype/removecol1.csv" ]]; then
#     python code/dataPrep/make_csv_covtype.py &
# fi

wait

echo "Census Setup Done"