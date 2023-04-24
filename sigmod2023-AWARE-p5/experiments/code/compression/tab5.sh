#!/bin/bash

source parameters.sh

# Techniques used:
techniques=("clab16 claWorkloadb16")
sysmltechniques=("cla-sysml")

# Compression repetitions - for the compression experiments only.
compressionRep=1
exrep=5

echo "Compress table 5 experiment"

# Data used
data=("covtypeNew census census_enc airlines infimnist_1m")
data=("census_enc")
# data=("covtypeNew")

sysml=1
sysds=0

# source code/compression/comp.sh

sysml=0
sysds=1

# source code/compression/comp.sh


# Note be carefull about this experiments since it takes 37 hours in cla-sysml.
# data=("amazon")
data=("amazon")
sysml=0
sysds=1
source code/compression/comp.sh
