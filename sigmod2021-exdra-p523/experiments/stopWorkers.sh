#!/bin/bash

source parameters.sh
address=(${address[@]})

for index in ${!address[*]}; do
    ssh -T ${address[$index]} " cd ${remoteDir}; ./code/stopWorker.sh;" &
done

wait
