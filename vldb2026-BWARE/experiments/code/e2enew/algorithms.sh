#!/bin/bash

export LOG4JPROP='code/logging/log4j-compression.properties'

logstart="results/algorithms"
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"

echo "code/e2enew/algorithms.sh"
exrep=1
profileEnabled=1

run() {
   alg=$1
   conf="code/conf/$2.xml"
   mode=$3

   shift 3

   logDir="$logstart/$HOSTNAME/$alg/$conf/$mode"

   # make log string correct.
   t=$IFS
   IFS="_"
   lname="$*"
   lname="${lname//'/'/'-'}"
   log="$logDir/$lname.log"
   IFS=$t

   if [ -f "$log" ]; then
      mv $log "$log$(date +"%m-%d-%y-%r").log"
   fi

   echo -n "--- Log : $log "
   i=1
   for i in $(seq $exrep); do

      if [ $profileEnabled == 1 ]; then
         mkdir -p "$log-perf"
         profile="$log-perf/$i.profile.html"
         export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/lib/libasyncProfiler.so=start,event=cpu,file=$profile"
      fi

      perf stat -d -d -d \
         timeout 2000 \
         systemds \
         code/e2enew/$alg.dml \
         -config $conf \
         -stats 100 -debug \
         -exec $mode \
         -seed $seed \
         -args $* \
         >>$log 2>&1
      # -explain \
      echo -n "."

      export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"
   done
   echo ""
}

removetmp() {
   rm -fr $1.tmp
   rm -fr $1.tmp.dict
   rm -fr $1.tmp.mtd
   rm -fr $1.tmp.tmp
   rm -fr $1.tmp.tmp.dict
   rm -fr $1.tmp.tmp.mtd
}

makeData() {
   exrept=$exrep
   exrep=1
   run mtd_detect ULAb16 singlenode $1
   run mtd_compress ULAb16 singlenode $1
   exrep=$exrept
}

pca_first() {
   run pca_first ULAb16 singlenode $1.bin $2
   run pca_first TAWAb16 singlenode $1.cla $2
}

pca_last() {
   run pca_last ULAb16 singlenode $1.bin $2
   run pca_last TAWAb16 singlenode $1.cla $2
}

L2SVM_first(){
   run L2SVM_first ULAb16 singlenode $1.bin $2
   run L2SVM_first TAWAb16 singlenode $1.cla $2
}

L2SVM_last(){
   run L2SVM_last ULAb16 singlenode $1.bin $2
   run L2SVM_last TAWAb16 singlenode $1.cla $2
}

kmeans_last(){
   run kmeans_last ULAb16 singlenode $1.bin $2
   run kmeans_last TAWAb16 singlenode $1.cla $2
}

kmeans_first(){
   run kmeans_first ULAb16 singlenode $1.bin $2
   run kmeans_first TAWAb16 singlenode $1.cla $2
}

kmeans10_last(){
   run kmeans10_last ULAb16 singlenode $1.bin $2
   # run kmeans10_last TAWAb16 singlenode $1.cla $2
}

kmeans10_first(){
   run kmeans10_first ULAb16 singlenode $1.bin $2
   run kmeans10_first TAWAb16 singlenode $1.cla $2
}

# # # Cat
file="data/cat/train.csv"
# makeData $file
spec="code/scripts/specs/catindat_full.json"
pca_last $file $spec
L2SVM_last $file $spec
kmeans_last  $file $spec
kmeans10_last  $file $spec
spec="code/scripts/specs/catindat_l10.json"
pca_last $file $spec
L2SVM_last $file $spec
kmeans_last  $file $spec
kmeans10_last  $file $spec


# # # #  Criteo
# file="data/criteo/day_0_10000000.tsv"
# makeData $file
# spec="code/scripts/specs/criteo_full.json"
# pca_first $file $spec
# L2SVM_first $file $spec
# kmeans_first  $file $spec
# kmeans10_first  $file $spec
# spec="code/scripts/specs/criteo_l10.json"
# pca_first $file $spec
# L2SVM_first $file $spec
# kmeans_first  $file $spec
# kmeans10_first  $file $spec

# # #  Crypto
# file="data/crypto/train.csv"
# makeData $file
# spec="code/scripts/specs/crypto_full.json"
# pca_last $file $spec
# L2SVM_last $file $spec
# kmeans_last  $file $spec
# kmeans10_last  $file $spec
# spec="code/scripts/specs/crypto_10l.json"
# pca_last $file $spec
# L2SVM_last $file $spec
# kmeans_last  $file $spec
# kmeans10_last  $file $spec


# # ### Not really interesting:

# # # # Adult
# file="data/adult/adult.csv"
# # makeData $file
# spec="code/scripts/specs/adult_full.json"
# # pca_last $file $spec
# # L2SVM_last $file $spec
# # kmeans_last  $file $spec
# # kmeans10_last  $file $spec
# spec="code/scripts/specs/adult_l10.json"
# # pca_last $file $spec
# # L2SVM_last $file $spec
# # kmeans_last  $file $spec
# kmeans10_last  $file $spec

# # # # Sanatander
# # ## Not faster in compressed space
# file="data/santander/train.csv"
# makeData $file
# spec="code/scripts/specs/santander_full.json"
# pca_first $file $spec
# L2SVM_first $file $spec
# kmeans_first  $file $spec
# kmeans10_first  $file $spec
# spec="code/scripts/specs/santander_l10.json"
# pca_first $file $spec
# L2SVM_first $file $spec
# kmeans_first  $file $spec
# kmeans10_first  $file $spec

# # # # Home
# # ## Home does not converge in the Eigen computation
# file="data/home/train.csv"
# makeData $file
# spec="code/scripts/specs/home_full.json"
# pca_first $file $specs
# L2SVM_first $file $specs
# kmeans_first  $file $spec
# kmeans10_first  $file $spec
# spec="code/scripts/specs/home_l10.json"
# pca_first $file $spec
# L2SVM_first $file $specs
# kmeans_first  $file $spec
# kmeans10_first  $file $spec

# # # # # KDD
# # ## KDD  does not converge in the Eigen computation
# file="data/kdd98/cup98lrn.csv"
# makeData $file
# spec="code/scripts/specs/kdd_full.json"
# pca_last $file $spec
# L2SVM_last $file $specs
# kmeans_last  $file $spec
# kmeans10_last  $file $spec
# spec="code/scripts/specs/kdd_l10.json"
# pca_last $file $spec
# kmeans_last $file $specs
# kmeans_first  $file $spec
# kmeans10_last  $file $spec




