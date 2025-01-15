#!/bin/bash

if [ -e "./SystemDS.jar" ]; then
  echo "SystemDS already installed. Delete SystemDS.jar to reinstall."
else
  ./run0_SetupSystem.sh
fi

./run1_PrepareDataAndModels.sh

./run2_1ExperimentsDistributed.sh

./run3_1GeneratePlotsDistributed.sh
