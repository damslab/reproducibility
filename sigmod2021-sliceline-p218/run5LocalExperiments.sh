#!/bin/bash

# This script runs all local experiments on the specified scale-up machine.

# All scripts are ran with 600GB JVM heap size but would also work with smaller 
# JVMs (selectively tested with 110GB on one of the scale-out nodes).

export CMD="java -Xmx600g -Xms600g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "

./exp/explocal/runExperiment1.sh
./exp/explocal/runExperiment2.sh
./exp/explocal/runExperiment3a.sh
./exp/explocal/runExperiment4a.sh
./exp/explocal/runExperiment4b.sh
./exp/explocal/runExperiment4c.sh
./exp/explocal/runExperiment5a.sh
