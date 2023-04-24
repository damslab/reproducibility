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

machines=("XPS-15-7590 dams-so001 tango")

mkdir -p plots/microbenchmark/tab

python plots/microbenchmark/table_v3.py \
      -d $data -t $techniques \
      -m $mm -s $mVSizes \
      -a $algorithms \
      -b $algorithmsData \
      -tt $algorithmsTechniques \
      -u $unaryAggregate \
      -c $scalar \
      -v $compressMeasures \
      -x $machines  &

python plots/microbenchmark/table_v4_comp.py \
      -d $data -t $techniques \
      -m $mm -s $mVSizes \
      -a $algorithms \
      -b $algorithmsData \
      -tt $algorithmsTechniques \
      -u $unaryAggregate \
      -c $scalar \
      -v $compressMeasures \
      -x $machines  &

python plots/microbenchmark/table_v4_ua.py \
      -d $data -t $techniques \
      -m $mm -s $mVSizes \
      -a $algorithms \
      -b $algorithmsData \
      -tt $algorithmsTechniques \
      -u $unaryAggregate \
      -c $scalar \
      -v $compressMeasures  \
      -x $machines  &

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
      -v $compressMeasures  \
      -x $machines  &


wait

mkdir -p plots/microbenchmark/mm
mkdir -p plots/microbenchmark/ua
mkdir -p plots/microbenchmark/sc
mkdir -p plots/microbenchmark/comp
mkdir -p plots/tables


wait


# ## Generate Plots.
python plots/microbenchmark/plot_UnaryAggOps.py -x $machines &
python plots/microbenchmark/plot_ScalarOps.py -x $machines &
python plots/microbenchmark/plot_new_mml.py -x $machines &
python plots/microbenchmark/plot_mm_scale.py -x $machines &
python plots/microbenchmark/plot_tensorflow.py -x $machines &

# ## Generate latex tables.
python plots/microbenchmark/generate_tex_scaleup.py -x $machines &
python plots/microbenchmark/generate_tex_scaleup_SYSML.py -x $machines &
python plots/microbenchmark/generate_tex_scaleup_SYSML_v2.py -x $machines &
python plots/microbenchmark/generate_tex_localExec.py -x $machines &
python plots/microbenchmark/generate_tex_comp_times.py -x $machines &
python plots/microbenchmark/generate_tex_spark_comp.py -x $machines &
python plots/microbenchmark/generate_tex_rmm_overlap.py -x $machines &

python plots/microbenchmark/generate_tex_TOPS.py -x $machines &
python plots/microbenchmark/generate_tex_grid.py -x $machines &



wait



# cp plots/microbenchmark/mm/* ../v2/fig/results/ &
# cp plots/microbenchmark/ua/* ../v2/fig/results/ &
