#!/bin/bash

sudo apt install python3-pip virtualenv -y
virtualenv -p python3 envHL7 #Create an environment: envHL7
source envHL7/bin/activate #Active environment: envHL7

pip3 install -r requirements.txt