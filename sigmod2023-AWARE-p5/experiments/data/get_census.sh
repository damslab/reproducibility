#/bin/bash

echo "Beginning download of Census"

# Change directory to data.
if [[ pwd != *"data"* ]]; then
    cd "data"
fi

# Download file if not already downloaded.
if [[ ! -f "census/census.csv" ]]; then
    mkdir -p census/
    wget -nv -O census/census.csv https://archive.ics.uci.edu/ml/machine-learning-databases/census1990-mld/USCensus1990.data.txt
else
    echo "Census is already downloaded"
fi

if [[ ! -f "census/census.csv.mtd" ]]; then
    echo '{"format":csv,"header":true,"rows":2458285,"cols":69,"value_type":"int"}' > census/census.csv.mtd
else
    echo "Already constructed metadata for census.csv"
fi

# CD out of the data directory.
cd ..

if [[ ! -f "data/census/train_census.data.mtd" ]]; then
    systemds code/dataPrep/saveTrainCensus.dml &
else
    echo "Already saved training data census."
fi

if [[ ! -f "data/census/train_census_enc.data.mtd" ]]; then
    systemds code/dataPrep/dataprepUSCensus.dml &
else
    echo "Already saved encoded training data census."
fi

wait

echo "Census Download / Setup Done"

echo ""
echo ""
