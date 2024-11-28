#/bin/bash

source parameters.sh

source "$VENV_PATH/bin/activate"

# Change base directory to data
if [[ $(pwd) != *"data"* ]]; then
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

mkdir -p infimnist/byteData/

if [[ ! -f "infimnist/byteData/mnist-7-8m-patterns-idx3-ubyte" ]]; then

    cd infimnist/
    ./infimnist pat   10000 1009999 >byteData/mnist-0-1m-patterns-idx3-ubyte &
    ./infimnist pat 1010000 2009999 >byteData/mnist-1-2m-patterns-idx3-ubyte &
    ./infimnist pat 2010000 3009999 >byteData/mnist-2-3m-patterns-idx3-ubyte &
    ./infimnist pat 3010000 4009999 >byteData/mnist-3-4m-patterns-idx3-ubyte &
    ./infimnist pat 4010000 5009999 >byteData/mnist-4-5m-patterns-idx3-ubyte &
    ./infimnist pat 5010000 6009999 >byteData/mnist-5-6m-patterns-idx3-ubyte &
    ./infimnist pat 6010000 7009999 >byteData/mnist-6-7m-patterns-idx3-ubyte &
    ./infimnist pat 7010000 8009999 >byteData/mnist-7-8m-patterns-idx3-ubyte &
    cd ..
fi

if [[ ! -f "infimnist/byteData/mnist-7-8m-labels-idx1-ubyte" ]]; then

    cd infimnist/
    ./infimnist lab   10000 1009999 >byteData/mnist-0-1m-labels-idx1-ubyte &
    ./infimnist lab 1010000 2009999 >byteData/mnist-1-2m-labels-idx1-ubyte &
    ./infimnist lab 2010000 3009999 >byteData/mnist-2-3m-labels-idx1-ubyte &
    ./infimnist lab 3010000 4009999 >byteData/mnist-3-4m-labels-idx1-ubyte &
    ./infimnist lab 4010000 5009999 >byteData/mnist-4-5m-labels-idx1-ubyte &
    ./infimnist lab 5010000 6009999 >byteData/mnist-5-6m-labels-idx1-ubyte &
    ./infimnist lab 6010000 7009999 >byteData/mnist-6-7m-labels-idx1-ubyte &
    ./infimnist lab 7010000 8009999 >byteData/mnist-7-8m-labels-idx1-ubyte &
    cd ..
fi

wait

mkdir -p infimnist/csvData/

cd ..
folderIn="data/infimnist/byteData"
folderOut="data/infimnist/csvData"
if [[ ! -f "$folderOut/train-7-8m.csv" ]]; then
    python code/dataPrep/make_csv_mnist.py -d "$folderIn/mnist-0-1m-patterns-idx3-ubyte" -o "$folderOut/train-0-1m.csv" -i 1 &
    python code/dataPrep/make_csv_mnist.py -d "$folderIn/mnist-1-2m-patterns-idx3-ubyte" -o "$folderOut/train-1-2m.csv" -i 1 &
    python code/dataPrep/make_csv_mnist.py -d "$folderIn/mnist-2-3m-patterns-idx3-ubyte" -o "$folderOut/train-2-3m.csv" -i 1 &
    python code/dataPrep/make_csv_mnist.py -d "$folderIn/mnist-3-4m-patterns-idx3-ubyte" -o "$folderOut/train-3-4m.csv" -i 1 &
    python code/dataPrep/make_csv_mnist.py -d "$folderIn/mnist-4-5m-patterns-idx3-ubyte" -o "$folderOut/train-4-5m.csv" -i 1 &
    python code/dataPrep/make_csv_mnist.py -d "$folderIn/mnist-5-6m-patterns-idx3-ubyte" -o "$folderOut/train-5-6m.csv" -i 1 &
    python code/dataPrep/make_csv_mnist.py -d "$folderIn/mnist-6-7m-patterns-idx3-ubyte" -o "$folderOut/train-6-7m.csv" -i 1 &
    python code/dataPrep/make_csv_mnist.py -d "$folderIn/mnist-7-8m-patterns-idx3-ubyte" -o "$folderOut/train-7-8m.csv" -i 1 &

    python code/dataPrep/make_csv_mnist.py -d "$folderIn/mnist-0-1m-labels-idx1-ubyte" -o "$folderOut/trainL-0-1m.csv" &
    python code/dataPrep/make_csv_mnist.py -d "$folderIn/mnist-1-2m-labels-idx1-ubyte" -o "$folderOut/trainL-1-2m.csv" &
    python code/dataPrep/make_csv_mnist.py -d "$folderIn/mnist-2-3m-labels-idx1-ubyte" -o "$folderOut/trainL-2-3m.csv" &
    python code/dataPrep/make_csv_mnist.py -d "$folderIn/mnist-3-4m-labels-idx1-ubyte" -o "$folderOut/trainL-3-4m.csv" &
    python code/dataPrep/make_csv_mnist.py -d "$folderIn/mnist-4-5m-labels-idx1-ubyte" -o "$folderOut/trainL-4-5m.csv" &
    python code/dataPrep/make_csv_mnist.py -d "$folderIn/mnist-5-6m-labels-idx1-ubyte" -o "$folderOut/trainL-5-6m.csv" &
    python code/dataPrep/make_csv_mnist.py -d "$folderIn/mnist-6-7m-labels-idx1-ubyte" -o "$folderOut/trainL-6-7m.csv" &
    python code/dataPrep/make_csv_mnist.py -d "$folderIn/mnist-7-8m-labels-idx1-ubyte" -o "$folderOut/trainL-7-8m.csv" &
fi

wait

if [[ ! -f "data/infimnist/train_infimnist_8m.data.mtd" ]]; then
    systemds code/dataPrep/infinimnist/inf-1m.dml
    systemds code/dataPrep/infinimnist/inf-2m.dml
    systemds code/dataPrep/infinimnist/inf-3m.dml 
    systemds code/dataPrep/infinimnist/inf-4m.dml 
    systemds code/dataPrep/infinimnist/inf-5m.dml 
    systemds code/dataPrep/infinimnist/inf-6m.dml 
    systemds code/dataPrep/infinimnist/inf-7m.dml 
    systemds code/dataPrep/infinimnist/inf-8m.dml 
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