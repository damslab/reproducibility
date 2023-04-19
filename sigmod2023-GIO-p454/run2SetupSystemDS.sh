#!/bin/bash

#cleanup
path="$(pwd)/setup"
rm -rf "$path/SystemDS"
mkdir -p "$path/SystemDS"


# clone Apache SystemDS repository
rm -rf systemds #cleanup
git clone https://github.com/fathollahzadeh/systemds.git
# checkout commit hash as of camera-ready version
cd systemds
git checkout -b   sf-GIORevision cc694bc0d18b261dec289781d0c1e078e4975dcc

#build systemds and prepare all dependencies
mvn clean package -P distribution


# move the jars outside to be accessible by the run scripts
mv target/SystemDS.jar "$path/SystemDS/"
mv target/lib/ "$path/SystemDS/"
