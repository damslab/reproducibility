#!/bin/bash

rows=100000
cols=1000
sp=1.0

rm resmicroevic_auto.dat
rm resmicroevic_auto_lru.dat
rm resmicroevic_auto_cs.dat
rm resmicroevic_auto_dh.dat
rm resmicroevic_auto_inf.dat

rm resmicroevic_stplm.dat
rm resmicroevic_stplm_lru.dat
rm resmicroevic_stplm_cs.dat
rm resmicroevic_stplm_dh.dat
rm resmicroevic_stplm_inf.dat

# time calculated in milliseconds

echo "Starting (8b) Pipeline Comparison microbenchmark"
echo "------------------------------------------------"

config lineagespill stop  #disable disk-based reuse

for rep in {1..3}
do
  start=$(date +%s%N)
  runjava -f micro_autoencoder.dml -stats 
  end=$(date +%s%N)
  echo -e $rows'\t'$cols'\t'$sp'\t'$((($end-$start)/1000000)) >> resmicroevic_auto.dat

  start=$(date +%s%N)
  runjava -f micro_autoencoder.dml -lineage reuse_full policy_lru -stats 
  end=$(date +%s%N)
  echo -e $rows'\t'$cols'\t'$sp'\t'$((($end-$start)/1000000)) >> resmicroevic_auto_lru.dat

  start=$(date +%s%N)
  runjava -f micro_autoencoder.dml -lineage reuse_full policy_costnsize -stats 
  end=$(date +%s%N)
  echo -e $rows'\t'$cols'\t'$sp'\t'$((($end-$start)/1000000)) >> resmicroevic_auto_cs.dat

  start=$(date +%s%N)
  runjava -f micro_autoencoder.dml -lineage reuse_full policy_dagheight -stats 
  end=$(date +%s%N)
  echo -e $rows'\t'$cols'\t'$sp'\t'$((($end-$start)/1000000)) >> resmicroevic_auto_dh.dat

#---------------------------------------------------#

  start=$(date +%s%N)
  runjava -f micro_stplm.dml -stats 
  end=$(date +%s%N)
  echo -e $rows'\t'$cols'\t'$sp'\t'$((($end-$start)/1000000)) >> resmicroevic_stplm.dat

  start=$(date +%s%N)
  runjava -f micro_stplm.dml -lineage reuse_full policy_lru -stats 
  end=$(date +%s%N)
  echo -e $rows'\t'$cols'\t'$sp'\t'$((($end-$start)/1000000)) >> resmicroevic_stplm_lru.dat

  start=$(date +%s%N)
  runjava -f micro_stplm.dml -lineage reuse_full policy_costnsize -stats 
  end=$(date +%s%N)
  echo -e $rows'\t'$cols'\t'$sp'\t'$((($end-$start)/1000000)) >> resmicroevic_stplm_cs.dat

  start=$(date +%s%N)
  runjava -f micro_stplm.dml -lineage reuse_full policy_dagheight -stats 
  end=$(date +%s%N)
  echo -e $rows'\t'$cols'\t'$sp'\t'$((($end-$start)/1000000)) >> resmicroevic_stplm_dh.dat

done

config lineagespill start  #enable disk-spilling

# CostnSize results can be used as inifinite due to 0 cache misses
cp resmicroevic_auto_cs.dat resmicroevic_auto_inf.dat
cp resmicroevic_stplm_cs.dat resmicroevic_stplm_inf.dat

exit

