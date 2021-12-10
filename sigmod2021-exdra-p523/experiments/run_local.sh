#!/bin/bash

# Run local ssh to the main machine and execute the local version of the experiment.

source parameters.sh

scp -q parameters.sh $main:$remoteDir
scp -q code/localExp.sh $main:$remoteDir/code/

ssh -T $main "
    cd ${remoteDir};
    ./code/localExp.sh;
"
