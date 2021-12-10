#!/bin/bash

# clone Apache SystemDS repository
rm -rf systemds #cleanup
git clone https://github.com/apache/systemds.git

# checkout commit hash as of camera-ready version
cd systemds
git checkout -b reproducibility 627825c25d5a5938a772a78ce037c57e68611998

# build systemds and prepare all dependencies
mvn clean package -P distribution

# move the jars outside to be accessible by the run scripts
cd ..
mv systemds/target/SystemDS.jar .
rm -rf lib
mv systemds/target/lib/ .
