#/bin/bash

if [[ -f "data/siemens/ananymized_data.csv" ]]; then
    if [[ -f "data/siemens/anonymized_data_modified.csv" ]]; then
        echo "Remove col 1 csv already done for siemens data."
    else
        python code/dataPrep/make_csv_siemens.py &
    fi

    if [[ -d "data/siemens/train_siemens.data" ]]; then
        echo "train already made for Covtype."
    else
        systemds code/dataPrep/saveTrainSiemens.dml &
    fi
    wait
else
    echo "Siemens data Missing"
fi
