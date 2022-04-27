#!/usr/bin/env bash

BASE_URL="https://dataserv.ub.tum.de/s/m1483140/download?path=%2F&files="
TESTING_H5="testing.h5"
P2_TESTING_LABELS_CSV="testing_label.csv"
TRAINING_FILE="training.h5"
VALIDATION_FILE="validation.h5"

source resources/env.sh
if [ ! -f $SANDBOX ]; then
  echo "Error: Singularity image" $SANDBOX "does not exist. Please run 1_setup_env.sh to build it (root or fakeroot privileges required)"
  exit
fi

mkdir -p $P2_DATA_DIR

if [ ! -f $P2_DATA_DIR/$TESTING_H5 ]; then
  echo "Downloading so2sat v2 testing dataset (3.3GB)"
  wget --no-check-certificate $BASE_URL$TESTING_H5 -O $P2_DATA_DIR/$TESTING_H5
fi

if [ ! -f $P2_DATA_DIR/$TRAINING_FILE ]; then
  echo "Downloading so2sat v2 training dataset (48.4GB)"
  wget --no-check-certificate $BASE_URL$TRAINING_FILE -O $P2_DATA_DIR/$TRAINING_FILE
fi

if [ ! -f $P2_DATA_DIR/$VALIDATION_FILE ]; then
  echo "Downloading so2sat v2 validation dataset (3.3GB)"
  wget --no-check-certificate $BASE_URL$VALIDATION_FILE -O $P2_DATA_DIR/$VALIDATION_FILE
fi

if [ ! -e $P2_DATA_DIR/$P2_MODEL_H5 ]; then
  singularity run --nv --bind "$CUDA11_PATH":/usr/local/cuda $SANDBOX \
    "cd $P2_DATA_DIR; python3 $P2_ROOT/resnet20-training.py dataset=$P2_DATASET datadir=$P2_DATA_DIR \
      2>&1 | tee $WORK_DIR/logs/p2-train-model-$(date --iso-8601)-log.txt"

  TRAINED_MODEL=$P2_DATA_DIR/saved_models/$(ls -rt $P2_DATA_DIR/saved_models | tail -n 1)
    retVal=$?
    if [ $retVal -ne 0 ]; then
      echo "Error, building the experiment sandbox (singularity container) seems to have failed with exit status" $retVal
      exit
    fi
  if [ -z $TRAINED_MODEL ]; then
    echo "No trained odel file found"
    exit
  fi
  ln -sf $TRAINED_MODEL $P2_DATA_DIR/$P2_MODEL_H5
  cd $BASE_DIR
fi

if [ ! -e $P2_DATA_DIR/$P2_MODEL_H5 ]; then
  echo "Error: No trained model file $P2_MODEL_H5 found in $P2_DATA_DIR. Quitting."
  exit
fi

if [ ! -f $P2_DATA_DIR/$P2_TESTING_DATA_CSV ]; then
  echo "Exporting $TESTING_H5 to $P2_TESTING_DATA_CSV"
  singularity run $SANDBOX \
    "python3 $P2_ROOT/convertH5imagesToCSV.py $P2_DATA_DIR/$TESTING_H5 $P2_DATASET NCHW nomean 2>&1 | tee $WORK_DIR/logs/p2-convert-images-h5tocsv-$(date --iso-8601)-log.txt"
fi

if [ ! -f $P2_DATA_DIR/$P2_TESTING_LABELS_CSV ]; then
  echo "Exporting $P2_TESTING_LABELS_CSV"
  singularity run $SANDBOX \
    "python3 $P2_ROOT/convertH5imagesToCSV.py $P2_DATA_DIR/$TESTING_H5 label 2>&1 | tee $WORK_DIR/logs/p2-convert-images-h5tocsv-$(date --iso-8601)-log.txt"
fi

if [ ! -e $P2_DATA_DIR/$P2_MODEL_CSV ]; then
  echo "Exporting $P2_MODEL_H5"
  singularity run $SANDBOX \
    "python3 $P2_ROOT/tf-model-export.py $P2_DATA_DIR/$P2_MODEL_H5 2>&1 | tee $WORK_DIR/logs/p2-model-export-$(date --iso-8601)-log.txt"
fi