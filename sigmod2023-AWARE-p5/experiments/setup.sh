#!/bin/bash

source parameters.sh

if [ ! -d "$SYSTEMDS_ROOT" ]; then
    echo "Systemds not installed."
    echo "Download systemds, and start anew."
    exit
fi

if [[ ! -d "$VENV_PATH" ]]; then
    echo "Creating Python Virtual Enviroment"
    python3 -m venv $VENV_PATH
    source "$VENV_PATH/bin/activate"
    pip install pip --upgrade > /dev/null
    pip -q install -r requirements.txt
    echo "$HOSTNAME"
    
fi


# if [[ ! -f "data/mnist/train_mnist.data" ]]; then
#     ./data/get_mnist.sh
# fi

# if [[ ! -f "data/binarymnist/train_binarymnist.data" ]]; then
#     systemds code/dataPrep/saveTrainSmallBinaryMnist.dml

#     ln -s "../mnist/train_mnist_labels.data" "data/binarymnist/train_binarymnist_labels.data"
#     ln -s "../mnist/train_mnist_labels.data.mtd" "data/binarymnist/train_binarymnist_labels.data.mtd"
# fi


# if [[ ! -f "data/covtype/train_covtype.data" ]] \
#     || [[ ! -f "data/covtypeNew/train_covtypeNew.data" ]]; then
#     ./data/get_covType.sh &
# fi

# if [[ ! -d "data/airlines/train_airlines.data" ]]; then
#     ./data/get_airlines.sh &
# fi

# if [[ ! -f "data/infimnist/train_infimnist_1m.data.mtd" ]]; then
#     ./data/get_infimnist.sh &
# fi

# if [[ ! -f "data/binarymnist/train_binarymnist_1m.data.mtd" ]]; then
#     ./data/get_binarymnist.sh &
# fi

# if [[ ! -f "data/census/train_census.data.mtd" ]]; then 
#     ./data/get_census.sh &
# fi 

# ./data/setup_siemens.sh &
wait 

# rm -fr target
mkdir -p hprof
mkdir -p results

deactivate
