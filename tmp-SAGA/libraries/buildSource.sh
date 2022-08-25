#!/bin/bash

# This script takes ~4 minutes to finish

# Clone Apache SystemDS repository
rm -rf systemds #cleanup
git clone https://github.com/apache/systemds.git

# Build the source
mvn clean package -P distribution

# Move the jars outside to be accessible by the run scripts
cd ..
mv systemds/target/SystemDS.jar .
rm -rf lib
mv systemds/target/lib/ .

# Cleanup the class files to save space
cd systemds
mvn clean
cd ..
