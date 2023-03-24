#!/bin/bash

source parameters.sh


for index in ${!address[*]}; do

        ssh ${address[$index]} " mkdir -p $remoteDir;" &
done 

wait

# Synchronize code and setup.
for index in ${!address[*]}; do
    if [ "${address[$index]}" != "localhost" ]; then
        sleep 0.1
        rsync -avhq -e ssh code/* ${address[$index]}:$remoteDir/code &
        sleep 0.1
        rsync -avhq -e ssh *.sh ${address[$index]}:$remoteDir &
        sleep 0.1
        rsync -avhq -e ssh requirements.txt ${address[$index]}:$remoteDir &
        sleep 0.1
        rsync -avhq -e ssh data/*.sh ${address[$index]}:$remoteDir/data &
        sleep 0.1
        ssh ${address[$index]} " cd ${remoteDir}; mkdir -p results; mkdir -p hprof; source code/util/gitIdLog.sh; logGitIDs;" &
    fi
done
wait

# Get results
for index in ${!address[*]}; do
    if [ "${address[$index]}" != "localhost" ]; then
        sleep 0.1
        rsync -avhq -e ssh ${address[$index]}:$remoteDir/results . &
        rsync -avhq -e ssh ${address[$index]}:$remoteDir/hprof . &
    fi
done
wait
