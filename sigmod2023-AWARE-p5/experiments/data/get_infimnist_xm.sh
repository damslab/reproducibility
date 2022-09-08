#/bin/bash

source parameters.sh

# export SYSDS_DISTRIBUTED=1

systemds code/dataPrep/infinimnist/inf-xm.dml -config code/conf/noCache.xml -stats -debug -exec hybrid -args "2" "test"
systemds code/dataPrep/infinimnist/inf-xm.dml -stats -debug -exec hybrid -args "2" "test"
# systemds code/dataPrep/infinimnist/inf-xm.dml -config code/conf/noCache.xml -stats -debug -exec hybrid -args "8" "16"
# systemds code/dataPrep/infinimnist/inf-xm.dml -config code/conf/noCache.xml -stats -debug -exec hybrid -args "16" "32"
# systemds code/dataPrep/infinimnist/inf-xm.dml -config code/conf/noCache.xml -stats -debug -exec hybrid -args "32" "64"
# systemds code/dataPrep/infinimnist/inf-xm.dml -config code/conf/noCache.xml -stats -debug -exec hybrid -args "64" "128"

wait
