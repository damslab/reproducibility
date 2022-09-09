#!/bin/bash

source load-had-3.3-spark-3.2-java-11.sh

export SYSTEMDS_ROOT="$HOME/github/systemds"
export PATH="$SYSTEMDS_ROOT/bin:$PATH"

# export LOG4JPROP='code/conf/log4j-off.properties'
# export LOG4JPROP='code/conf/log4j-warn.properties'
# export LOG4JPROP='code/conf/log4j-factory.properties'
export LOG4JPROP='code/conf/log4j-compression.properties'
# export LOG4JPROP='code/conf/log4j-compression-trace-sizeEstimator.properties'
export LOG4JPROP_SYSML='code/conf/log4j-compression-sysml.properties'

export SYSDS_QUIET=1

if [ "$HOSTNAME" = "XPS-15-7590" ]; then
    export SYSTEMDS_STANDALONE_OPTS="-Xmx32g -Xms32g -Xmn3200m"
    # export SYSTEMDS_STANDALONE_OPTS="-Xmx30g -Xms30g -Xmn3000m"
    # export SYSTEMDS_STANDALONE_OPTS="-Xmx24g -Xms24g -Xmn2400m"
    # export SYSTEMDS_STANDALONE_OPTS="-Xmx8g -Xms8g -Xmn800m"
    # export SYSTEMDS_STANDALONE_OPTS="-Xmx16g -Xms16g -Xmn1600m"
elif [ "$HOSTNAME" = "alpha" ]; then
    export SYSTEMDS_STANDALONE_OPTS="-Xmx700g -Xms700g -Xmn70g"
    export SYSTEMDS_DISTRIBUTED_OPTS="\
        --master yarn \
        --deploy-mode client \
        --driver-memory 700g \
        --conf spark.driver.extraJavaOptions=\"-Xms700g -Xmn70g -Dlog4j.configuration=file:$LOG4JPROP\" \
        --conf spark.executor.extraJavaOptions=\"-Dlog4j.configuration=file:$LOG4JPROP\" \
        --conf spark.executor.heartbeatInterval=100s \
        --files $LOG4JPROP \
        --conf spark.network.timeout=512s \
        --num-executors 6 \
        --executor-memory 105g \
        --executor-cores 32 \
        "
else
    export SYSTEMDS_STANDALONE_OPTS="-Xmx110g -Xms110g -Xmn11g"
    export SYSTEMDS_DISTRIBUTED_OPTS="\
        --master yarn \
        --deploy-mode client \
        --driver-memory 110g \
        --conf spark.driver.extraJavaOptions=\"-Xms110g -Xmn11g -Dlog4j.configuration=file:$LOG4JPROP\" \
        --conf spark.executor.extraJavaOptions=\"-Dlog4j.configuration=file:$LOG4JPROP\" \
        --conf spark.executor.heartbeatInterval=100s \
        --files $LOG4JPROP \
        --conf spark.network.timeout=512s \
        --num-executors 6 \
        --executor-memory 105g \
        --executor-cores 32 \
        "
fi

if [ -d ~/intel ] && [ -d ~/intel/bin ] && [ -f ~/intel/bin/compilervars.sh ]; then
    . ~/intel/bin/compilervars.sh intel64
else
    . /opt/intel/bin/compilervars.sh intel64
fi

VENV_PATH="python_venv"

address=(localhost)
# address=(alpha)
address=(tango)
# address=(charlie)

remoteDir="github/papers/2023-sigmod-AWARE/experiments"

# data=("infimnist_2m")
# data=("infimnist_4m infimnist_5m infimnist_6m infimnist_7m")
# data=("infimnist_8m infimnist_8m_16k")
# data=("infimnist_8m_16k")
# data=("infimnist_1m_16k")
# data=("census_enc_16k")

## COMPRESSION only:
data=("covtypeNew census census_enc airlines infimnist_1m amazon")
# data=("covtypeNew census census_enc airlines infimnist_1m")

# data=("amazon")

## ALL DATASETS microbenchmarks
data=("covtypeNew census census_enc airlines infimnist_1m")

# data=("census_enc_16k infimnist_1m_16k airlines covtypeNew mnist")
# data=("census_enc infimnist_1m")
# data=("census_enc airlines infimnist_1m")
# data=("census_enc infimnist_1m")
# data=("infimnist_1m")
# data=("mnist")
# data=("airlines")
# data=("airlines infimnist_1m")
data=("census")
# data=("census_enc")
# data=("covtypeNew")
# data=("amazon")

# data=("infimnist_1m census_enc")

