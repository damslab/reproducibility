#!/bin/bash
set -e   # fail on any error
echo "Beginning download of Adult Dataset"
 
mkdir -p ../10_data
cd ../10_data

# Download file if not already downloaded.
if [[ ! -f "adult/Adult.csv" ]]; then
    mkdir -p adult/
    mkdir -p adult/models
    #the download is very slow
    wget -nv -O adult/Adult.csv https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data
    if [[ -f "adult/Adult.csv" ]]; then
      sed -i '$d' adult/Adult.csv; # fix empty line at end of file
      echo "Successfully downloaded Adult dataset."
    else
      echo "Could not download Adult dataset."
      exit 1
    fi
else
    echo "Adult is already downloaded."
fi


echo "Beginning download of Census"

# Download file if not already downloaded.
if [[ ! -f "census/Census.csv" ]]; then
    mkdir -p census/
    mkdir -p census/models
    #the download is very slow
    wget -nv -O census/Census.csv https://kdd.ics.uci.edu/databases/census1990/USCensus1990.data.txt
    if [[ -f "census/Census.csv" ]]; then
      echo "Successfully downloaded census dataset."
    else
      echo "Could not download dataset."
      exit
    fi
else
    echo "Census is already downloaded"
fi

if [[ ! -f "census/census.csv.mtd" ]]; then
    echo "Constructing metadata."
    echo '{"format":csv,"header":true,"rows":2458285,"cols":69,"value_type":"int"}' > census/census.csv.mtd
else
    echo "Already constructed metadata for census.csv"
fi

echo "DONE"
