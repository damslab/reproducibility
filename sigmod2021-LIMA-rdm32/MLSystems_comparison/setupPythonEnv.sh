#!/bin/bash

python3 -m venv --system-site-packages ./tf-venv
source tf-venv/bin/activate
pip install --upgrade pip
pip install tensorflow==2.3.1
pip install scikit-learn==0.23.2
pip install pandas
deactivate
