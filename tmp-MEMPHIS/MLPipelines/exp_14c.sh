#!/bin/bash

rm E2G_gpu.dat
rm E2G_gpu_reusemulti.dat
rm E2G_gpu_reusefull.dat
rm E2G_clipper.dat

echo "Starting E2G translation scoring"
echo "--------------------------------"
# time calculated in milliseconds

for rep in {1..3}
do
  echo "repetition: $rep"
  start=$(date +%s%N)
  runjava -f translation_E2G.dml -stats -gpu
  end=$(date +%s%N)
  echo -e $((($end-$start)/1000000)) >> E2G_gpu.dat

  start=$(date +%s%N)
  runjava -f translation_E2G.dml -stats -gpu -lineage reuse_multilevel
  end=$(date +%s%N)
  echo -e $((($end-$start)/1000000)) >> E2G_gpu_reusemulti.dat

  start=$(date +%s%N)
  runjava -f translation_E2G.dml -stats -gpu -lineage reuse_full
  end=$(date +%s%N)
  echo -e $((($end-$start)/1000000)) >> E2G_gpu_reusefull.dat

  start=$(date +%s%N)
  runjava -f translation_E2G_clipper.dml -stats -gpu
  end=$(date +%s%N)
  echo -e $((($end-$start)/1000000)) >> E2G_clipper.dat

done

exit

