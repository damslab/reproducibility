#!/bin/bash

# clone Apache SystemDS repository
rm -rf systemds #cleanup
git clone https://github.com/apache/systemds.git

# checkout commit hash as of camera-ready version (as of Jan 03)
cd systemds
git checkout -b reproducibility a41027f7aa256ee2ea8609f819cded19896bc9f4

# build systemds and prepare all dependencies
mvn clean package -P distribution

# move the jars outside to be accessible by the run scripts
cd ..
mv systemds/target/SystemDS.jar .
rm -rf lib
mv systemds/target/lib/ .
