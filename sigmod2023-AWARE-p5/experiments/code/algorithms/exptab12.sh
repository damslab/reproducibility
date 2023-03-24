#/bin/bash

source parameters.sh

export LOG4JPROP='code/conf/log4j-compression.properties'
export LOG4JPROP_SYSML='code/conf/log4j-off.properties'

data=("census_enc_8x_16k census_enc_16x_16k census_enc_32x_16k census_enc_128x_16k")
algorithms=("kmeans+ PCA+ mLogReg+ lmCG+ lmDS+ l2svm+")
techniques=("ulab16 claWorkloadb16")


data=(" census_enc_128x_16k")
# data=(" census_enc_8x_16k")
# algorithms=("PCA+")
# algorithms=("l2svm+")
techniques=("claWorkloadb16")
# techniques=("ulab16")


source code/algorithms/algorithms.sh

