#!/bin/bash

source parameters.sh

# Synchronize code and setup.
for index in ${!address[*]}; do

    if [ "${address[$index]}" != "localhost" ]; then
        ssh -T ${address[$index]} '
        cd github/systemds;
        git fetch; 
        git reset --hard origin/CompressionRLE > /dev/null 2>&1;
        git checkout CompressionRLE > /dev/null 2>&1;
        git pull  > /dev/null 2>&1;
        mvn clean package > /dev/null 2>&1;
        printf "$HOSTNAME\tInstalled $(git rev-parse --abbrev-ref HEAD) $(git rev-parse HEAD)\n"
        ' &
        ssh ${address[$index]} " cd ${remoteDir}; rm -rf results; rm -rf hprof" &
    else
        path=$pwd
        cd ~/github/systemds
        git fetch
        git checkout CompressionRLE >/dev/null 2>&1
        git pull >/dev/null 2>&1
        mvn clean package >/dev/null 2>&1 &
        printf "$HOSTNAME\tInstalled $(git rev-parse --abbrev-ref HEAD) $(git rev-parse HEAD)\n"
        cd $path
    fi
done

wait
