#!/bin/bash

nrkdd=95412
nckdd=7909
nraps=70000
ncaps=170

rm resexampleSyn.dat
rm resexampleSyn_reuse.dat
rm resexampleKdd.dat
rm resexampleKdd_reuse.dat
rm resexampleKdd_np.dat
rm resexampleKdd_np_reuse.dat

rm resexampleCVSyn.dat
rm resexampleCVSyn_reuse.dat
rm resexampleCVKdd.dat
rm resexampleCVKdd_reuse.dat
rm resexampleCVKdd_np.dat
rm resexampleCVKdd_np_reuse.dat

rm respcaSyn.dat
rm respcaSyn_reuse.dat
rm respcaKdd.dat
rm respcaKdd_reuse.dat
rm respcaKdd_np.dat
rm respcaKdd_np_reuse.dat

rm resl2svmSyn.dat
rm resl2svmSyn_reuse.dat
rm resl2svmAps.dat
rm resl2svmAps_reuse.dat
rm resl2svmKdd_np.dat
rm resl2svmKdd_np_reuse.dat

rm resenswpSyn.dat
rm resenswpSyn_reuse.dat
rm resenswpAps.dat
rm resenswpAps_reuse.dat
rm resenswpAps_np.dat
rm resenswpAps_np_reuse.dat


echo "Starting (9f) compare speedup for synthetic & real datasets"
echo "------------------------------------------------------------"
# time calculated in milliseconds

for rep in {1..3}
do
  echo "Starting 9f(a), repetition: $rep"
  start=$(date +%s%N)
  runjava -f gridsearchl2svm_kdd.dml -args KDD_synthetic -stats
  end=$(date +%s%N)
  echo -e $nraps'\t'$ncaps'\t'$((($end-$start)/1000000)) >> resl2svmSyn.dat

  start=$(date +%s%N)
  runjava -f gridsearchl2svm_kdd.dml -args KDD_synthetic -stats -lineage reuse_hybrid
  end=$(date +%s%N)
  echo -e $nraps'\t'$ncaps'\t'$((($end-$start)/1000000)) >> resl2svmSyn_reuse.dat

  start=$(date +%s%N)
  runjava -f gridsearchl2svm_kdd.dml -args KDD_prep -stats
  end=$(date +%s%N)
  echo -e $nraps'\t'$ncaps'\t'$((($end-$start)/1000000)) >> resl2svmKdd.dat

  start=$(date +%s%N)
  runjava -f gridsearchl2svm_kdd.dml -args KDD_prep -stats -lineage reuse_hybrid
  end=$(date +%s%N)
  echo -e $nraps'\t'$ncaps'\t'$((($end-$start)/1000000)) >> resl2svmKdd_reuse.dat

  start=$(date +%s%N)
  runjava -f gridsearchl2svm_kdd.dml -args KDD_noprep -stats
  end=$(date +%s%N)
  echo -e $nraps'\t'$ncaps'\t'$((($end-$start)/1000000)) >> resl2svmKdd_np.dat

  start=$(date +%s%N)
  runjava -f gridsearchl2svm_kdd.dml -args KDD_noprep -stats -lineage reuse_hybrid
  end=$(date +%s%N)
  echo -e $nraps'\t'$ncaps'\t'$((($end-$start)/1000000)) >> resl2svmKdd_np_reuse.dat
done

for rep in {1..3}
do
  echo "Starting 9f(b), repetition: $rep"
  start=$(date +%s%N)
  runjava -f gridsearchLM_kdd.dml -args KDD_synthetic -stats
  end=$(date +%s%N)
  echo -e $nrkdd'\t'$nckdd'\t'$((($end-$start)/1000000)) >> resexampleSyn.dat

  start=$(date +%s%N)
  runjava -f gridsearchLM_kdd.dml -args KDD_synthetic -stats -lineage reuse_hybrid
  end=$(date +%s%N)
  echo -e $nrkdd'\t'$nckdd'\t'$((($end-$start)/1000000)) >> resexampleSyn_reuse.dat

  start=$(date +%s%N)
  runjava -f gridsearchLM_kdd.dml -args KDD_prep -stats
  end=$(date +%s%N)
  echo -e $nrkdd'\t'$nckdd'\t'$((($end-$start)/1000000)) >> resexampleKdd.dat

  start=$(date +%s%N)
  runjava -f gridsearchLM_kdd.dml -args KDD_prep -stats -lineage reuse_hybrid
  end=$(date +%s%N)
  echo -e $nrkdd'\t'$nckdd'\t'$((($end-$start)/1000000)) >> resexampleKdd_reuse.dat

  start=$(date +%s%N)
  runjava -f gridsearchLM_kdd.dml -args KDD_noprep -stats
  end=$(date +%s%N)
  echo -e $nrkdd'\t'$nckdd'\t'$((($end-$start)/1000000)) >> resexampleKdd_np.dat

  start=$(date +%s%N)
  runjava -f gridsearchLM_kdd.dml -args KDD_noprep -stats -lineage reuse_hybrid
  end=$(date +%s%N)
  echo -e $nrkdd'\t'$nckdd'\t'$((($end-$start)/1000000)) >> resexampleKdd_np_reuse.dat
done

