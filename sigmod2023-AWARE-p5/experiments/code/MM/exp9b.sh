#/bin/bash

source parameters.sh


# export LOG4JPROP='code/conf/log4j-off.properties'
export LOG4JPROP='code/conf/log4j-compression.properties'
export LOG4JPROP_SYSML='code/conf/log4j-off.properties'

data=("covtypeNew census census_enc airlines infimnist_1m")

mVSizes=("16")
inrep=50
techniques=("ulab16 clab16 claWorkloadb16")
sysmltechniques=("cla-sysml")

echo "Running compressed MML scaling all"
sysds=1
sysml=1
mm=("euclidean+")
source code/MM/runMM.sh
