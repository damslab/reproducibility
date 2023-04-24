#/bin/bash

source parameters.sh

export SYSDS_DISTRIBUTED=1

export LOG4JPROP='code/conf/log4j-compression.properties'
# export LOG4JPROP='code/conf/log4j-compression-spark.properties'
# export LOG4JPROP='code/conf/log4j-compression-spark.properties'
export LOG4JPROP_SYSML='code/conf/log4j-off.properties'

# data=("census_enc_8x_16k census_enc_16x_16k census_enc_32x_16k census_enc_128x_16k")
# algorithms=("kmeans+ PCA+ mLogReg+ lmCG+ lmDS+ l2svm+")
# algorithms=("PCA+ lmCG+ lmDS+ l2svm+ mLogReg+ kmeans+")
data=("census_enc_16k")
techniques=("ulab16 clab16 claWorkloadb16")
algorithms=("GridMLogReg+")

exrep=3
data=("census_enc_16k")
# data=("census_enc")
# data=("census_enc_16k census_enc_8x_16k census_enc_16x_16k census_enc_32x_16k")
data=("census_enc_16k census_enc_8x_16k")
# data=("census_enc_16x_16k census_enc_32x_16k")
# exrep=3
# exrep=1
# exrep=1




source code/algorithms/algorithms.sh

