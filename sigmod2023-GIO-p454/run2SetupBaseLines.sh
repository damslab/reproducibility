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

#---------------

#cleanup
rm -rf "$path/JavaBaselines"
mkdir -p "$path/JavaBaselines"


# clone Apache SystemDS repository
rm -rf systemds #cleanup
git clone https://github.com/fathollahzadeh/systemds.git
# checkout commit hash as of camera-ready version
cd systemds
git checkout -b   GIOV02 d1ed124a04bc2ec42c704382c3a8097b2c3243a9

#build systemds and prepare all dependencies
mvn clean package -P distribution

# clean-up last libs
rm -rf "$path/baselines/JavaBaselines/lib"
mkdir -p "$path/baselines/JavaBaselines/lib"

# move the jars outside to be accessible by the run scripts
mv target/SystemDS.jar "$path/baselines/JavaBaselines/lib/"
mv target/lib/ "$path/baselines/JavaBaselines/lib/"
