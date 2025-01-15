#!/bin/bash
set -e
#based on https://github.com/damslab/reproducibility/blob/master/vldb2022-UPLIFT-p2528/libraries/buildSource.sh by @phaniarnab

echo "Clone Apache SystemDS repository"
rm -rf systemds #cleanup
git clone https://github.com/apache/systemds.git

echo "Create branch from the commit that was used"
cd systemds || exit
git checkout -b reproducibility-shap bd17eadc2c2cbb8077857e4a10b78db4ca485941 

echo "Build the source"
mvn clean package -P distribution

echo "Move the jars outside to be accessible by the run scripts"
cd ..
mv systemds/target/SystemDS.jar ..
rm -rf lib
mv systemds/target/lib/ ..

echo "Cleanup the class files to save space"
cd systemds || exit
mvn clean
cd ..


