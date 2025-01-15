#!/bin/bash
set -e
echo "========================================================================"
echo "Setting up SystemDS and checking for Spark Installation"
echo "========================================================================"

cd ./00_setup

./installAptPackages.sh

./pythonSetup.sh

./buildSystemDS.sh

./checkSpark.sh

cd ..
