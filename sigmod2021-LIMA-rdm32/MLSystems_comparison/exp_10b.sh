#!/bin/bash

nrows=95412
cols=469

rm respcanb_kdd.dat
rm respcanb_kdd_reuse.dat
rm respcanb_aps.dat
rm respcanb_aps_reuse.dat
rm respcanb_kdd_sk.dat
rm respcanb_aps_sk.dat

echo "Starting (10b) PCANB with KDD & APS dataset "
echo "--------------------------------------------"
# time calculated in milliseconds

for rep in {1..3}
do
  start=$(date +%s%N)
  runjava -f pcaNB_kdd.dml -stats
  end=$(date +%s%N)
  echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> respcanb_kdd.dat

  start=$(date +%s%N)
  runjava -f pcaNB_kdd.dml -stats -lineage reuse_hybrid
  end=$(date +%s%N)
  echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> respcanb_kdd_reuse.dat

  start=$(date +%s%N)
  runjava -f pcaNB_aps.dml -stats 
  end=$(date +%s%N)
  echo -e 70000'\t'170'\t'$((($end-$start)/1000000)) >> respcanb_aps.dat

  start=$(date +%s%N)
  runjava -f pcaNB_aps.dml -stats -lineage reuse_hybrid
  end=$(date +%s%N)
  echo -e 70000'\t'170'\t'$((($end-$start)/1000000)) >> respcanb_aps_reuse.dat

  echo "Starting sklearn"
  source tf-venv/bin/activate
  start=$(date +%s%N)
  python3 pcaNB_kdd_sk.py
  end=$(date +%s%N)
  echo -e $nrows'\t'$cols'\t'$((($end-$start)/1000000)) >> respcanb_kdd_sk.dat

  start=$(date +%s%N)
  python3 pcaNB_aps_sk.py
  end=$(date +%s%N)
  echo -e 70000'\t'170'\t'$((($end-$start)/1000000)) >> respcanb_aps_sk.dat
  deactivate
done


exit

