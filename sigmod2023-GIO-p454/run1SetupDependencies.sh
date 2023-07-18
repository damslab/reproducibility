#!/bin/bash

sudo apt update
sudo apt-get install -y openjdk-11-jdk-headless
sudo apt install -y maven
sudo apt install -y git
sudo apt-get install -y unzip
sudo apt-get install -y unrar
sudo apt install -y xz-utils

rm -rf envGIO # clean up

apt install -y python3-pip virtualenv
virtualenv -p python3 envGIO #Create an environment: envGIO
source envGIO/bin/activate #Active environment: envGIO
