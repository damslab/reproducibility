#!/bin/bash

rm autoenc_gpu.dat
rm autoenc_gpu_reuse.dat
rm autoenc_cpu.dat
rm autoenc_lima.dat
rm autoenc_coordl.dat

echo "Starting dropout rate optimization for autoencoder"
echo "-------------------------------------------------- "
# time calculated in milliseconds

for rep in {1..3}
do
  echo "repetition: $rep"
  start=$(date +%s%N)
  runjava -f autoencoder_kdd.dml -stats -gpu
  end=$(date +%s%N)
  echo -e $((($end-$start)/1000000)) >> autoenc_gpu.dat

  start=$(date +%s%N)
  runjava -f autoencoder_kdd.dml -stats -gpu -lineage reuse_multilevel
  end=$(date +%s%N)
  echo -e $((($end-$start)/1000000)) >> autoenc_gpu_reuse.dat

  start=$(date +%s%N)
  runjava -f autoencoder_kdd.dml -stats
  end=$(date +%s%N)
  echo -e $((($end-$start)/1000000)) >> autoenc_cpu.dat

  start=$(date +%s%N)
  runjava -f autoencoder_kdd.dml -stats -lineage reuse_multilevel
  end=$(date +%s%N)
  echo -e $((($end-$start)/1000000)) >> autoenc_lima.dat

  start=$(date +%s%N)
  runjava -f autoencoder_kdd_coordl.dml -stats -gpu
  end=$(date +%s%N)
  echo -e $((($end-$start)/1000000)) >> autoenc_coordl.dat



done

exit

