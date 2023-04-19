#!/bin/bash

sudo apt update
sudo apt-get install openjdk-11-jdk-headless
sudo apt install -y maven
sudo apt install -y git

rm -rf envGIO # clean up

apt install python3-pip virtualenv -y
virtualenv -p python3 envGIO #Create an environment: envGIO
source envGIO/bin/activate #Active environment: envGIO
