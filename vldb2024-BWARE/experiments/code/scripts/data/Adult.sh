#/bin/bash

# https://archive.ics.uci.edu/ml/datasets/US+Census+Data+(1990)

mkdir -p data/adult/

if [[ ! -f "data/adult/adult.csv" ]]; then
    wget -O data/adult/adult.csv https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data
    
    # fix empty line at end of file
    sed -i '/^\s*$/d' data/adult/adult.csv
    echo '{"data_type":"frame","format":"csv","sep":",","header":false}' >data/adult/adult.csv.mtd
fi
