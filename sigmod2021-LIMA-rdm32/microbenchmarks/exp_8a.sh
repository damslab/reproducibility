#!/bin/bash

rm resmicroeviction.dat 
rm resmicroeviction_lru.dat 
rm resmicroeviction_cs.dat 
rm resmicroeviction_inf.dat 

# time calculated in milliseconds

echo "Starting (8a) Pipeline with Phases microbenchmark"
echo "--------------------------------------------------"

config lineagespill stop  #disable spilling

for rep in {1..5}
do
  start=$(date +%s%N)
  runjava -f micro_eviction.dml -stats > tmp.out
  end=$(date +%s%N)
  p1_base="$(grep Phase1 tmp.out|awk '{print $3}')"
  p2="$(grep Phase2 tmp.out|awk '{print $3}')"
  p3="$(grep Phase3 tmp.out|awk '{print $3}')"
  echo -e ${p1_base%.*}'\t'${p2%.*}'\t'${p3%.*} >> resmicroeviction.dat

  start=$(date +%s%N)
  runjava -f micro_eviction.dml -stats -lineage reuse_full policy_lru > tmp.out
  end=$(date +%s%N)
  p1="$(grep Phase1 tmp.out|awk '{print $3}')"
  p2_lru="$(grep Phase2 tmp.out|awk '{print $3}')"
  p3="$(grep Phase3 tmp.out|awk '{print $3}')"
  echo -e ${p1%.*}'\t'${p2_lru%.*}'\t'${p3%.*} >> resmicroeviction_lru.dat

  start=$(date +%s%N)
  runjava -f micro_eviction.dml -stats -lineage reuse_full policy_costnsize > tmp.out
  end=$(date +%s%N)
  p1="$(grep Phase1 tmp.out|awk '{print $3}')"
  p2="$(grep Phase2 tmp.out|awk '{print $3}')"
  p3="$(grep Phase3 tmp.out|awk '{print $3}')"
  echo -e ${p1%.*}'\t'${p2%.*}'\t'${p3%.*} >> resmicroeviction_cs.dat

  # p1_inf = phase1 time of base
  # p2_inf = phase2 time of lru (fully reused)
  # p3_inf = ~0 (fully reused results of phase1)
  p3=1
  echo -e ${p1_base%.*}'\t'${p2_lru%.*}'\t'${p3%.*} >> resmicroeviction_inf.dat
done

rm tmp.out
config lineagespill start  #enable spilling
exit
