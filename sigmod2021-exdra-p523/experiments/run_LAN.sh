#!/bin/bash

source parameters.sh

address=(${address[@]} $main)

scp -q code/distributedExpNew.sh $main:$remoteDir/code

for index in ${!address[*]}; do
    scp -q parameters.sh ${address[$index]}:$remoteDir
done
wait


ssh -T $main "
    cd ${remoteDir};
    ./code/distributedExpNew.sh;
"
