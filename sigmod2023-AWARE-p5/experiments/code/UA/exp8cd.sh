#!/bin/bash

source parameters.sh

LOG4JPROP='code/conf/log4j-off.properties'
LOG4JPROP_SYSML='code/conf/log4j-off.properties'

data=("covtypeNew census census_enc airlines infimnist_1m")
unaryAggregate=("tsmm tsmm+")

# Low Repeat because it is slow.
inrep=5

# Techniques used:
sysmltechniques=("cla-sysml")
techniques=("ulab16 clab16 claWorkloadb16")
sysml=1
sysds=1

echo "Running TSMM sparse and dense"

source code/UA/unaryAggregateRun.sh
