#!/bin/bash

#cleanup
path="$(pwd)/setup"
rm -rf "$path/RapidJSON"
rm -rf "$path/Python"
mkdir -p "$path/RapidJSON"
mkdir -p "$path/Python"


# build and setup RapidJSON baseline
cd baselines/RapidJSONCPP
./makeClean.sh
cp bin/aminer-author-json "$path/RapidJSON/"
cp bin/aminer-paper-json "$path/RapidJSON/"
cp bin/yelp-json "$path/RapidJSON/"
cd ..

#  build and setup Python baseline
cd PythonPandas
pip install -r requirements.txt # install requirements

cp matrixCSVReader.py "$path/Python"
cp matrixLibSVMReader.py "$path/Python"
cp matrixMMReader.py "$path/Python"
cp frameCSVReader.py "$path/Python"
cp frameHL7Reader.py "$path/Python"