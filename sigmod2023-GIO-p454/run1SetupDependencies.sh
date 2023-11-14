#!/bin/bash

sudo apt update

# Install Java 
sudo apt-get install -y openjdk-11-jdk-headless

# Install C++ dependencies
sudo apt-get install -y cmake # need to compile c++ based baselines
sudo apt-get install -y clang # need for c++ implementations
sudo apt-get install -y rapidjson-dev # RapidJSON baseline

sudo apt install -y maven # need to compile java based baselines
sudo apt install -y git # need to clon repositories
sudo apt-get install -y wget # need to download datasets

sudo apt-get install -y unzip # extract .zip files
sudo apt-get install -y unrar # extract .rar fiels
sudo apt install -y xz-utils # extract tar.xz files

# Install pdflatex for visualization
sudo apt-get install -y texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra
sudo apt-get install -y texlive-science

# Python Environment 
rm -rf envGIO # clean up
sudo apt install -y python3-pip virtualenv
virtualenv -p python3 envGIO #Create an environment: envGIO
source envGIO/bin/activate #Active environment: envGIO
