#!/bin/bash

rm pca_cv_tf.dat
rm pca_cv_lima.dat

echo "Starting (10c) PCACV pipeline"
echo "-----------------------------"

# Disable cache spilling to avoid going out of disk space
# in AWS instances (30gb disk). This can hurt performance.
config lineagespill stop

execute() {
  for rep in {1..3}
  do
    cols=1000
    echo "Number of rows: $1, repetition: $rep"
    echo "Starting dml with reuse"
    start=$(date +%s%N)
    runjava -f pca_cv_helix.dml -args $1 0 -lineage reuse_multilevel -stats
    end=$(date +%s%N)
    echo -e $1'\t'$cols'\t'$((($end-$start)/1000000)) >> pca_cv_lima.dat

    # TF gets killed due to OOM for >100K rows
    source tf-venv/bin/activate
    echo "Starting TF with autograph"
    start=$(date +%s%N)
    python3 pca_cv_tf.py $1
    end=$(date +%s%N)
    echo -e $1'\t'$cols'\t'$((($end-$start)/1000000)) >> pca_cv_tf.dat
    deactivate
  done
}

for nrows in {50000..100000..50000}
do
  execute $nrows
done

for nrows in {200000..400000..100000}
do
  execute $nrows
done
config lineagespill start

exit


