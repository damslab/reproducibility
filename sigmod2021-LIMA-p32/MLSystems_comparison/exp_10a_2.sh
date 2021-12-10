#!/bin/bash

nrows=95412
cols=469

rm respcacvkdd.dat
rm respcacvkdd_reuse.dat
rm respcacvkdd_helix.dat
rm respcacvkdd_tfg.dat

echo "Starting (10a-2) PCACV with KDD dataset "
echo "-----------------------------------------"
# time calculated in milliseconds

for rep in {1..3}
do
  start=$(date +%s%N)
  runjava -f pcacv_kdd_helix.dml -args 0 -stats
  end=$(date +%s%N)
  echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> respcacvkdd.dat

  start=$(date +%s%N)
  runjava -f pcacv_kdd_helix.dml -args 0 -stats -lineage reuse_multilevel
  end=$(date +%s%N)
  echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> respcacvkdd_reuse.dat

  start=$(date +%s%N)
  runjava -f pcacv_kdd_helix.dml -args 1 -stats
  end=$(date +%s%N)
  echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> respcacvkdd_helix.dat

  echo "Starting TF"
  source tf-venv/bin/activate
  start=$(date +%s%N)
  python3 pcacv_kdd_tf.py
  end=$(date +%s%N)
  echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> respcacvkdd_tf.dat

  start=$(date +%s%N)
  python3 pcacv_kdd_tfg.py
  end=$(date +%s%N)
  echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> respcacvkdd_tfg.dat

  start=$(date +%s%N)
  python-xla pcacv_kdd_tfg.py
  end=$(date +%s%N)
  echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> respcacvkdd_tfg_xla.dat
  deactivate
done


exit

