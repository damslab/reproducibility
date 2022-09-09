#!/bin/bash

source parameters.sh

# CD over to the other path
path=$pwd

if [[ ! -d "$HOME/github/systemds" ]]; then
    echo "downloading SystemDS"
    cd "$HOME/github"
    git clone https://github.com/apache/systemds.git
fi


cd ~/github/systemds
git fetch
git checkout $systemDSID >/dev/null 2>&1
git pull >/dev/null 2>&1
mvn clean package >/dev/null 2>&1 &

wait

printf "$HOSTNAME\tInstalled SystemDS $(git rev-parse --abbrev-ref HEAD) $(git rev-parse HEAD)\n"


# CD back
cd $path
