#!/usr/bin/env bash

export BASE_DIR=$PWD
export WORK_DIR=$BASE_DIR/workdir
export RESULT_DIR=$BASE_DIR/results
export SANDBOX=$BASE_DIR/experiment-sandbox.sif

export MB_REPETITIONS=3

export P1_REPETITIONS=3
export P1_ROOT=$BASE_DIR/experiments/p1
export P1_DATA_DIR=$WORK_DIR/p1-data
export P1_RESULTS=$RESULT_DIR/p1

export P2_ROOT=$BASE_DIR/experiments/p2
export P2_DATA_DIR=$WORK_DIR/p2-data
export P2_BATCHSIZE=2048
export P2_RESULTS=$RESULT_DIR/p2
export P2_REPETITIONS=3
export P2_DATASET=sen2
#export P2_MODEL_H5=sen2_resnet20_model.015.h5
export P2_MODEL_H5=trained-model.h5
export P2_MODEL_CSV=trained-model_hdf2csv/
export P2_TESTING_DATA_CSV="testing_sen2_NCHW_nomean.csv"
export P2_TESTING_LABELS_CSV="testing_label.csv"

export MB_ROOT=$BASE_DIR/experiments/microbenchmarks
export MB_DATA_DIR=$WORK_DIR/mb-data
export MB_RESULTS=$RESULT_DIR/microbenchmarks

export DAPHNE_ROOT=$WORK_DIR/daphne
export SYSTEMDS_ROOT=$WORK_DIR/systemds

export CUDA10_VERSION=10.2
export CUDA10_PACKAGE=cuda_10.2.89_440.33.01_linux.run
export CUDA10_PATH=$WORK_DIR/cuda-$CUDA10_VERSION

export CUDA11_VERSION=11.4.1
export CUDA11_PACKAGE=cuda_11.4.1_470.57.02_linux.run
export CUDA11_PATH=$WORK_DIR/cuda-$CUDA11_VERSION

export CUDNN7_PACKAGE=cudnn-10.2-linux-x64-v7.6.5.32.tgz
export CUDNN7_URL="https://developer.nvidia.com/compute/machine-learning/cudnn/secure/7.6.5.32/Production/10.2_20191118/cudnn-10.2-linux-x64-v7.6.5.32.tgz"
export CUDNN8_PACKAGE=cudnn-11.4-linux-x64-v8.2.2.26.tgz
export CUDNN8_URL="https://developer.nvidia.com/compute/machine-learning/cudnn/secure/8.2.2/11.4_07062021/cudnn-11.4-linux-x64-v8.2.2.26.tgz"

export MKL_PACKAGE=l_mkl_2019.5.281.tgz

