#!/bin/bash

sudo apt update
sudo apt-get install -y openjdk-11-jdk-headless
sudo apt install -y maven
sudo apt install -y git
sudo apt-get install unzip
sudo apt-get install unrar
sudo apt install xz-utils

rm -rf envGIO # clean up

apt install python3-pip virtualenv -y
virtualenv -p python3 envGIO #Create an environment: envGIO
source envGIO/bin/activate #Active environment: envGIO
