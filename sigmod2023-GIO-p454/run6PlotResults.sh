#!/bin/bash

cd explocal/plotting

rm -rf results # clean-up
mkdir -p results # create merge results path

mkdir -p plots
python3 merge_results.py

make clean
make
make clean

rm -rf ../../plots # clean-up
mv exp2_identification_1k_10k_Table3.pdf plots/Table3.pdf
mv plots/ ../../