## ALGORITHM RUNS
# data=("census_enc_16k census_enc_8x_16k census_enc_16x_16k census_enc_32x_16k census_enc_128x_16k")
# data=("census_enc_16k census_enc_8x_16k census_enc_16x_16k census_enc_32x_16k")
# data=("census_enc_16k census_enc_32x_16k")
# data=("census_enc_16k census_enc_8x_16k")
# data=("census_enc_32x_16k census_enc_128x_16k")
# data=("census_enc_32x_16k")
# data=("census_enc_128x_16k")
# data=("census_enc_16x_16k census_enc_32x_16k")
# data=("census_enc_2x")
# data=("census_enc_16x_16k")
# data=("census_enc_16k")
# data=("census_enc")
# data=("census_enc_16k census_enc_8x_16k")
# data=("census_enc_8x_16k")
# data=("airlines")
# data=("census_enc census_enc_2x")

seed=333
exrep=1
inrep=1000
# inrep=500
compressionRep=1
# mode="spark"
# mode="hybrid"
mode="singlenode"
sysml=1
# Old paper
# sysmlClassPath="$HOME/github/systemml_compression3/target/SystemML.jar:$HOME/github/systemml_compression3/target/lib/*"
# Old system
sysmlClassPath="$HOME/github/systemml/target/SystemML.jar:$HOME/github/systemml_compression3/target/lib/*"
sysds=1
# sysds=0

# Compression:
# techniques=("clab16 claGreedyb16 claWorkloadb16 claGreedyWorkloadb16 claStatic")
# techniques=("clab16 claGreedyb16 claWorkloadb16 claGreedyWorkloadb16 claStatic")
# techniques=("claSTATICRLE")
# techniques=("ulab16 clab16 claWorkloadb16")
# techniques=("ulab16")
# sysmltechniques=("cla-sysml")
# sysmltechniques=("ula-sysml cla-sysml")
# sysmltechniques=("ula-sysml")

# Others:
techniques=("ulab16")
# techniques=("clab16")
# techniques=("clab16 claWorkloadb16")
# techniques=("clab16 claWorkloadb16")
# techniques=("clab16 claWorkloadb16 claWorkloadb16NoOL")
# techniques=("claWorkloadb16NoOL")
# techniques=("claWorkloadb16")
# techniques=("ulab16 clab16 claWorkloadb16")
# techniques=("ulab16 claWorkloadb16 claGreedyWorkloadb16 clab16 claGreedyb16")
# techniques=("claWorkloadb16 claGreedyWorkloadb16 clab16 claGreedyb16")
# techniques=("ulab16 claWorkloadb16 clab16")
# techniques=("claGreedyb16")
# techniques=("clab16")
# techniques=("clab16 clab16NoSoft")
# techniques=("clab16NoSoft")
# techniques=("ulab16 claWorkloadb16")
# techniques=("claWorkloadb16RLE")
# techniques=("clab16RLE")
# techniques=("claSTATICRLE")
# techniques=("ulab16")
# techniques=("claSTATIC")
# techniques=("claWorkloadb16DDCRLEOnly")
# techniques=("claGreedyWorkloadb16")
# techniques=("claWorkloadb16 claGreedyWorkloadb16")
# techniques=("claStatic")
# techniques=("claStaticWorkload")
# techniques=("clab16 claWorkloadb16")
# sysmltechniques=("ula-sysml cla-sysml")
# sysmltechniques=("ula-sysml")
# sysmltechniques=("cla-sysml")

# Compression Experiments
# techniques=("claLocalSparkb1 claLocalSparkb2 claLocalSparkb8 claLocalSparkb16 claLocalSparkb32 claLocalSparkb64 claLocalSparkb128")
# techniques=("clab1 clab2 clab4 clab8 clab16 clab32 clab64 clab128 clab256 claWorkloadb1 claWorkloadb2 claWorkloadb4 claWorkloadb8 claWorkloadb16 claWorkloadb32 claWorkloadb64 claWorkloadb128 claWorkloadb256")
# techniques=("claLocalSparkb64")

# Scale up Compression Experiments:
# techniques=("claMemory")

# mm=("mml mml+ mmr mmr+")
# mm=("mml mml+")
# mm=("mml mml+ mmr mmr+")
# mm=("mml+")
# mm=("mml+")
# mm=("mml mml+")
# mm=("mmr mmr+")
mm=("mmr")
# mm=("mmr+ euclidean+")
mm=("euclidean+")
# mm=("mmr+")
mm=("seqmmr")

