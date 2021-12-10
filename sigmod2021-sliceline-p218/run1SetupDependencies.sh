#!/bin/bash

sudo apt update
sudo apt install -y openjdk-8-jdk-headless
sudo apt install -y maven
sudo apt install -y git
sudo apt install -y r-base

export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64

sudo Rscript exp/setup/installDependencies.R