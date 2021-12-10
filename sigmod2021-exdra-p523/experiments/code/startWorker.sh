#!/bin/bash

source parameters.sh

export LOG4JPROP='code/conf/log4j-worker.properties'

mkdir -p tmp/worker
mkdir -p results/fed/workerlog/

nohup \
    systemds WORKER $1 -stats 50 -config code/conf/$2.xml \
    > results/fed/workerlog/$HOSTNAME-$1.out 2>&1 &

echo Starting worker $HOSTNAME $1 $2

# Save process Id in file, to stop at a later time
echo $! > tmp/worker/$HOSTNAME-$1
