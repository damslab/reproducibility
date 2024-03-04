#!/bin/bash

source parameters.sh

for remote in $remotes; do
    ssh -T $remote "
    mkdir -p github;
    mkdir -p github/systemds;
    mkdir -p $remoteDir;
    mkdir -p $remoteDir/results;
"

    rsync -avhq -e ssh code/* $remote:$remoteDir/code &
    sleep 0.1
    rsync -avhq -e ssh *.sh $remote:$remoteDir &
    sleep 0.1
    rsync -avhq -e ssh requirements.txt $remote:$remoteDir &

    rsync -avhq -e ssh ~/.kaggle $remote:~/ &
done

wait
