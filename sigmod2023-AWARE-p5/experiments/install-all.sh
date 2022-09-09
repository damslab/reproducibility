#!/bin/bash

./install-pythonvenv.sh &
./install-SystemDS.sh &
./install-SystemML.sh &

wait 

echo "Installed all"