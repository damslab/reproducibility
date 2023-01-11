#/bin/bash

source parameters.sh

export LOG4JPROP='code/conf/log4j-compression.properties'
export LOG4JPROP_SYSML='code/conf/log4j-off.properties'

data=("census_enc_16k")
algorithms=("l2svmml")
techniques=("ulab16 clab16 claWorkloadb16")

source code/algorithms/algorithms.sh
