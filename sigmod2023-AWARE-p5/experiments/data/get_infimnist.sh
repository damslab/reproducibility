#/bin/bash

# Change base directory to data
if [[ pwd != *"data"* ]]; then
    cd "data"
fi

# Download infimnist
if [[ ! -f "infimnist/infimnist" ]]; then
    mkdir -p infimnist/
    wget -nv -O infimnist/infimnist.tar.gz https://leon.bottou.org/_media/projects/infimnist.tar.gz
    cd infimnist/
    tar zxvf "infimnist.tar.gz" -C ../
    make
    rm -f infimnist.tar.gz
    cd ..
fi

if [[ ! -f "infimnist/mnist2m-patterns-idx3-ubyte" ]]; then

    cd infimnist/
    ./infimnist pat 10000 2009999 >mnist2m-patterns-idx3-ubyte &
    cd ..
fi

if [[ ! -f "infimnist/mnist2m-labels-idx1-ubyte" ]]; then

    cd infimnist/
    ./infimnist lab 10000 2009999 >mnist2m-labels-idx1-ubyte &
    cd ..
fi

if [[ ! -f "infimnist/mnist1m-patterns-idx3-ubyte" ]]; then

    cd infimnist/
    ./infimnist pat 10000 1009999 >mnist1m-patterns-idx3-ubyte &
    cd ..
fi

if [[ ! -f "infimnist/mnist1m-labels-idx1-ubyte" ]]; then

    cd infimnist/
    ./infimnist lab 10000 1009999 >mnist1m-labels-idx1-ubyte &
    cd ..
fi

wait
cd ..

# if [[ ! -f "data/infimnist/train-80m.csv" ]]; then
#     python code/dataPrep/make_csv_mnist.py -d "data/infimnist/mnist80m-patterns-idx3-ubyte" -o "data/infimnist/train-80m.csv" -i 1 &
#     python code/dataPrep/make_csv_mnist.py -d "data/infimnist/mnist80m-labels-idx1-ubyte" -o "data/infimnist/trainL-80m.csv" &
# fi

if [[ ! -f "data/infimnist/train-8m.csv" ]]; then
    python code/dataPrep/make_csv_mnist.py -d "data/infimnist/mnist8m-patterns-idx3-ubyte" -o "data/infimnist/train-8m.csv" -i 1 &
    python code/dataPrep/make_csv_mnist.py -d "data/infimnist/mnist8m-labels-idx1-ubyte" -o "data/infimnist/trainL-8m.csv" &
fi

if [[ ! -f "data/infimnist/train-2m.csv" ]]; then
    python code/dataPrep/make_csv_mnist.py -d "data/infimnist/mnist2m-patterns-idx3-ubyte" -o "data/infimnist/train-2m.csv" -i 1 &
    python code/dataPrep/make_csv_mnist.py -d "data/infimnist/mnist2m-labels-idx1-ubyte" -o "data/infimnist/trainL-2m.csv" &
fi

if [[ ! -f "data/infimnist/train-1m.csv" ]]; then
    python code/dataPrep/make_csv_mnist.py -d "data/infimnist/mnist1m-patterns-idx3-ubyte" -o "data/infimnist/train-1m.csv" -i 1 &
    python code/dataPrep/make_csv_mnist.py -d "data/infimnist/mnist1m-labels-idx1-ubyte" -o "data/infimnist/trainL-1m.csv" &
fi
wait

if [[ ! -f "data/infimnist/train_infimnist_2m.data.mtd" ]]; then
    systemds code/dataPrep/saveTrainInfimnist.dml -args 2000000 "2m" &
fi

if [[ ! -f "data/infimnist/train_infimnist_1m.data.mtd" ]]; then
    systemds code/dataPrep/saveTrainInfimnist.dml -args 1000000 "1m" &
fi

# Create shortcuts for the test dataset, this should be the same as the mnist dataset.
# Therefore im using symbolic links
if [[ ! -f "data/infimnist/test_infimnist.data.mtd" ]]; then
    ln -s "../mnist/test_mnist.data" "data/infimnist/test_infimnist.data"
    ln -s "../mnist/test_mnist.data.mtd" "data/infimnist/test_infimnist.data.mtd"
    ln -s "../mnist/test_mnist_labels.data" "data/infimnist/test_infimnist_labels.data"
    ln -s "../mnist/test_mnist_labels.data.mtd" "data/infimnist/test_infimnist_labels.data.mtd"
fi
wait