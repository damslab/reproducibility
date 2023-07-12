#!/bin/bash

mkdir -p tmpdata
cd tmpdata

# HIGGS (CSV)
wget https://archive.ics.uci.edu/ml/machine-learning-databases/00280/HIGGS.csv.gz

# Mnist8m (LibSVM)
wget https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/multiclass/mnist8m.xz

# Susy (LibSVM)
wget https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/SUSY.xz

# Queen (Matrix Market)
wget https://suitesparse-collection-website.herokuapp.com/MM/Janna/Queen_4147.tar.gz



# HIGGS CSV
#https://archive.ics.uci.edu/ml/machine-learning-databases/00280/HIGGS.csv.gz

# LibSVM : https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/
# KDD 12
# https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/kdd12.bz2


#MM
#https://graphchallenge.mit.edu/data-sets
#https://graphchallenge.s3.amazonaws.com/synthetic/graph500-scale25-ef16/graph500-scale25-ef16_adj.mmio.gz

#MM
#https://sparse.tamu.edu/

# 786,431	786,431	2,710,370,560	Undirected Graph
#https://sparse.tamu.edu/Mycielski/mycielskian20



#1. 2186	relat9	JGD_Relat	12,360,060	549,336	38,955,420	Combinatorial Problem	2008
# https://sparse.tamu.edu/JGD_Relat/relat9

#2.	Queen_4147	Janna	4,147,110	4,147,110	316,548,962	2D/3D Problem
#https://sparse.tamu.edu/Janna/Queen_4147
