#!/bin/bash

source parameters.sh

mkdir -p results
mkdir -p hprof

source code/util/gitIdLog.sh
logGitIDs

date +%T

# Compression experiment (Table 5)
# ./code/compression/comp.sh

# Compression experiment Distributed (Table 6)
# ./code/compression/comp-spark.sh

# Figure 6 Sum and ColSum.
./code/UA/exp6.sh


# ./code/UA/unaryAggregateRun.sh
# ./code/scalar/scalar.sh

# if [ "$HOSTNAME" = "XPS-15-7590" ]; then
    # ./code/MM/runMM.sh
    # ./code/compression/comp.sh
    # ./code/UA/unaryAggregateRun.sh
    # ./code/scalar/scalar.sh
    # ./code/tensorflow/tensorflow.sh
    # ./code/algorithms/algorithmsLocal.sh
#    ./code/algorithms/algorithmsSysML.sh
# else
    # ./code/compression/comp.sh
    # ./code/MM/runMM.sh
    # ./code/UA/unaryAggregateRun.sh
    # ./code/scalar/scalar.sh
    # ./code/algorithms/algorithms.sh
    # ./code/algorithms/algorithmsSysML.sh
    # ./code/tensorflow/tensorflow.sh
    # ./code/algorithms/algorithmsLocal.sh
# fi

# >> results/out-$HOSTNAME-"`date +"%d-%m-%Y"`".log 2>&1
# ./code/algorithqms/algorithmsSparkLocalFiles.sh >> results/out-$HOSTNAME-"`date +"%d-%m-%Y"`".log 2>&1

# Signal IT IS DONE!
printf 'DONE! \a'
sleep 0.2
printf '\a'
sleep 0.1
printf '\a'
sleep 0.2
printf '\a'
sleep 0.4
printf '\a'
sleep 0.4
printf '\a\n'
