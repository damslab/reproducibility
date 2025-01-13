#!/bin/bash

# This script performs basic feature transformations and trains models to
# obtain the recoded input data and error vector, which are inputs to SliceLine.
# The results are writte as *_X (data) and *_e (error) to ./data/*

CMD="java -Xmx200g -Xms200g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "
CONF=" -config code/SystemDS-config.xml" #just for faster training (~7x)

# run end to end experiments
$CMD -f code/runSliceLineAllData.dml -exec singlenode -stats -args 0
$CMD -f code/runSliceLineAllData.dml -exec singlenode -stats -args 1
$CMD -f code/runSliceLineAllDataPruning.dml -exec singlenode -stats

# run micro benchmarks
$CMD -f code/runSliceLineMicro.dml -exec singlenode -stats -args 0
$CMD -f code/runSliceLineMicro.dml -exec singlenode -stats -args 1
$CMD -f code/runSliceLineMicro2.dml -exec singlenode -stats -args 1
$CMD -f code/runSliceLineMicro3.dml -exec singlenode -stats -args 1
$CMD -f code/runSliceLineMicro3.dml -exec singlenode -stats -args 0

# postprocessing for runSliceLineMicro2
for i in {0..59}
do
	$CMD -f code/runReadWrite.dml -exec singlenode -stats -args results/Exp2b_1_debug.csv/${i}_null
done

