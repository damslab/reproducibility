#!/bin/bash

rm ft_cifar.dat
rm ft_cifar_reusefull.dat
rm ft_imagenet.dat
rm ft_imagenet_reusefull.dat

echo "Starting transfer learning"
echo "---------------------------"
# time calculated in milliseconds

for rep in {1..3}
do
  echo "repetition: $rep"
  config2 all stop
  start=$(date +%s%N)
  runjava -f featureExtraction.dml -args cifar -stats -gpu
  end=$(date +%s%N)
  echo -e $((($end-$start)/1000000)) >> ft_cifar.dat

  start=$(date +%s%N)
  runjava -f featureExtraction.dml -args cifar -stats -gpu -lineage reuse_full
  end=$(date +%s%N)
  echo -e $((($end-$start)/1000000)) >> ft_cifar_reusefull.dat

  start=$(date +%s%N)
  runjava -f featureExtraction.dml -args imagenet -stats -gpu
  end=$(date +%s%N)
  echo -e $((($end-$start)/1000000)) >> ft_imagenet.dat

  start=$(date +%s%N)
  runjava -f featureExtraction.dml -args imagenet -stats -gpu -lineage reuse_full
  end=$(date +%s%N)
  echo -e $((($end-$start)/1000000)) >> ft_imagenet_reusefull.dat



done

exit

