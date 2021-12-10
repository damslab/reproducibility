#!/bin/bash

# This script performs basic feature transformations and trains models to
# obtain the recoded input data and error vector, which are inputs to SliceLine.
# The results are writte as *_X (data) and *_e (error) to ./data/*

# All scripts are ran with 600GB JVM heap size but would also work with smaller 
# JVMs (tested with 110GB on one of the scale-out nodes).

CMD="java -Xmx600g -Xms600g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "
CONF=" -config exp/dataprep/SystemDS-config.xml" #just for faster training (~7x)

$CMD -f exp/dataprep/dataprepAdult.dml -exec singlenode -stats 
$CMD -f exp/dataprep/dataprepCovtype.dml -exec singlenode -stats $CONF
$CMD -f exp/dataprep/dataprepKDD98.dml -explain -exec singlenode -stats
$CMD -f exp/dataprep/dataprepUSCensus.dml -exec singlenode -stats $CONF
$CMD -f exp/dataprep/dataprepSalaries.dml -exec singlenode -stats 

$CMD -f exp/dataprep/dataprepUSCensusSize.dml -exec singlenode -stats 
