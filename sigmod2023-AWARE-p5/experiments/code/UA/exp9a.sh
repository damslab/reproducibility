#!/bin/bash

source parameters.sh

LOG4JPROP='code/conf/log4j-off.properties'
LOG4JPROP_SYSML='code/conf/log4j-off.properties'

data=("covtypeNew census census_enc airlines infimnist_1m")
unaryAggregate=("scaleshift scaleshift+ xdivvector xdivvector+")

# Low Repeat because it is slow.

# Techniques used:
inrep=50
sysmltechniques=("cla-sysml")
techniques=("ulab16")
sysml=1
sysds=1

echo "Running scale and shift baselines"

source code/UA/unaryAggregateRun.sh

inrep=10000
# Techniques used:
# sysmltechniques=("cla-sysml")
techniques=("clab16 claWorkloadb16")
sysml=0
sysds=1

echo "Running scale and shift MEM and AWARE"

source code/UA/unaryAggregateRun.sh
