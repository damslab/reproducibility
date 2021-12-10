#!/bin/bash

source parameters.sh

source code/util/gitIdLog.sh

logGitIDs

address=(${address[@]} "localhost")

scp -q code/distributedExpNew.sh localhost:$remoteDir/code

for index in ${!address[*]}; do
    scp -q parameters.sh ${address[$index]}:$remoteDir
done
wait

ssh -T localhost "
    cd ${remoteDir};
    ./code/distributedExpNew.sh;
"
