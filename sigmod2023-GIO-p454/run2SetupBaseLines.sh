#!/bin/bash

#cleanup
root_path="$(pwd)"
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

cd ..

# clone Apache SystemDS repository
rm -rf systemds #cleanup
git clone git@github.com:apache/systemds.git

# checkout commit hash as of camera-ready version
cd systemds
git checkout -b reproducibility 82d9d130861be8e36d37a08c22cdd8d3231de6c2

#build systemds and prepare all dependencies
mvn clean package -P distribution

# clean-up last libs
rm -rf "../JavaBaselines/lib"

# move the jars outside to be accessible by the run scripts
mv target/lib/ "../JavaBaselines/"
mv target/SystemDS.jar "../JavaBaselines/lib/"

cd .. # move to parent path
rm -rf systemds #clean-up

# compile and setup java baselines (GIO, SystemDS, and some other implementations over the SystemDS)
cd "JavaBaselines"
rm -rf target
mvn clean package -P distribution

#cleanup
rm -rf "$path/JavaBaselines"
mkdir -p "$path/JavaBaselines"

mv target/lib/ "$path/JavaBaselines/"
mv target/JavaBaselines.jar "$path/JavaBaselines/"
 