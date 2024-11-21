#!/bin/bash

# Set variables to be used in the other scripts.
# Change these settings to specify what experiments to run, and machines to use.

# Remote addresses These should be ssh accessible by name.
# Test by opening an terminal and writing 'ssh <name>' like 'ssh delta'
address=("delta india mike papa romeo sierra uniform")

# Main is the machine that is used for controller in LAN experiments and the baseline results.
## For the experiments this means ssh to main, and execute the experiments for LAN and baseline
## it is assumed main have faster and shorter internet connection to the other workers than
## the local machine
main="tango"
## Local machine name (hopefully the laptop you sit with should work nicely)
local_machine_name="XPS-15-7590"

# IF YOU DONT HAVE A LIST OF REMOTE MACHINES: (This will not be performant and probably run out of memory)
# address=("localhost localhost localhost")
# main="localhost"

## The ports to use on each machine.
ports=("8001 8002 8003 8004 8005 8006 8007 8008")

## If your local machine does not have access to the ports start the port forward script and set this variable to 1.
portForward=1

# Set memory budget for the machines rule of thumb is 10% is in Xmn:
if [ "$HOSTNAME" = "$local_machine_name" ]; then
    # Local machine for WAN experiments use less memory (this is a laptop)
    export SYSTEMDS_STANDALONE_OPTS="-Xmx30g -Xms30g -Xmn3000m"
else
    # Distributed machines for LAN experiments 
    export SYSTEMDS_STANDALONE_OPTS="-Xmx110g -Xms110g -Xmn11000m"
fi

export LOG4JPROP='code/conf/log4j-off.properties'
# export LOG4JPROP='code/conf/log4j-trace.properties'
# export LOG4JPROP='code/conf/log4j-info.properties'
# export LOG4JPROP='code/conf/log4j-debug.properties'

remoteDir="reproducibility/sigmod2021-exdra-p523/experiments"

# Systemds github hash used in paper submission for final experiments
# This commit works in all experiments except PCA (mkl config)
# This commit also does not create the data correctly, so start with the newer commit
# is in our python api but that is not used for the actual performance
# experiments.
# The paper was submitted with PCA using "def" config
systemdsHash="13dd8cb68260cec6692b2006271f651150519e42" # (Mar 28 2021) 

# SystemDS a bit after with fixed python but still buggy MKL PCA:
# systemdsHash="5c63f3056a741360de77478e9c5d52246bb26786" #  (Apr 12 2021)

# Fixes to nnz handling in mkl for tsmm to enable PCA mkl
# The major differences in results here is
#  - in l2svm that become slower because of communication overhead of more federated operations support
#  - And the PCA becoming faster because of more federated operations leading to less data transfer
# to reproduce paper use the Mar 28 commit.
systemdsHash="3227fdb70c6afcbfdca28a7a323ae6927048b37e" # (Jul 15 2021)

# Decide a location to install systemds
export SYSTEMDS_ROOT="$HOME/reproducibility/systemds"
export PATH="$SYSTEMDS_ROOT/bin:$PATH"
export SYSDS_QUIET=1

# Set java version to 8.
export JAVA_HOME="/usr/lib/jvm/java-1.8.0-openjdk-amd64"
export PATH=$JAVA_HOME/bin:$PATH

# If installed use intel MKL for multiplication:
if [ -d ~/intel ] && [ -d ~/intel/bin ] && [ -f ~/intel/bin/compilervars.sh ]; then
    . ~/intel/bin/compilervars.sh intel64
else
    . /opt/intel/bin/compilervars.sh intel64
fi

VENV_PATH="python_venv"

# Unsupervised Algorithms to run:
Algs=("kmeans pca")

# Supervised Algorithms to run:
SAlgs=("lm l2svm logreg")

# datasets names:
## For Figure 5, 6, 7 use P2P
UnsupervisedD="P2P"
SupervisedD="P2P"

## Note that only one network can be executed in one run so only enable one of them.
## To enable use all three lines:
# networks=("FNN")
# epochs=(5)
# batch_size=(512)

## CNN automattically use MNIST dataset instead.
## To enable use all three lines:
# networks=("CNN")
# epochs=(2)
# batch_size=(128)

# For Figure 8: 
## use and only run LM and P2_FFN:
## comment out the following 5 lines to do this remember to outcomment unsupervised algorithms above $Algs.
# SAlgs=("lm")
# SupervisedD="P2"
# networks=("P2_FFN")
# epochs=(5)
# batch_size=(512)

# Configuration to run with:
## We used a different configurations for the different experiments.
## Most of the results in the paper is using 'mkl' and a few with 'sslmkl'
## Def is our default systemds without accelerator liberaies.
# confs=("def")
confs=("mkl")
# confs=("sslmkl")

# Number of repetitions of experiments Most experiments in the paper was run with 5 reps,
# To make the reproduction faster it is set down to 1, but if the results are odd, then set it up.
rep=1

# Clear variable specifying if new results should append, remove, or skip already done experiments.
# 0 : Skip if already done
# 1 : Remove previous experiment results
# 2 : Append to previous results
clear=1
