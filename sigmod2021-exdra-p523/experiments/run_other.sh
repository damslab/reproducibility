#!/bin/bash

source parameters.sh

scp -q parameters.sh $main:$remoteDir
scp -q code/other.sh $main:$remoteDir/code/

ssh -T $main "
    cd ${remoteDir};
    ./code/other.sh;
"
