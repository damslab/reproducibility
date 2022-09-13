#!/bin/bash

source parameters.sh

export data=("covtypeNew census census_enc airlines infimnist_1m")
export unaryAggregate=("sum sum+ colsum colsum+")

# High Repeat  (because it is fast!)
export inrep=10000

# Techniques used:
export techniques=("clab16 claWorkloadb16")
export sysml=0

echo "Running compressed Sum and ColSum"
echo ""

source code/UA/unaryAggregateRun.sh

# Low repeat Baselines (because it is slow)

export techniques=("ulab16")
export sysmltechniques=("cla-sysml")

export inrep=100
export sysml=1


echo "Running baseline Sum and ColSum"
echo ""

source code/UA/unaryAggregateRun.sh




