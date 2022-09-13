#!/bin/bash

source parameters.sh

if [ ! -d "$SYSTEMDS_ROOT" ]; then
    echo "Systemds not installed."
    echo "Download systemds, and start anew."
    exit
fi

if [ ! -d "$VENV_PATH" ]; then
    echo "Python virtual environment not setup"
    exit
fi 

./data/get_census.sh 
./data/get_covType.sh 
./data/get_infimnist.sh 
./data/get_airlines.sh 

wait 

