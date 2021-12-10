#!/bin/bash

nohup ./exp/expdist/sparkDML.sh SystemDS.jar \
  -f ./exp/expdist/SlicingExp6.dml -explain -exec hybrid -stats \
  -args /data/criteo_X_d21.bin /data/criteo_e_d21.bin >results/Experiment6.out 2>&1