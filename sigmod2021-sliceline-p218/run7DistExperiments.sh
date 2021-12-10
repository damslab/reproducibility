#!/bin/bash

# This script runs all hybrid and distributed experiments on the specified 
# scale-out cluster in a distributed Spark cluster of 1+12 nodes, 128GB mem.
# The experiments are invoked from the main node running the Hadoop daemons.

./exp/expdist/runExperiment5b.sh;
./exp/expdist/runExperiment6.sh;