for rep in {1..3}
do
  echo "Starting 9f(c), repetition: $rep"
  start=$(date +%s%N)
  runjava -f gridsearchLM_cv_kdd.dml -args KDD_synthetic -stats
  end=$(date +%s%N)
  echo -e $nrkdd'\t'$nckdd'\t'$((($end-$start)/1000000)) >> resexampleCVSyn.dat

  start=$(date +%s%N)
  runjava -f gridsearchLM_cv_kdd.dml -args KDD_synthetic -stats -lineage reuse_hybrid
  end=$(date +%s%N)
  echo -e $nrkdd'\t'$nckdd'\t'$((($end-$start)/1000000)) >> resexampleCVSyn_reuse.dat

  start=$(date +%s%N)
  runjava -f gridsearchLM_cv_kdd.dml -args KDD_prep -stats
  end=$(date +%s%N)
  echo -e $nrkdd'\t'$nckdd'\t'$((($end-$start)/1000000)) >> resexampleCVKdd.dat

  start=$(date +%s%N)
  runjava -f gridsearchLM_cv_kdd.dml -args KDD_prep -stats -lineage reuse_hybrid
  end=$(date +%s%N)
  echo -e $nrkdd'\t'$nckdd'\t'$((($end-$start)/1000000)) >> resexampleCVKdd_reuse.dat

  start=$(date +%s%N)
  runjava -f gridsearchLM_cv_kdd.dml -args KDD_noprep -stats
  end=$(date +%s%N)
  echo -e $nrkdd'\t'$nckdd'\t'$((($end-$start)/1000000)) >> resexampleCVKdd_np.dat

  start=$(date +%s%N)
  runjava -f gridsearchLM_cv_kdd.dml -args KDD_noprep -stats -lineage reuse_hybrid
  end=$(date +%s%N)
  echo -e $nrkdd'\t'$nckdd'\t'$((($end-$start)/1000000)) >> resexampleCVKdd_np_reuse.dat
done

for rep in {1..3}
do
  echo "Starting 9f(d), repetition: $rep"
  start=$(date +%s%N)
  runjava -f enswpvoting_aps.dml -args APS_synthetic -stats
  end=$(date +%s%N)
  echo -e $nraps'\t'$ncaps'\t'$((($end-$start)/1000000)) >> resenswpSyn.dat

  start=$(date +%s%N)
  runjava -f enswpvoting_aps.dml -args APS_synthetic -stats -lineage reuse_hybrid
  end=$(date +%s%N)
  echo -e $nraps'\t'$ncaps'\t'$((($end-$start)/1000000)) >> resenswpSyn_reuse.dat

  start=$(date +%s%N)
  runjava -f enswpvoting_aps.dml -args APS_prep -stats
  end=$(date +%s%N)
  echo -e $nraps'\t'$ncaps'\t'$((($end-$start)/1000000)) >> resenswpAps.dat

  start=$(date +%s%N)
  runjava -f enswpvoting_aps.dml -args APS_prep -stats -lineage reuse_hybrid
  end=$(date +%s%N)
  echo -e $nraps'\t'$ncaps'\t'$((($end-$start)/1000000)) >> resenswpAps_reuse.dat

  start=$(date +%s%N)
  runjava -f enswpvoting_aps.dml -args APS_noprep -stats
  end=$(date +%s%N)
  echo -e $nraps'\t'$ncaps'\t'$((($end-$start)/1000000)) >> resenswpAps_np.dat

  start=$(date +%s%N)
  runjava -f enswpvoting_aps.dml -args APS_noprep -stats -lineage reuse_hybrid
  end=$(date +%s%N)
  echo -e $nraps'\t'$ncaps'\t'$((($end-$start)/1000000)) >> resenswpAps_np_reuse.dat
done

for rep in {1..3}
do
  echo "Starting 9f(e), repetition: $rep"
  start=$(date +%s%N)
  runjava -f pca_pipeline_kdd.dml -args KDD_synthetic -stats
  end=$(date +%s%N)
  echo -e $nrkdd'\t'$nckdd'\t'$((($end-$start)/1000000)) >> respcaSyn.dat

  start=$(date +%s%N)
  runjava -f pca_pipeline_kdd.dml -args KDD_synthetic -stats -lineage reuse_hybrid
  end=$(date +%s%N)
  echo -e $nrkdd'\t'$nckdd'\t'$((($end-$start)/1000000)) >> respcaSyn_reuse.dat

  start=$(date +%s%N)
  runjava -f pca_pipeline_kdd.dml -args KDD_prep -stats
  end=$(date +%s%N)
  echo -e $nrkdd'\t'$nckdd'\t'$((($end-$start)/1000000)) >> respcaKdd.dat

  start=$(date +%s%N)
  runjava -f pca_pipeline_kdd.dml -args KDD_prep -stats -lineage reuse_hybrid
  end=$(date +%s%N)
  echo -e $nrkdd'\t'$nckdd'\t'$((($end-$start)/1000000)) >> respcaKdd_reuse.dat

  start=$(date +%s%N)
  runjava -f pca_pipeline_kdd.dml -args KDD_noprep -stats
  end=$(date +%s%N)
  echo -e $nrkdd'\t'$nckdd'\t'$((($end-$start)/1000000)) >> respcaKdd_np.dat

  start=$(date +%s%N)
  runjava -f pca_pipeline_kdd.dml -args KDD_noprep -stats -lineage reuse_hybrid
  end=$(date +%s%N)
  echo -e $nrkdd'\t'$nckdd'\t'$((($end-$start)/1000000)) >> respcaKdd_np_reuse.dat
done

exit

