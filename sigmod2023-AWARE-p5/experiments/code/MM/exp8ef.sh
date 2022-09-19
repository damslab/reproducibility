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

echo "Running compressed MML scaling all"
sysds=1
sysml=1
mm=("mml")
source code/MM/runMM.sh

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

echo "Running Compressed MML 16 Infinimnist reduced"
inrep=20
sysds=1
sysml=0
data=("infimnist_1m")
source code/MM/runMM.sh

echo "Running  CLA baseline MML 16"
inrep=20
sysds=0
sysml=1
data=("covtypeNew census census_enc airlines infimnist_1m")
source code/MM/runMM.sh

## RMM!
mm=("mmr")

echo "Running Compressed MMR 16 Mem and AWARE only."
techniques=("clab16 claWorkloadb16")
sysds=1
sysml=0
data=("covtypeNew census census_enc airlines infimnist_1m")
inrep=10000
source code/MM/runMM.sh

echo "Running Baseline MMR 16 Baseline"
techniques=("ulab16")
sysml=1
sysds=1
inrep=50
source code/MM/runMM.sh
