#!/bin/bash

export LOG4JPROP='code/logging/log4j-compression.properties'

logstart="results/poly"
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"

echo "code/e2enew/poly.sh"
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
         timeout 3600 \
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


binary_lm_1() {


   run mtd_detect ULAb16 singlenode $1
   run binary_lm_1 ULAb16 singlenode $1.bin $2
   run binary_lm_1_poly_2 ULAb16 singlenode $1.bin $2
   run binary_lm_1_poly_3 ULAb16 singlenode $1.bin $2
   run binary_lm_1_poly_4 ULAb16 singlenode $1.bin $2
   run binary_lm_1_poly_5 ULAb16 singlenode $1.bin $2
   run binary_lm_1_poly_6 ULAb16 singlenode $1.bin $2
   run binary_lm_1_poly_7 ULAb16 singlenode $1.bin $2
   run binary_lm_1_poly_8 ULAb16 singlenode $1.bin $2
   run binary_lm_1_poly_9 ULAb16 singlenode $1.bin $2



   run mtd_compress ULAb16 singlenode $1
   run binary_lm_1 TAWAb16 singlenode $1.cla $2
   run binary_lm_1_poly_2 TAWAb16 singlenode $1.cla $2
   run binary_lm_1_poly_3 TAWAb16 singlenode $1.cla $2
   run binary_lm_1_poly_4 TAWAb16 singlenode $1.cla $2
   run binary_lm_1_poly_5 TAWAb16 singlenode $1.cla $2
   run binary_lm_1_poly_6 TAWAb16 singlenode $1.cla $2
   run binary_lm_1_poly_7 TAWAb16 singlenode $1.cla $2
   run binary_lm_1_poly_8 TAWAb16 singlenode $1.cla $2
   run binary_lm_1_poly_9 TAWAb16 singlenode $1.cla $2

}

binary_lm_last() {


   run mtd_detect ULAb16 singlenode $1
   run binary_lm_last ULAb16 singlenode $1.bin $2
   run binary_lm_last_poly_2 ULAb16 singlenode $1.bin $2
   run binary_lm_last_poly_3 ULAb16 singlenode $1.bin $2
   run binary_lm_last_poly_4 ULAb16 singlenode $1.bin $2
   run binary_lm_last_poly_5 ULAb16 singlenode $1.bin $2
   run binary_lm_last_poly_6 ULAb16 singlenode $1.bin $2
   run binary_lm_last_poly_7 ULAb16 singlenode $1.bin $2
   run binary_lm_last_poly_8 ULAb16 singlenode $1.bin $2
   run binary_lm_last_poly_9 ULAb16 singlenode $1.bin $2




   run mtd_compress ULAb16 singlenode $1
   run binary_lm_last TAWAb16 singlenode $1.cla $2
   run binary_lm_last_poly_2 TAWAb16 singlenode $1.cla $2
   run binary_lm_last_poly_3 TAWAb16 singlenode $1.cla $2
   run binary_lm_last_poly_4 TAWAb16 singlenode $1.cla $2
   run binary_lm_last_poly_5 TAWAb16 singlenode $1.cla $2
   run binary_lm_last_poly_6 TAWAb16 singlenode $1.cla $2
   run binary_lm_last_poly_7 TAWAb16 singlenode $1.cla $2
   run binary_lm_last_poly_8 TAWAb16 singlenode $1.cla $2
   run binary_lm_last_poly_9 TAWAb16 singlenode $1.cla $2

}

regress_lm() {

   run mtd_detect ULAb16 singlenode $1
   run regress_lm ULAb16 singlenode $1.bin $2
   run regress_lm_poly_2 ULAb16 singlenode $1.bin $2
   run regress_lm_poly_3 ULAb16 singlenode $1.bin $2
   run regress_lm_poly_4 ULAb16 singlenode $1.bin $2
   run regress_lm_poly_5 ULAb16 singlenode $1.bin $2
   run regress_lm_poly_6 ULAb16 singlenode $1.bin $2
   run regress_lm_poly_7 ULAb16 singlenode $1.bin $2
   run regress_lm_poly_8 ULAb16 singlenode $1.bin $2
   run regress_lm_poly_9 ULAb16 singlenode $1.bin $2

   run mtd_compress ULAb16 singlenode $1
   run regress_lm TAWAb16 singlenode $1.cla $2
   run regress_lm_poly_2 TAWAb16 singlenode $1.cla $2
   run regress_lm_poly_3 TAWAb16 singlenode $1.cla $2
   run regress_lm_poly_4 TAWAb16 singlenode $1.cla $2
   run regress_lm_poly_5 TAWAb16 singlenode $1.cla $2
   run regress_lm_poly_6 TAWAb16 singlenode $1.cla $2
   run regress_lm_poly_7 TAWAb16 singlenode $1.cla $2
   run regress_lm_poly_8 TAWAb16 singlenode $1.cla $2
   run regress_lm_poly_9 TAWAb16 singlenode $1.cla $2
}

# binary -- last column

# # Adult
# file="data/adult/adult.csv"
# spec="code/scripts/specs/adult"
# binary_lm_last $file ${spec}_full.json
# binary_lm_last $file ${spec}_l10.json

# # Sanatander
# file="data/santander/train.csv"
# spec="code/scripts/specs/santander"
# binary_lm_1 $file ${spec}_full.json
# binary_lm_1 $file ${spec}_l10.json

# # Home
# file="data/home/train.csv"
# spec="code/scripts/specs/home"
# binary_lm_1 $file ${spec}_full.json
# binary_lm_1 $file ${spec}_l10.json

# # KDD
# file="data/kdd98/cup98lrn.csv"
# spec="code/scripts/specs/kdd"
# regress_lm $file ${spec}_l10.json
# regress_lm $file ${spec}_full.json

# Crypto
# file="data/crypto/train.csv"
# spec="code/scripts/specs/crypto"
# # regress_lm $file ${spec}_full.json
# regress_lm $file ${spec}_l10.json
