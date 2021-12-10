#!/bin/bash

if [[ -d "tmp/worker" ]]; then
    echo "Stopping workers $HOSTNAME"
    for f in ./tmp/worker/*; do
        pkill -P $(cat $f)
        rm -f $f
    done
    rm -fr tmp/worker
fi
