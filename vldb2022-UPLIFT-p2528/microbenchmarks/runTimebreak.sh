#!/bin/bash

rm res*breakdown*.dat

echo "Starting Time breakdwon of phases test"
echo "---------------------------------------"
# time calculated in milliseconds

./config stagedtransform start
python3 dataGenString_100c.py 5000000 10000 5
sed -i "s+hadoop.root.logger=INFO,console+hadoop.root.logger=DEBUG,console+" ../libraries/log4j-silent.properties
./config partransform start
# To factor JIT compilation, record the last 3 results (skipping first 2)
./runjava -f micro_timebreak_cat.dml -args 1 -stats &> outTimeBreak.log #RC
grep "Elapsed time for build phase" outTimeBreak.log | awk '{print $10}' | tail -3 >> res_RC_breakdown.dat
grep "Elapsed time for allocation" outTimeBreak.log | awk '{print $9}' | tail -3 >> res_RC_breakdown.dat
grep "Elapsed time for apply phase" outTimeBreak.log | awk '{print $10}' | tail -3 >> res_RC_breakdown.dat
grep "Time spent getting metadata" outTimeBreak.log | awk '{print $9}' | tail -3 >> res_RC_breakdown.dat
./runjava -f micro_timebreak_cat.dml -args 2 -stats &> outTimeBreak.log #DC
grep "Elapsed time for build phase" outTimeBreak.log | awk '{print $10}' | tail -3 >> res_DC_breakdown.dat
grep "Elapsed time for allocation" outTimeBreak.log | awk '{print $9}' | tail -3 >> res_DC_breakdown.dat
grep "Elapsed time for apply phase" outTimeBreak.log | awk '{print $10}' | tail -3 >> res_DC_breakdown.dat
grep "Time spent getting metadata" outTimeBreak.log | awk '{print $9}' | tail -3 >> res_DC_breakdown.dat

python3 dataGenString_50c.py 5000000 10000 5
python3 dataGenFloat_50c.py 5000000 5000000
./runjava -f micro_timebreak_num.dml -stats &> outTimeBreak.log #BIN
grep "Elapsed time for build phase" outTimeBreak.log | awk '{print $10}' | tail -3 >> res_BIN-RC_breakdown.dat
grep "Elapsed time for allocation" outTimeBreak.log | awk '{print $9}' | tail -3 >> res_BIN-RC_breakdown.dat
grep "Elapsed time for apply phase" outTimeBreak.log | awk '{print $10}' | tail -3 >> res_BIN-RC_breakdown.dat
grep "Time spent getting metadata" outTimeBreak.log | awk '{print $9}' | tail -3 >> res_BIN-RC_breakdown.dat

./config partransform stop
./runjava -f micro_timebreak_cat.dml -args 1 -stats &> outTimeBreak.log #RC Baseline
grep "Elapsed time for build phase" outTimeBreak.log | awk '{print $10}' | tail -3 >> res_RC_breakdown_base.dat
grep "Elapsed time for allocation" outTimeBreak.log | awk '{print $9}' | tail -3 >> res_RC_breakdown_base.dat
grep "Elapsed time for apply phase" outTimeBreak.log | awk '{print $10}' | tail -3 >> res_RC_breakdown_base.dat
grep "Time spent getting metadata" outTimeBreak.log | awk '{print $9}' | tail -3 >> res_RC_breakdown_base.dat
./runjava -f micro_timebreak_cat.dml -args 2 -stats &> outTimeBreak.log #DC Baseline
grep "Elapsed time for build phase" outTimeBreak.log | awk '{print $10}' | tail -3 >> res_DC_breakdown_base.dat
grep "Elapsed time for allocation" outTimeBreak.log | awk '{print $9}' | tail -3 >> res_DC_breakdown_base.dat
grep "Elapsed time for apply phase" outTimeBreak.log | awk '{print $10}' | tail -3 >> res_DC_breakdown_base.dat
grep "Time spent getting metadata" outTimeBreak.log | awk '{print $9}' | tail -3 >> res_DC_breakdown_base.dat

./runjava -f micro_timebreak_num.dml -stats &> outTimeBreak.log #BIN Baseline
grep "Elapsed time for build phase" outTimeBreak.log | awk '{print $10}' | tail -3 >> res_BIN-RC_breakdown_base.dat
grep "Elapsed time for allocation" outTimeBreak.log | awk '{print $9}' | tail -3 >> res_BIN-RC_breakdown_base.dat
grep "Elapsed time for apply phase" outTimeBreak.log | awk '{print $10}' | tail -3 >> res_BIN-RC_breakdown_base.dat
grep "Time spent getting metadata" outTimeBreak.log | awk '{print $9}' | tail -3 >> res_BIN-RC_breakdown_base.dat


./config partransform start
./config stagedtransform stop
sed -i "s+hadoop.root.logger=DEBUG,console+hadoop.root.logger=INFO,console+" ../libraries/log4j-silent.properties
rm data1.csv data2.csv  data.csv

exit
