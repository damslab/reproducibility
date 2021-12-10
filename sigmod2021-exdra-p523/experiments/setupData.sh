#!/bin/bash

source parameters.sh

# Syncronize the parameters file with remote
scp -q parameters.sh $main:$remoteDir
scp -q code/generateData.sh $main:$remoteDir/code

# Syncronize the parameters file with a potentially different local location
cp parameters.sh ~/$remoteDir/parameters.sh
cp code/generateData.sh ~/$remoteDir/code/generateData.sh

# Only creat data on local and main machines
address=($main "localhost")

for index in ${!address[*]}; do
    ssh -T  ${address[$index]} "
        cd ${remoteDir};
        ./code/generateData.sh;
    " &
done
wait