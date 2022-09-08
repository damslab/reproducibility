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

mkdir -p results/tensorflow

## NORMAL:

# { time python3 code/tensorflow/LinearRegression.py -x $x -y $y -i $it \
#      ; } >results/tensorflow/tlr-$HOSTNAME-1.log 2>&1
# { time python3 code/tensorflow/LinearRegression.py -x $x -y $y -i $it \
#      ; } >results/tensorflow/tlr-$HOSTNAME-2.log 2>&1

# { time python3 code/tensorflow/LinearRegressionGraph.py -x $x -y $y -i $it \
#      ; } >results/tensorflow/tlrG-$HOSTNAME-2.log 2>&1
# { time python3 code/tensorflow/LinearRegressionGraph.py -x $x -y $y -i $it \
#      ; } >results/tensorflow/tlrG-$HOSTNAME-2.log 2>&1

# { time systemds code/tensorflow/LinearRegression.dml -stats -args $x $y $it \
#      -config code/conf/ula.xml; } >results/tensorflow/ds_ula-$HOSTNAME-1.log 2>&1
# { time systemds code/tensorflow/LinearRegression.dml -stats -args $x $y $it \
#      -config code/conf/ula.xml; } >results/tensorflow/ds_ula-$HOSTNAME-2.log 2>&1

# { time systemds code/tensorflow/LinearRegression.dml -stats -seed 1234 -args $x $y $it \
#      -config code/conf/claWorkload.xml; } >results/tensorflow/ds_claWorkload-$HOSTNAME-1.log 2>&1
# { time systemds code/tensorflow/LinearRegression.dml -stats -seed 1234 -args $x $y $it \
#      -config code/conf/claWorkload.xml; } >results/tensorflow/ds_claWorkload-$HOSTNAME-2.log 2>&1

# { time python3 code/tensorflow/LinearRegressionGraph.py -x $x -y $y -i $it \
#      ; } >results/tensorflow/tlrG-$HOSTNAME-1.log 2>&1
# { time python3 code/tensorflow/LinearRegressionGraph.py -x $x -y $y -i $it \
#      ; } >results/tensorflow/tlrG-$HOSTNAME-2.log 2>&1

# { time python3 code/tensorflow/LinearRegressionGraphFP32.py -x $x -y $y -i $it \
#      ; } >results/tensorflow/tlrG-FP32-$HOSTNAME-1.log 2>&1
# { time python3 code/tensorflow/LinearRegressionGraphFP32.py -x $x -y $y -i $it \
#      ; } >results/tensorflow/tlrG-FP32-$HOSTNAME-2.log 2>&1

# { time python3 code/tensorflow/LinearRegressionGraphBF16.py -x $x -y $y -i $it \
#      ; } >results/tensorflow/tlrG-BF16-$HOSTNAME-1.log 2>&1
# { time python3 code/tensorflow/LinearRegressionGraphBF16.py -x $x -y $y -i $it \
#      ; } >results/tensorflow/tlrG-BF16-$HOSTNAME-2.log 2>&1

# { time python3 code/tensorflow/LinearRegressionGraphSparse.py -x $x -y $y -i $it \
#      ; } >results/tensorflow/tlrG-Sparse-$HOSTNAME-1.log 2>&1
# { time python3 code/tensorflow/LinearRegressionGraphSparse.py -x $x -y $y -i $it \
#      ; } >results/tensorflow/tlrG-Sparse-$HOSTNAME-2.log 2>&1

# { time python3 code/tensorflow/LinearRegressionGraphSparseFP32.py -x $x -y $y -i $it \
#      ; } >results/tensorflow/tlrG-SparseFP32-$HOSTNAME-1.log 2>&1
# { time python3 code/tensorflow/LinearRegressionGraphSparseFP32.py -x $x -y $y -i $it \
#      ; } >results/tensorflow/tlrG-SparseFP32-$HOSTNAME-2.log 2>&1

# Single threaded:
# { time systemds code/tensorflow/LinearRegression.dml -stats -seed 1234 -args $x $y $it \
#      -config code/conf/claWorkloadST.xml; } >results/tensorflow/ds_claWorkloadST-$HOSTNAME-1.log 2>&1
# { time systemds code/tensorflow/LinearRegression.dml -stats -seed 1234 -args $x $y $it \
#      -config code/conf/claWorkloadST.xml; } >results/tensorflow/ds_claWorkloadST-$HOSTNAME-2.log 2>&1

# { time systemds code/tensorflow/LinearRegression.dml -stats -args $x $y $it \
#      -config code/conf/ulaST.xml; } >results/tensorflow/ds_ST-$HOSTNAME-1.log 2>&1
# { time systemds code/tensorflow/LinearRegression.dml -stats -args $x $y $it \
#      -config code/conf/ulaST.xml; } >results/tensorflow/ds_ST-$HOSTNAME-2.log 2>&1

{ time systemds code/tensorflow/LinearRegression.dml -stats -seed 1234 -args $x $y $it \
     -config code/conf/claWorkloadSTR.xml; } >results/tensorflow/ds_claWorkloadSTR-$HOSTNAME-1.log 2>&1
{ time systemds code/tensorflow/LinearRegression.dml -stats -seed 1234 -args $x $y $it \
     -config code/conf/claWorkloadSTR.xml; } >results/tensorflow/ds_claWorkloadSTR-$HOSTNAME-2.log 2>&1

{ time systemds code/tensorflow/LinearRegression.dml -stats -args $x $y $it \
     -config code/conf/ulaSTR.xml; } >results/tensorflow/ds_STR-$HOSTNAME-1.log 2>&1
{ time systemds code/tensorflow/LinearRegression.dml -stats -args $x $y $it \
     -config code/conf/ulaSTR.xml; } >results/tensorflow/ds_STR-$HOSTNAME-2.log 2>&1

# systemds code/tensorflow/compareModels.dml
