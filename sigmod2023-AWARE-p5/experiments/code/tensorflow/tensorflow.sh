#!/bin/bash

source parameters.sh
source "$VENV_PATH/bin/activate"

# x="data/census/train_census_enc_16k.csv"
# y="data/census/train_census_enc_16k_labels.csv"

x="data/census/train_census_enc.csv"
y="data/census/train_census_enc_labels.csv"
# export OMP_NUM_THREADS=32

# x="data/mnist/train.csv"
# y="data/mnist/trainL.csv"

it=4

it=300
exrep=5

mkdir -p results/tensorflow
mkdir -p results/tensorflow/$HOSTNAME

## NORMAL:

for i in $(seq $exrep); do
     # { time python3 code/tensorflow/LinearRegression.py -x $x -y $y -i $it \
     #      ; } >results/tensorflow/$HOSTNAME/tlr-$i.log 2>&1
     # { time python3 code/tensorflow/LinearRegressionGraph.py -x $x -y $y -i $it \
     #      ; } >results/tensorflow/$HOSTNAME/tlrG-$i.log 2>&1
     { time python3 code/tensorflow/LinearRegressionGraph.py -x $x -y $y -i $it \
          ; } >results/tensorflow/$HOSTNAME/tlrG-$i.log 2>&1
     { time python3 code/tensorflow/LinearRegressionGraphFP32.py -x $x -y $y -i $it \
          ; } >results/tensorflow/$HOSTNAME/tlrG-FP32-$i.log 2>&1
     { time python3 code/tensorflow/LinearRegressionGraphBF16.py -x $x -y $y -i $it \
          ; } >results/tensorflow/$HOSTNAME/tlrG-BF16-$i.log 2>&1
     { time python3 code/tensorflow/LinearRegressionGraphSparse.py -x $x -y $y -i $it \
          ; } >results/tensorflow/$HOSTNAME/tlrG-Sparse-$i.log 2>&1

     { time python3 code/tensorflow/LinearRegressionGraphSparseFP32.py -x $x -y $y -i $it \
          ; } >results/tensorflow/$HOSTNAME/tlrG-SparseFP32-$i.log 2>&1
     # Single threaded read:
     { time systemds code/tensorflow/LinearRegression.dml -stats -seed 1234 -args $x $y $it \
          -config code/conf/claWorkloadSTR.xml; } >results/tensorflow/$HOSTNAME/ds_claWorkloadSTR-$i.log 2>&1

     { time systemds code/tensorflow/LinearRegression.dml -stats -args $x $y $it \
          -config code/conf/ulaSTR.xml; } >results/tensorflow/$HOSTNAME/ds_STR-$i.log 2>&1

     # Parallel:

     { time systemds code/tensorflow/LinearRegression.dml -stats -args $x $y $it \
          -config code/conf/ula.xml; } >results/tensorflow/$HOSTNAME/ds_ula-$i.log 2>&1

     { time systemds code/tensorflow/LinearRegression.dml -stats -seed 1234 -args $x $y $it \
          -config code/conf/claWorkload.xml; } >results/tensorflow/$HOSTNAME/ds_claWorkload-$i.log 2>&1

done

# systemds code/tensorflow/compareModels.dml

# Single threaded:
# { time systemds code/tensorflow/LinearRegression.dml -stats -seed 1234 -args $x $y $it \
#      -config code/conf/claWorkloadST.xml; } >results/tensorflow/$HOSTNAME/ds_claWorkloadST-1.log 2>&1

# { time systemds code/tensorflow/LinearRegression.dml -stats -args $x $y $it \
#      -config code/conf/ulaST.xml; } >results/tensorflow/$HOSTNAME/ds_ST-1.log 2>&1
