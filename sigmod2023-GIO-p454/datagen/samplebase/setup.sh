#!/bin/bash

sudo apt install python3-pip virtualenv -y
virtualenv -p python3 datagen #Create an environment: envHL7
source datagen/bin/activate #Active environment: envHL7

#pip3 install -r requirements.txt