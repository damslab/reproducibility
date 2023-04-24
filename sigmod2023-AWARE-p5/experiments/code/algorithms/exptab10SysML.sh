
#/bin/bash

source parameters.sh

export LOG4JPROP='code/conf/log4j-compression.properties'
export LOG4JPROP_SYSML='code/conf/log4j-off.properties'

exrep=2
# data=("train_census_enc")
# data=("train_census_enc_128x")
# data=("train_census_enc")
# data=("train_census_enc_256x")
algorithms=("l2svmml")
# sysmltechniques=("cla-sysml ula-sysml")
# sysmltechniques=("ula-sysml")
# sysmltechniques=("cla-sysml")
sysmltechniques=("ula-sysmlb16 cla-sysmlb16")
sysmltechniques=("cla-sysmlb16")
sysmltechniques=("ula-sysmlb16")

# data=("train_census_enc")
# source code/algorithms/algorithmsSysML-singleNode.sh

# data=("train_census_enc train_census_enc_128x")
data=("train_census_enc_256x")
source code/algorithms/algorithmsSysML.sh

