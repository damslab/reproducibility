#!/bin/bash

mkdir -p tmpdata
cd tmpdata

# clean-up
rm -rf HIGGS.csv.gz
rm -rf mnist8m.xz
rm -rf SUSY.xz
rm -rf Queen_4147.tar.gz
rm -rf AMiner-Paper.rar
rm -rf AMiner-Author.zip

rm -rf HIGGS.csv
rm -rf mnist8m
rm -rf SUSY
rm -rf Queen_4147
rm -rf AMiner-Paper.txt
rm -rf AMiner-Author.txt

# HIGGS (CSV)
wget https://archive.ics.uci.edu/ml/machine-learning-databases/00280/HIGGS.csv.gz

# Mnist8m (LibSVM)
wget https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/multiclass/mnist8m.xz

# Susy (LibSVM)
wget https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/SUSY.xz

# Queen (Matrix Market)
wget https://suitesparse-collection-website.herokuapp.com/MM/Janna/Queen_4147.tar.gz

# AMiner
wget https://lfs.aminer.cn/lab-datasets/aminerdataset/AMiner-Paper.rar
wget https://lfs.aminer.cn/lab-datasets/aminerdataset/AMiner-Author.zip

# Yelp (JSON):
# download YELP dataset from this link: https://www.yelp.com/dataset/download


# Extract datasets and rename
gzip -d HIGGS.csv.gz
unxz mnist8m.xz
unxz SUSY.xz
tar -xvzf Queen_4147.tar.gz
unrar e AMiner-Paper.rar
unzip AMiner-Author.zip

mv HIGGS.csv ../data/higgs-csv.dat
mv mnist8m ../data/mnist8m-libsvm.dat
mv SUSY ../data/susy-libsvm.dat
mv Queen_4147/Queen_4147.mtx ../data/queen-mm.dat
rm -rf Queen_4147
mv AMiner-Paper.txt ../data/aminer-paper.dat
mv AMiner-Author.txt ../data/aminer-author.dat
