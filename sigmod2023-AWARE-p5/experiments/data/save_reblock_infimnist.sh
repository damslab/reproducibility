#!/bin/bash

source parameters.sh 

export SYSDS_DISTRIBUTED=1

# systemds code/dataPrep/save_reblock.dml -config code/conf/ulab16.xml -args "infimnist/train_infimnist_8m"
systemds code/dataPrep/save_reblock.dml -config code/conf/ulab16.xml -args "infimnist/train_infimnist_1m"
