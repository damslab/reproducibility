#/bin/bash

source parameters.sh


# export LOG4JPROP='code/conf/log4j-off.properties'
export LOG4JPROP='code/conf/log4j-compression.properties'
export LOG4JPROP_SYSML='code/conf/log4j-off.properties'

data=("census_enc")

exrep=5

mm=("seqmmr")
mVSizes=("512")
inrep=10
techniques=("ulab16 claWorkloadb16 claWorkloadb16NoOL")
techniques=("clab16")
# sysmltechniques=("cla-sysml")

sysds=1
sysml=0

echo "Running compressed MMR Sequence"
source code/MM/runMM.sh

sysds=0
sysml=1


echo "Running compressed MMR Sequence SystemML"

sysmltechniques=("ula-sysmlb16 cla-sysmlb16")
# source code/MM/runMM.sh