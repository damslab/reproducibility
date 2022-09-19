#/bin/bash

source parameters.sh


# export LOG4JPROP='code/conf/log4j-off.properties'
export LOG4JPROP='code/conf/log4j-compression.properties'
export LOG4JPROP_SYSML='code/conf/log4j-off.properties'

data=("census_enc")

mm=("seqmmr")
mVSizes=("512")
inrep=10
# techniques=("ulab16 claWorkloadb16 claWorkloadb16NoOL")
sysmltechniques=("cla-sysml")
sysds=1
sysml=1

echo "Running compressed MMR Sequence"
source code/MM/runMM.sh
