
#/bin/bash

source parameters.sh

export SYSDS_DISTRIBUTED=1
export LOG4JPROP='code/conf/log4j-compression.properties'
export LOG4JPROP_SYSML='code/conf/log4j-off.properties'

exrep=5
data=("census_enc_16k")
algorithms=("kmeans+ PCA+ mLogReg+ lmCG+ lmDS+ l2svm+")
techniques=("ulab16 clab16 claWorkloadb16")

techniques=("clab16")


source code/algorithms/algorithms.sh
