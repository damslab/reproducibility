#/bin/bash

source parameters.sh


# export LOG4JPROP='code/conf/log4j-off.properties'
export LOG4JPROP='code/conf/log4j-compression.properties'
export LOG4JPROP_SYSML='code/conf/log4j-off.properties'


sysmltechniques=("cla-sysml")

mVSizes=("16")

# Techniques used:

## LMM
mm=("mml")

# echo "Running compressed MML 16."
# inrep=50
# data=("covtypeNew census census_enc airlines")
# techniques=("ulab16 clab16 claWorkloadb16")
# sysds=1
# sysml=0
# source code/MM/runMM.sh

# echo "Running Compressed MML 16 Infinimnist reduced"
# inrep=20
# sysds=1
# sysml=0
# data=("infimnist_1m")
# source code/MM/runMM.sh

# echo "Running  CLA baseline MML 16"
# inrep=20
# sysds=0
# sysml=1
# data=("covtypeNew census census_enc airlines infimnist_1m")
# source code/MM/runMM.sh

## RMM!
mm=("mmr")

# echo "Running Compressed MMR 16 Mem and AWARE only."
# techniques=("clab16 claWorkloadb16")
# sysds=1
# sysml=0
# data=("covtypeNew census census_enc airlines infimnist_1m")
# inrep=10000
# source code/MM/runMM.sh

# echo "Running Baseline MMR 16 Baseline CLA"
# techniques=("ulab16")
# sysml=0
# sysds=1
# inrep=50
# data=("covtypeNew census census_enc airlines infimnist_1m")
# source code/MM/runMM.sh

# echo "Running Baseline MMR 16 Baseline SYSML"
# techniques=("ulab16")
# sysml=1
# sysds=0
# inrep=50
# data=("covtypeNew census census_enc airlines")
# source code/MM/runMM.sh

techniques=("ulab16")
sysml=1
sysds=0
inrep=10
data=("infimnist_1m")
source code/MM/runMM.sh

