
#/bin/bash

source parameters.sh

export LOG4JPROP='code/conf/log4j-compression.properties'
export LOG4JPROP_SYSML='code/conf/log4j-off.properties'



algorithms=("l2svmml")
sysmltechniques=("cla-sysml ula-sysml")

source code/algorithms/algorithmsSysML.sh
