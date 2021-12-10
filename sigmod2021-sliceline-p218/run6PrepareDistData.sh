#!/bin/bash

# This script performs basic feature transformations and trains models for 
# the Criteo dataset in a distributed Spark cluster of 1+12 nodes, 128GB mem.
# The experiments are invoked from the main node running the Hadoop daemons.

# upload loca USCensus 1x dataset to HDFS
hadoop fs -rmr /data/USCensus_X1.bin
hadoop fs -rmr /data/USCensus_X1.bin.mtd
hadoop fs -rmr /data/USCensus_o_e1.bin
hadoop fs -rmr /data/USCensus_o_e1.bin.mtd
hadoop fs -put data/USCensus_X1.bin /data/USCensus_X1.bin
hadoop fs -put data/USCensus_X1.bin.mtd /data/USCensus_X1.bin.mtd
hadoop fs -put data/USCensus_o_e1.bin /data/USCensus_o_e1.bin
hadoop fs -put data/USCensus_o_e1.bin.mtd /data/USCensus_o_e1.bin.mtd

# run Criteo data preparation
hadoop fs -put data/Criteo_D21.csv /data/Criteo_D21.csv

./exp/expdist/sparkDML.sh SystemDS.jar \
  -f ./exp/dataprep/dataprepCriteo.dml -explain -exec hybrid -stats
