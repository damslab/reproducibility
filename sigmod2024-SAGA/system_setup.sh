#!/bin/bash
# This script takes ~10 minutes to finish

sudo apt update
sudo apt install -y openjdk-11-jdk-headless
sudo apt install -y maven 
sudo apt install -y build-essential
sudo apt install -y git
sudo update-alternatives --config java
sudo apt install -y python3-dev python3-pip python3-venv
sudo apt install -y r-base
sudo apt install -y texlive-full #LaTeX compiler (takes a few minutes)
export JAVA_HOME=/usr/lib/jvm/java-1.11.0-openjdk-amd64

