#/bin/bash

mkdir -p data/crypto

# Crypto forcasting dataset
if [[ ! -f "data/crypto/train.csv" ]]; then
    cd data/crypto
    kaggle competitions download g-research-crypto-forecasting -f train.csv
    unzip -p train.csv.zip >train.csv
    rm train.csv.zip
    echo '{"data_type": "frame","format": "csv","sep": ",","header": true}' >train.csv.mtd
    cd ../../

fi
