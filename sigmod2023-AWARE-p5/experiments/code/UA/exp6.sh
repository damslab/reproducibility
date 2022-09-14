#!/bin/bash

source parameters.sh

LOG4JPROP='code/conf/log4j-off.properties'
LOG4JPROP_SYSML='code/conf/log4j-off.properties'

data=("covtypeNew census census_enc airlines infimnist_1m")
unaryAggregate=("sum sum+ colsum colsum+")

# High Repeat  (because it is fast!)
inrep=10000

# Techniques used:
techniques=("clab16 claWorkloadb16")
sysml=0

echo "Running compressed Sum and ColSum"
echo ""

source code/UA/unaryAggregateRun.sh

# Low repeat Baselines (because it is slow)

techniques=("ulab16")
sysmltechniques=("cla-sysml")

inrep=100
sysml=1

echo "Running baseline Sum and ColSum"
echo ""

source code/UA/unaryAggregateRun.sh




