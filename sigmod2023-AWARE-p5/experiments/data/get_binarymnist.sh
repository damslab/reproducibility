#/bin/bash

source parameters.sh

source "$VENV_PATH/bin/activate"

# Change base directory to data
if [[ $(pwd) != *"data"* ]]; then
    cd "data"
fi

mkdir -p binarymnist/

cd ..

if [[ ! -f "data/binarymnist/test_binarymnist.data.mtd" ]]; then
    systemds code/dataPrep/saveTestBinarymnist.dml &
fi

if [[ ! -f "data/binarymnist/train_binarymnist_8m.data.mtd" ]]; then
    systemds code/dataPrep/saveTrainBinarymnist.dml -args "8m" &
fi

if [[ ! -f "data/binarymnist/train_binarymnist_7m.data.mtd" ]]; then
    systemds code/dataPrep/saveTrainBinarymnist.dml -args "7m" &
fi

if [[ ! -f "data/binarymnist/train_binarymnist_6m.data.mtd" ]]; then
    systemds code/dataPrep/saveTrainBinarymnist.dml -args "6m" &
fi

if [[ ! -f "data/binarymnist/train_binarymnist_5m.data.mtd" ]]; then
    systemds code/dataPrep/saveTrainBinarymnist.dml -args "5m" &
fi

if [[ ! -f "data/binarymnist/train_binarymnist_4m.data.mtd" ]]; then
    systemds code/dataPrep/saveTrainBinarymnist.dml -args "4m" &
fi

if [[ ! -f "data/binarymnist/train_binarymnist_3m.data.mtd" ]]; then
    systemds code/dataPrep/saveTrainBinarymnist.dml -args "3m" &
fi

if [[ ! -f "data/binarymnist/train_binarymnist_2m.data.mtd" ]]; then
    systemds code/dataPrep/saveTrainBinarymnist.dml -args "2m" &
fi

if [[ ! -f "data/binarymnist/train_binarymnist_1m.data.mtd" ]]; then
    systemds code/dataPrep/saveTrainBinarymnist.dml -args "1m" &
fi

# Create shortcuts for the test dataset, this should be the same as the mnist dataset.
# Therefore im using symbolic links
if [[ ! -f "data/binarymnist/train_binarymnist_1m_labels.data.mtd" ]]; then

    ln -s "../infimnist/train_infimnist_8m_labels.data" "data/binarymnist/train_binarymnist_8m_labels.data"
    ln -s "../infimnist/train_infimnist_8m_labels.data.mtd" "data/binarymnist/train_binarymnist_8m_labels.data.mtd"
    ln -s "../infimnist/train_infimnist_7m_labels.data" "data/binarymnist/train_binarymnist_7m_labels.data"
    ln -s "../infimnist/train_infimnist_7m_labels.data.mtd" "data/binarymnist/train_binarymnist_7m_labels.data.mtd"
    ln -s "../infimnist/train_infimnist_6m_labels.data" "data/binarymnist/train_binarymnist_6m_labels.data"
    ln -s "../infimnist/train_infimnist_6m_labels.data.mtd" "data/binarymnist/train_binarymnist_6m_labels.data.mtd"
    ln -s "../infimnist/train_infimnist_5m_labels.data" "data/binarymnist/train_binarymnist_5m_labels.data"
    ln -s "../infimnist/train_infimnist_5m_labels.data.mtd" "data/binarymnist/train_binarymnist_5m_labels.data.mtd"
    ln -s "../infimnist/train_infimnist_4m_labels.data" "data/binarymnist/train_binarymnist_4m_labels.data"
    ln -s "../infimnist/train_infimnist_4m_labels.data.mtd" "data/binarymnist/train_binarymnist_4m_labels.data.mtd"
    ln -s "../infimnist/train_infimnist_3m_labels.data" "data/binarymnist/train_binarymnist_3m_labels.data"
    ln -s "../infimnist/train_infimnist_3m_labels.data.mtd" "data/binarymnist/train_binarymnist_3m_labels.data.mtd"
    ln -s "../infimnist/train_infimnist_2m_labels.data" "data/binarymnist/train_binarymnist_2m_labels.data"
    ln -s "../infimnist/train_infimnist_2m_labels.data.mtd" "data/binarymnist/train_binarymnist_2m_labels.data.mtd"
    ln -s "../infimnist/train_infimnist_1m_labels.data" "data/binarymnist/train_binarymnist_1m_labels.data"
    ln -s "../infimnist/train_infimnist_1m_labels.data.mtd" "data/binarymnist/train_binarymnist_1m_labels.data.mtd"

    ln -s "../mnist/test_mnist.data" "data/binarymnist/test_binarymnist.data"
    ln -s "../mnist/test_mnist.data.mtd" "data/binarymnist/test_binarymnist.data.mtd"
    ln -s "../mnist/test_mnist_labels.data" "data/binarymnist/test_binarymnist_labels.data"
    ln -s "../mnist/test_mnist_labels.data.mtd" "data/binarymnist/test_binarymnist_labels.data.mtd"
fi

wait
