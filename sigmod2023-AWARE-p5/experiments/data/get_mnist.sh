#/bin/bash

# Change directory to data.
if [[ pwd != *"data"* ]]; then
    cd "data"
fi

# Download file if not already downloaded.
mkdir -p mnist/
if [[ ! -f "mnist/train-images-idx3-ubyte.gz" ]]; then
    sleep 0.2
    wget http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz &
fi
if [[ ! -f "mnist/train-labels-idx1-ubyte.gz" ]]; then
    sleep 0.2
    wget http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz &
fi
if [[ ! -f "mnist/t10k-images-idx3-ubyte.gz" ]]; then
    sleep 0.2
    wget http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz &
fi
if [[ ! -f "mnist/t10k-labels-idx1-ubyte.gz" ]]; then
    sleep 0.2
    wget http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz &
fi

wait

cd mnist/
if [[ ! -f "mnist/train-images-idx3-ubyte" ]]; then
    gunzip "train-images-idx3-ubyte.gz" &
fi
if [[ ! -f "mnist/train-labels-idx1-ubyte" ]]; then
    gunzip "train-labels-idx1-ubyte.gz" &
fi
if [[ ! -f "mnist/t10k-images-idx3-ubyte" ]]; then
    gunzip "t10k-images-idx3-ubyte.gz" &
fi
if [[ ! -f "mnist/t10k-labels-idx1-ubyte" ]]; then
    gunzip "t10k-labels-idx1-ubyte.gz" &
fi
cd ..
wait

cd ..
if [[ ! -f "data/mnist/train.csv" ]]; then
    python code/dataPrep/make_csv_mnist.py -d "data/mnist/t10k-images-idx3-ubyte" -o "data/mnist/test.csv" -i "True" &
    python code/dataPrep/make_csv_mnist.py -d "data/mnist/train-images-idx3-ubyte" -o "data/mnist/train.csv" -i "True" &

    python code/dataPrep/make_csv_mnist.py -d "data/mnist/t10k-labels-idx1-ubyte" -o "data/mnist/testL.csv" &
    python code/dataPrep/make_csv_mnist.py -d "data/mnist/train-labels-idx1-ubyte" -o "data/mnist/trainL.csv" &

    wait
fi

if [[ ! -f "data/mnist/train_mnist.data" ]]; then
    systemds code/dataPrep/saveTrainMnist.dml
fi

echo "Mnist Setup Done"
