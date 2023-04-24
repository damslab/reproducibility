#/bin/bash

source parameters.sh

export SYSDS_DISTRIBUTED=1

export LOG4JPROP='code/conf/log4j-compression.properties'
# export LOG4JPROP='code/conf/log4j-compression-spark.properties'
# export LOG4JPROP='code/conf/log4j-compression-spark.properties'
export LOG4JPROP_SYSML='code/conf/log4j-off.properties'

data=("census_enc_8x_16k census_enc_16x_16k census_enc_32x_16k census_enc_128x_16k")
algorithms=("kmeans+ PCA+ mLogReg+ lmCG+ lmDS+ l2svm+")
techniques=("ulab16 claWorkloadb16")
algorithms=("PCA+ lmCG+ lmDS+ l2svm+ mLogReg+ kmeans+")

exrep=4
data=("census_enc_16k")
# data=("census_enc")
# data=("census_enc_16k census_enc_8x_16k census_enc_16x_16k census_enc_32x_16k")
data=("census_enc_16k census_enc_8x_16k")
# data=("census_enc_16x_16k census_enc_32x_16k")
# exrep=3
# exrep=1
# exrep=1
data=("census_enc_32x_16k")
# data=("census_enc_16x_16k")
data=("census_enc_128x_16k")
data=("census_enc_8x_16k")
# data=("census_enc_16k")

# algorithms=("lmCG+ lmDS+ l2svm+ mLogReg+ kmeans+")
algorithms=("l2svm+ mLogReg+ kmeans+")
algorithms=("lmCG+ lmDS+ l2svm+ mLogReg+ kmeans+")
# algorithms=("lmCG+ lmDS+ l2svm+")
# algorithms=("PCA+")
# algorithms=("mLogReg+")
# algorithms=("lmDS+")
# algorithms=("lmCG+")
# algorithms=("l2svm+")
# algorithms=("kmeans+")
# techniques=("claWorkloadb16")
techniques=("ulab16")


## smaller block size.
# data=("census_enc_128x")
# techniques=("ula")



source code/algorithms/algorithms.sh

