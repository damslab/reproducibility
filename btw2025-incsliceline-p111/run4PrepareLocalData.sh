#!/bin/bash

# This script performs basic feature transformations and trains models to
# obtain the recoded input data and error vector, which are inputs to SliceLine.
# The results are writte as *_X (data) and *_e (error) to ./data/*

CMD="java -Xmx200g -Xms200g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "
CONF=" -config code/SystemDS-config.xml" #just for faster training (~7x)

$CMD -f code/dataprepAdult.dml -exec singlenode -stats
$CMD -f code/dataprepCovtype.dml -exec singlenode -stats $CONF
$CMD -f code/dataprepKDD98.dml -explain -exec singlenode -stats
$CMD -f code/dataprepUSCensus.dml -explain -exec singlenode -stats $CONF
$CMD -f code/dataprepCreateReplicas.dml -explain -exec singlenode -stats
