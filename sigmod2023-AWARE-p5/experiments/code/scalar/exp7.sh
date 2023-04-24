#/bin/bash

source parameters.sh


# export LOG4JPROP='code/conf/log4j-off.properties'
export LOG4JPROP='code/conf/log4j-compression.properties'
export LOG4JPROP_SYSML='code/conf/log4j-off.properties'

data=("covtypeNew census census_enc airlines infimnist_1m")
# data=("census_enc")
scalar=("plus plus+ divcellwise")

# High Repeat  (because it is fast!)
inrep=10000

# Techniques used:
techniques=("clab16 claWorkloadb16")
sysds=1
sysml=0

echo "Running compressed Plus and Div vector."

source code/scalar/scalar.sh

techniques=("ulab16")

# Lower rep... just to not waste time.
inrep=100


echo "Running baseline Sum and ColSum"
echo ""

source code/scalar/scalar.sh


sysmltechniques=("cla-sysml")
sysml=1
sysds=0

# even lower rep to reduce time usage again.
inrep=30

source code/scalar/scalar.sh

sysds=1