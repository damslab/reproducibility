#!/bin/bash

nrows=95412
cols=7909
nh1=500
nh2=2
nepochs=10

rm resautoen.dat
rm resautoen_reuse.dat
rm resautoen_tf.dat
rm resautoen_tfg.dat
rm resautoen_tfg_xla.dat

echo "Starting (10a-1) Autoencoder with KDD dataset "
echo "-----------------------------------------------"
# time calculated in milliseconds

for rep in {1..3}
do
  echo "Number of epochs: $nepochs, repetition: $rep"
  echo "Starting dml with codegen"
  config codegen start
  source config mkl start
  start=$(date +%s%N)
  runjava -f autoencoder_kdd.dml -args 500 2 $nepochs 256
  end=$(date +%s%N)
  echo -e $nh1'\t'$nh2'\t'$nepochs'\t'$((($end-$start)/1000000)) >> resautoen.dat

  echo "Starting dml with codegen with reuse"
  start=$(date +%s%N)
  runjava -f autoencoder_kdd.dml -args 500 2 $nepochs 256 -lineage reuse_hybrid policy_dagheight
  end=$(date +%s%N)
  echo -e $nh1'\t'$nh2'\t'$nepochs'\t'$((($end-$start)/1000000)) >> resautoen_reuse.dat
  config codegen stop
  config mkl stop

  echo "Starting TF"
  source tf-venv/bin/activate
  start=$(date +%s%N)
  python3 autoencoderKdd_tf.py 500 2 $nepochs 256
  end=$(date +%s%N)
  echo -e $nh1'\t'$nh2'\t'$nepochs'\t'$((($end-$start)/1000000)) >> resautoen_tf.dat

  echo "Starting TF with autograph"
  start=$(date +%s%N)
  python3 autoencoderKdd_tfg.py 500 2 $nepochs 256
  end=$(date +%s%N)
  echo -e $nh1'\t'$nh2'\t'$nepochs'\t'$((($end-$start)/1000000)) >> resautoen_tfg.dat

  echo "Starting TF-XLA with autograph"
  start=$(date +%s%N)
  python-xla autoencoderKdd_tfg.py 500 2 $nepochs 256
  end=$(date +%s%N)
  echo -e $nh1'\t'$nh2'\t'$nepochs'\t'$((($end-$start)/1000000)) >> resautoen_tfg_xla.dat
  deactivate
done

exit