# mm=("mml mml+ mmr mmr+ euclidean euclidean+")
# mm=("mml")
# mm=("mml+ mmls mmls+")
# mm=("mml mml+ mmls mmls+")
# mm=("mmls ")
# mm=("euclidean")
# mm=("euclidean euclidean+")
# mm=("mml mmr+")
# mm=("mmr+ mmrbem+")
# mm=("mmrbem+ mmrbem")
# mm=("mmrbem")


# FOR ALL COMPARE!
mVSizes=("16")
mVSizes=("512")

# For Scaling:
# mVSizes=("1 2 4 8 16 32 64 128 256 512 1024")
# mVSizes=("1 2 4 8 16 32 64 128 256 512")
# mVSizes=("128 256")
# mVSizes=("512 1024")
# mVSizes=("512")
# mVSizes=("1024")
# mVSizes=("3")
# mVSizes=("4")
# mVSizes=("32")
# mVSizes=("128")
# mVSizes=("1 2 4 8 16")
# mVSizes=("1")
# mVSizes=("2")
# mVSizes=("2")
# mVSizes=("8")

# scalar=("mult plus cellwiseMV less lessOL2 lessEqOLSingle")
scalar=("mult")
scalar=("plus")
# scalar=("plusOL")
# scalar=("plusOLSingle")
# scalar=("squared")
# scalar=("isNaN")
# scalar=("plus squared")
# scalar=("cellwiseMV div divcellwise divcellwiseinv divinv divOL less less2 lessEq lessEQOL lessEqOLSingle mult plus squared")

# unaryAggregate=("colmax colmean colsum max mean min rowmax rowmaxOL rowsum sqsum sum xminusmean xminusmeanTrick xminusmeanSingle tsmm tsmm+ sum+")
# unaryAggregate=("colmean rowmax rowsum sum xminusmean xminusmeanSingle xminusmeanTrick")
# unaryAggregate=("sum sum+")
# unaryAggregate=("xminusvector xminusvector+ xdivvector xdivvector+")
unaryAggregate=("colsum colsum+ sum sum+ scaleshift scaleshift+ rowmax rowmax+")
# unaryAggregate=("scaleshift scaleshift+") 
# unaryAggregate=("scaleshift+")
unaryAggregate=("scaleshift") 
unaryAggregate=("sum sum+")
unaryAggregate=("sum")
# unaryAggregate=("colsum colsum+")
# unaryAggregate=("xdivvector xdivvector+")
# unaryAggregate=("xdivvector+")
# unaryAggregate=("rowmax")
# unaryAggregate=("francesco francesco_m")
# unaryAggregate=("francesco_m")
# unaryAggregate=("tsmm tsmm+")
# unaryAggregate=("tsmm+")
# unaryAggregate=("tsmm")
# unaryAggregate=("xdivvector xdivvector+")

# unaryAggregate=("sum colsum")

# algorithms=("PCA kmeans")
# algorithms=("kmeans")
# algorithms=("kmeans mLogReg")
# algorithms=("PCA")
# algorithms=("lmCG")
# algorithms=("lmDS")
# algorithms=("lmCG lmCG")

# algorithms=("l2svm")
algorithms=("mLogReg")
# algorithms=("kmeans PCA mLogReg lmCG lmDS l2svm")
# algorithms=("kmeans kmeans+ PCA PCA+ mLogReg mLogReg+ lmCG lmCG+ lmDS lmDS+ l2svm l2svm+")
algorithms=("l2svm l2svm+")
# algorithms=("kmeans+ PCA PCA+ mLogReg mLogReg+ lmCG lmCG+ lmDS lmDS+ l2svm l2svm+")
algorithms=("kmeans+ PCA+ mLogReg+ lmCG+ lmDS+ l2svm+")
# algorithms=("PCA+")
# algorithms=("kmeans kmeans+")
# algorithms=("kmeans+")

# algorithms=("mLogReg+")

# algorithms=("mLogReg lmCG lmDS l2svm")
# algorithms=("PCA mLogReg lmCG lmDS l2svm")
# algorithms=("kmeans lmCG lmDS l2svm mLogReg")
# algorithms=("lmCG lmDS l2svm")
# algorithms=("kmeans PCA mLogReg")
# algorithms=("lmDS")

# algorithms=("PCA PCA+")
# algorithms=("PCA")
# algorithms=("PCA PCAS")
# algorithms=("PCAS")
# algorithms=("l2svm lmDS")

# algorithms=("printCol")
# algorithms=("l2svm+")
algorithms=("l2svm")
algorithms=("l2svmml")

# algorithms=("GridMLogReg+")
# algorithms=("mLogReg+")

# experiments=("MatrixVector")

clear=1
