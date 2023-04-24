#/bin/bash

source parameters.sh


# export LOG4JPROP='code/conf/log4j-off.properties'
export LOG4JPROP='code/conf/log4j-compression.properties'
export LOG4JPROP_SYSML='code/conf/log4j-off.properties'


mVSizes=("1 2 4 8 16 32 64 128 256 512")
data=("census_enc")
inrep=50
techniques=("ulab16 clab16 claWorkloadb16")
sysmltechniques=("cla-sysml")

## MML Scaling

echo "Running compressed MML scaling all"
sysds=1
sysml=1
mm=("mml")
source code/MM/runMM.sh

## MMR scaling:

echo "Running MMR baselines scaling ULA and CLA"
techniques=("ulab16")
sysds=1
sysml=1
mm=("mmr")
source code/MM/runMM.sh

echo "Running MMR MEM and AWARE"
inrep=10000
techniques=("clab16 claWorkloadb16")
sysds=1
sysml=0
mm=("mmr")
source code/MM/runMM.sh

