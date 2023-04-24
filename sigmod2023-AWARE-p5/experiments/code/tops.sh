#!/bin/bash

source parameters.sh

# Important LOG4J is in compression mode
export LOG4JPROP='code/conf/log4j-compression.properties'

export SYSDS_DISTRIBUTED=0

data=("census_enc")

# Copy to not owerwrite the old results.
techniques=("ulab16Copy claWorkloadb16Copy")

exrep=3

inrep=100
sysds=1
sysml=0

unaryAggregate=("sum")


# fill cache with the input data...
source code/UA/unaryAggregateRun.sh

# UA
unaryAggregate=("sum sum+ tsmm scaleshift")
source code/UA/unaryAggregateRun.sh

# MM
mm=("mmr mml euclidean")
# mm=("mmr mml")
mVSizes=("256")
source code/MM/runMM.sh


# Scalar
scalar=("plus")
source code/scalar/scalar.sh

