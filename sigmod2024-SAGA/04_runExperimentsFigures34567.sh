#!/bin/bash

cd experiments;
python ./prepFoodDataJenga.py;
python ./generateCorruptionsJenga.py;
./runSynJenga.sh;
cd ..;

