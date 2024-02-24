#!/bin/bash

# Clone Apache SystemDS repository
rm -rf systemds #cleanup
git clone https://github.com/apache/systemds.git

# Create branch from the commit that includes all paper codes
cd systemds
git checkout -b reproducibility 42b3caae0ad5a0563427358794559be1fc420ef7

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

