#!/bin/bash

# source load-had-3.3-spark-3.2-java-11.sh

# SystemML github Hash to use (On fork: git@github.com:Baunsgaard/systemds.git)
systemMLID="06e40c6165cce5d6ae1e822a16f702d8bcd77ff6"
# SystemDS github Hash to use (On Main: git@github.com:apache/systemds.git)
systemDSID="c34ea60da241ad0d11b37565265b7824e5012d81"

# SSH address of the machine running experiments.
address=(so001)
# Name of laptop if you are using one.
laptop="XPS-15-7590"

# The directory on the remote machine to copy results from... (again if wanted)
# This path should match the location of cloning the reproducability repository.
remoteDir="~/github/reproducibility/sigmod2023-AWARE-p5/experiments"

# SystemDS set on path to enable running SystemDS
export SYSTEMDS_ROOT="$HOME/github/systemds"
export PATH="$SYSTEMDS_ROOT/bin:$PATH"

# SystemML class path. to enable running SystemML
sysmlClassPath="$HOME/github/systemml/target/SystemML.jar:$HOME/github/systemml_compression3/target/lib/*"

# Boolean switches to enable running or disableing running SystemDS or SystemML
sysml=1
sysds=1

# Switch to set if one want to overwrite old results or not.
# 1 means overwrite.
# 0 means do not run if already run.
clear=1

# Logging settings to use:
# SystemDS Logging file:
# export LOG4JPROP='code/conf/log4j-off.properties'
# export LOG4JPROP='code/conf/log4j-warn.properties'
# export LOG4JPROP='code/conf/log4j-factory.properties'
export LOG4JPROP='code/conf/log4j-compression.properties'
# export LOG4JPROP='code/conf/log4j-compression-trace-sizeEstimator.properties'
# SystemML logging file:
export LOG4JPROP_SYSML='code/conf/log4j-compression-sysml.properties'

export SYSDS_QUIET=1

# Machine parameters for memory consumption
# Note the distributed options are needed for running in spark.
if [ "$HOSTNAME" = "$laptop" ]; then
    # export SYSTEMDS_STANDALONE_OPTS="-Xmx32g -Xms32g -Xmn3200m"
    export SYSTEMDS_STANDALONE_OPTS="-Xmx30g -Xms30g -Xmn3000m"
    # export SYSTEMDS_STANDALONE_OPTS="-Xmx24g -Xms24g -Xmn2400m"
    # export SYSTEMDS_STANDALONE_OPTS="-Xmx16g -Xms16g -Xmn1600m"
    # export SYSTEMDS_STANDALONE_OPTS="-Xmx8g -Xms8g -Xmn800m"
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

# Load Intel MKL if available.
if [ -d ~/intel ] && [ -d ~/intel/bin ] && [ -f ~/intel/bin/compilervars.sh ]; then
    . ~/intel/bin/compilervars.sh intel64
elif [ -d /opt/intel ]; then
    . /opt/intel/bin/compilervars.sh intel64
fi

# Python Vertual environment
VENV_PATH="python_venv"
if [ -d $VENV_PATH ]; then
    source "$VENV_PATH/bin/activate"
fi

# General Seed for all the experiments
seed=333

# ExpRep, the number of times to repeat experiments
# Increase this to improve numerical stability of the results... but increase execution time.
exrep=1

# The number of times to repeat inner operations in a given microbenchmark.
# This value is important to change depending on operation testing, since
# Different operations take vastly different time.
# I suggest consulting the paper to find a balance of how fast an operation is
# and the number of times to repeat.
inrep=1000

# General mode to run experiments in.
# If we want to force everything into spark use "spark"
# If we want to force everything into local use "singlenode"
# If we want to use both spark and local instructions use "Hybrid" -- This should be best
# mode="spark"
# mode="hybrid"
mode="singlenode"

## Configuration to use:
# Note techniques should correspond to configuration files in experiments/code/conf
# techniques are configurations for SystemDS
# sysmltechniques are configurations for systemML

# techniques explaination:
# ulab16 = ULA with blocksize of 16k                -> Default baseline
# clab16 = CLA with blocksize of 16k                -> Default AWARE-Mem (sometimes called Mem in paper)
# claWorkloadb16 = AWARE with blocksize of 16k      -> Default AWARE
# claSTATIC = CLA with no cocoding
# claWorkloadb16NoOL= CLA Workload no Overlapping intermediates  -> Aware-No OL

# systmltechniques:
# ula-sysml = SystemML ULA
# cla-sysml = SystemML CLA                          -> Default CLA SystemML
# cla-sysmlb16 = SystemML CLA with blocksize of 16k

# Others:
# techniques=("ulab16")
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

# ETC

# data=("infimnist_2m")
# data=("infimnist_4m infimnist_5m infimnist_6m infimnist_7m")
# data=("infimnist_8m infimnist_8m_16k")
# data=("infimnist_8m_16k")
# data=("infimnist_1m_16k")
# data=("census_enc_16k")

## COMPRESSION only:
# data=("covtypeNew census census_enc airlines infimnist_1m amazon")
# data=("covtypeNew census census_enc airlines infimnist_1m")
# data=("amazon")

## ALL DATASETS microbenchmarks
# data=("covtypeNew census census_enc airlines infimnist_1m")

# data=("census_enc_16k infimnist_1m_16k airlines covtypeNew mnist")
# data=("census_enc infimnist_1m")
# data=("census_enc airlines infimnist_1m")
# data=("census_enc infimnist_1m")
# data=("infimnist_1m")
# data=("mnist")
# data=("airlines")
# data=("airlines infimnist_1m")
# data=("census")
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

# mm=("mml mml+ mmr mmr+")
# mm=("mml mml+")
# mm=("mml mml+ mmr mmr+")
# mm=("mml+")
# mm=("mml+")
# mm=("mml mml+")
# mm=("mmr mmr+")
# mm=("mmr")
# mm=("mmr+ euclidean+")
# mm=("euclidean+")
# mm=("mmr+")
# mm=("seqmmr")

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
# mVSizes=("16")
# mVSizes=("512")

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
# scalar=("mult")
# scalar=("plus")
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
# unaryAggregate=("colsum colsum+ sum sum+ scaleshift scaleshift+ rowmax rowmax+")
# unaryAggregate=("scaleshift scaleshift+")
# unaryAggregate=("scaleshift+")
# unaryAggregate=("scaleshift")
# unaryAggregate=("sum sum+")
# unaryAggregate=("sum")
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
# algorithms=("mLogReg")
# algorithms=("kmeans PCA mLogReg lmCG lmDS l2svm")
# algorithms=("kmeans kmeans+ PCA PCA+ mLogReg mLogReg+ lmCG lmCG+ lmDS lmDS+ l2svm l2svm+")
# algorithms=("l2svm l2svm+")
# algorithms=("kmeans+ PCA PCA+ mLogReg mLogReg+ lmCG lmCG+ lmDS lmDS+ l2svm l2svm+")
# algorithms=("kmeans+ PCA+ mLogReg+ lmCG+ lmDS+ l2svm+")
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
# algorithms=("l2svm")
# algorithms=("l2svmml")

# algorithms=("GridMLogReg+")
# algorithms=("mLogReg+")
