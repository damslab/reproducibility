#/bin/bash

echo "Beginning download of mnist"

# Change directory to data.
if [[ pwd != *"data"* ]]; then
    cd "data"
fi

# Download file if not already downloaded.
mkdir -p mnist/
cd mnist
if [[ ! -f "train-images-idx3-ubyte.gz" ]]; then
    sleep 0.2
    wget http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz &
else
    echo "Download part of Mnist is already done p1"
fi
if [[ ! -f "train-labels-idx1-ubyte.gz" ]]; then
    sleep 0.2
    wget http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz &
else
    echo "Download part of Mnist is already done p2"
fi
if [[ ! -f "t10k-images-idx3-ubyte.gz" ]]; then
    sleep 0.2
    wget http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz &
else
    echo "Download part of Mnist is already done p3"
fi
if [[ ! -f "t10k-labels-idx1-ubyte.gz" ]]; then
    sleep 0.2
    wget http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz &
else
    echo "Download part of Mnist is already done p4"
fi
cd ..

wait

cd mnist/
if [[ ! -f "train-images-idx3-ubyte" ]]; then
    gunzip "train-images-idx3-ubyte.gz" &
else
    echo "Unzip of part MNIST already done p1"
fi
if [[ ! -f "train-labels-idx1-ubyte" ]]; then
    gunzip "train-labels-idx1-ubyte.gz" &
else
    echo "Unzip of part MNIST already done p2"
fi
if [[ ! -f "t10k-images-idx3-ubyte" ]]; then
    gunzip "t10k-images-idx3-ubyte.gz" &
else
    echo "Unzip of part MNIST already done p3"
fi
if [[ ! -f "t10k-labels-idx1-ubyte" ]]; then
    gunzip "t10k-labels-idx1-ubyte.gz" &
else
    echo "Unzip of part MNIST already done p4"
fi
cd ..
wait

cd ..

# Activate python venv
source parameters.sh


if [[ ! -f "data/mnist/train.csv" ]]; then
    python code/dataPrep/make_csv_mnist.py -d "data/mnist/t10k-images-idx3-ubyte" -o "data/mnist/test.csv" -i "True" &
    python code/dataPrep/make_csv_mnist.py -d "data/mnist/train-images-idx3-ubyte" -o "data/mnist/train.csv" -i "True" &

    python code/dataPrep/make_csv_mnist.py -d "data/mnist/t10k-labels-idx1-ubyte" -o "data/mnist/testL.csv" &
    python code/dataPrep/make_csv_mnist.py -d "data/mnist/train-labels-idx1-ubyte" -o "data/mnist/trainL.csv" &

    wait
else
    echo "Saving of CSV already done for MNIST"
fi

if [[ ! -f "data/mnist/train_mnist.data" ]]; then
    systemds code/dataPrep/saveTrainMnist.dml
else
    echo "Saving of SystemDS binary already done for MNIST"
fi

echo "Mnist Setup Done"


echo ""
echo ""
