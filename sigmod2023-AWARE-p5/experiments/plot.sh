#!/bin/bash

source parameters.sh

date +%T

data=("covtype covtypeNew census mnist airlines infimnist_1m infimnist_2m infimnist_3m infimnist_4m infimnist_5m infimnist_6m infimnist_7m infimnist_8m binarymnist_1m binarymnist_2m binarymnist_3m binarymnist_4m binarymnist_5m binarymnist_6m binarymnist_7m binarymnist_8m")
# data=("covtypeNew")
techniques=("ula cla claOL lcla lclaOL")
techniques=("ula cla claNoOL")
techniques=("ula cla claNoOL claCostMatrix claBIN claCostMatrix005 cla005 claCostMatrix01")
techniques=("ula cla claWorkload")
# techniques=("ula cla sdc claNoOL ddc")

compressMeasures=("cla claTranspose claNoTranspose sdc ddc")
compressMeasures=("cla claCostMatrix claCostMatrix005 claCostMatrix01 claCostMatrix05")
compressMeasures=("cla claWorkload")
compressMeasures=("claMemory-hybrid")

mm=("mmC mml mml+ mmls mmls+ mmlt mmr mmr+ mmrs mmrs+ mmrus seqmmr+ tsmmOL mmrbem mmrbem+")
# mm=("mmr mmrbem")
mVSizes=("1 2 4 8 16 32 64 128 256 512 1024")

scalar=("cellwiseMV div divcellwise divcellwiseinv divinv divOL less less2 lessEq lessEQOL lessEqOLSingle lessEqOLDual mult plus plusOL plusOLSingle squared")

algorithms=("kmeans PCA mLogReg lmCG lmDS l2svm")
algorithmsData=("census_enc_16k census_enc_8x_16k census_enc_32x_16k census_enc_128x_16k")
algorithmsTechniques=("ulab16-hybrid claWorkloadb16-hybrid")

unaryAggregate=("colmax colmean colsum max mean min rowmax rowmaxOL rowsum rowsumOL sqsum sum xminusmean xminusmeanTrick xminusmeanSingle tsmm tsmm+")

machines=("XPS-15-7590 tango alpha")
machines=("XPS-15-7590")
# machines=("alpha")
machines=("tango")

python plots/microbenchmark/table_v3.py \
      -d $data -t $techniques \
      -m $mm -s $mVSizes \
      -a $algorithms \
      -b $algorithmsData \
      -tt $algorithmsTechniques \
      -u $unaryAggregate \
      -c $scalar \
      -v $compressMeasures \
      -x $machines &

python plots/microbenchmark/table_v4_comp.py \
      -d $data -t $techniques \
      -m $mm -s $mVSizes \
      -a $algorithms \
      -b $algorithmsData \
      -tt $algorithmsTechniques \
      -u $unaryAggregate \
      -c $scalar \
      -v $compressMeasures \
      -x $machines &

python plots/microbenchmark/table_v4_ua.py \
      -d $data -t $techniques \
      -m $mm -s $mVSizes \
      -a $algorithms \
      -b $algorithmsData \
      -tt $algorithmsTechniques \
      -u $unaryAggregate \
      -c $scalar \
      -v $compressMeasures  &

python plots/microbenchmark/table_v4_scalar.py \
      -d $data -t $techniques \
      -m $mm -s $mVSizes \
      -a $algorithms \
      -b $algorithmsData \
      -tt $algorithmsTechniques \
      -u $unaryAggregate \
      -c $scalar \
      -v $compressMeasures \
      -x $machines &

python plots/microbenchmark/table_v4_mm.py \
      -d $data -t $techniques \
      -m $mm -s $mVSizes \
      -a $algorithms \
      -b $algorithmsData \
      -tt $algorithmsTechniques \
      -u $unaryAggregate \
      -c $scalar \
      -v $compressMeasures  &


wait

mkdir -p plots/microbenchmark/mm
mkdir -p plots/microbenchmark/ua
mkdir -p plots/microbenchmark/sc
mkdir -p plots/microbenchmark/comp


# python plots/microbenchmark/plot_Algorithms.py &
# python plots/microbenchmark/plot_v1.py &
# python plots/microbenchmark/plot_mml.py &
# python plots/microbenchmark/plot_mmr.py &
# python plots/microbenchmark/plot_tsmm.py &





python plots/microbenchmark/plot_comp_spark.py &
python plots/microbenchmark/plot_tensorflow.py &


python plots/microbenchmark/plot_census_sum.py &
python plots/microbenchmark/plot_mean_div.py &
python plots/microbenchmark/plot_mean_minus.py &
python plots/microbenchmark/plot_UnaryAggOps.py &
python plots/microbenchmark/plot_ScalarOps.py &
python plots/microbenchmark/plot_mm_scale.py &
python plots/microbenchmark/plot_new_mml.py &
python plots/microbenchmark/generate_tex.py &

python plots/microbenchmark/plot_comp_workload_size.py &


wait

# cp plots/microbenchmark/mm/* ../v2/fig/results/ &
# cp plots/microbenchmark/ua/* ../v2/fig/results/ &
