#!/bin/bash

wget https://gitlab.com/dlr-dw/is-it-worth-it-benchmark/-/archive/main/is-it-worth-it-benchmark-main.zip
unzip is-it-worth-it-benchmark-main.zip
cp -rn ./is-it-worth-it-benchmark-main/* ./is-it-worth-it-benchmark/
rm -rf ./is-it-worth-it-benchmark-main
rm is-it-worth-it-benchmark-main.zip

conda env create -f requirements/utsadbench_requirements.yml   # Create the conda environment
conda activate btw2025
pip install merlin@git+https://gitlab.com/dlr-dw/py-merlin.git

cd is-it-worth-it-benchmark
pip install -e . --no-deps # All dependencies are already installed in the conda environment


# Make sure to run the script install_merlin_ucr.sh to copy the data to the correct location inside the is-it-worth-it-benchmark-main directory
cp -r ../data/ucraa/ data/ucraa/
cd ..




