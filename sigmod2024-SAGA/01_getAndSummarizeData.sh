#!/bin/bash

cd data;
./getData.sh;

cd ..
mv systemds/target/SystemDS.jar ./experiments
rm -rf lib
mv systemds/target/lib/ ./experiments/


cd ../experiments;
./runTable4.sh;
cd ..;