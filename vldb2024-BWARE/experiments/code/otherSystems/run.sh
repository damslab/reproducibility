#!/bin/bash

logstart="results/otherSystems"

echo "code/otherSystems/run.sh"
exrep=2

runPython() {

   alg=$1
   spec=$2
   data=$3
   header=$4
   delim=$5

   shift 3

   logDir="$logstart/$HOSTNAME/$alg"
   mkdir -p "$logDir"

   t=$IFS
   IFS="_"
   lname="$data"
   lname="${lname//'/'/'-'}"
   log="$logDir/$spec-$lname.log"
   IFS=$t

   if [ -f "$log" ]; then
      mv $log "$log$(date +"%m-%d-%y-%r").log"
   fi

   echo -n "--- Log : $log "

   echo -n "code/otherSystems/baseline_$alg.py "

   for i in $(seq $exrep); do
      perf stat -d -d -d \
         timeout 3000 \
         python \
         code/otherSystems/baseline_$alg.py \
         code/scripts/specs/$spec.json \
         data/$data \
         $header $delim >>$log 2>&1
      echo -n "."

   done
   echo ""
}

runDML() {

   alg=$1
   spec=$2
   data=$3
   conf=$4

   shift 4

   logDir="$logstart/$HOSTNAME/$alg"
   mkdir -p "$logDir"

   t=$IFS
   IFS="_"
   lname="$data"
   lname="${lname//'/'/'-'}"
   log="$logDir/$spec-$lname-$conf.log"
   IFS=$t

   conf="code/conf/$conf.xml"

   if [ -f "$log" ]; then
      mv $log "$log$(date +"%m-%d-%y-%r").log"
   fi

   echo -n "--- Log : $log "

   for i in $(seq $exrep); do
      perf stat -d -d -d \
         timeout 3000 \
         systemds \
         code/otherSystems/baseline_$alg.dml \
         -config $conf \
         -stats 100 -debug \
         -exec singlenode \
         -seed $seed \
         -args \
         data/$data \
         code/scripts/specs/$spec.json \
         >>$log 2>&1
      echo -n "."

   done
   echo ""
}

## Sad situation
# runPython pd adult_full adult/adult.csv 0
# runPython pl adult_full adult/adult.csv 0
# runPython sk adult_full adult/adult.csv 0
# runPython tf adult_full adult/adult.csv 0
# runPython torch adult_full adult/adult.csv 0

# runDML def adult_full adult/adult.csv ULAb16
# runDML tra adult_full adult/adult.csv ULAb16
# runDML def adult_full adult/adult.csv TAWAb16
# runDML tra adult_full adult/adult.csv TAWAb16
# runDML comp adult_full adult/adult.csv TAWAb16

# runPython pd home_full home/train.csv 1
# runPython pl home_full home/train.csv 1
# runPython sk home_full home/train.csv
# runPython tf home_full home/train.csv
# runPython torch home_full home/train.csv
# runPython dask home_full home/train.csv

# runDML def home_full home/train.csv ULAb16
# runDML tra home_full home/train.csv ULAb16
# runDML def home_full home/train.csv TAWAb16
# runDML tra home_full home/train.csv TAWAb16
# runDML comp home_full home/train.csv TAWAb16

# runPython pd catindat_full cat/train.csv 1 ,
# runPython pl catindat_full cat/train.csv 1 ,
# runPython sk catindat_full cat/train.csv 1 ,
# runPython tf catindat_full cat/train.csv 1 ,

# runDML def catindat_full cat/train.csv ULAb16
# runDML tra catindat_full cat/train.csv ULAb16
# runDML def catindat_full cat/train.csv TAWAb16
# runDML tra catindat_full cat/train.csv TAWAb16
# runDML comp catindat_full cat/train.csv TAWAb16

d=("day_0_100000 day_0_1000000 day_0_10000000")
d=("day_0_100000000")
for x in $d; do

   runPython pd criteo_full criteo/$x.tsv 0 t
   runPython pl criteo_full criteo/$x.tsv 0 t
   runPython sk criteo_full criteo/$x.tsv 0 t
   runPython tf criteo_full criteo/$x.tsv 0 t

   runDML def criteo_full criteo/$x.tsv ULAb16
   runDML tra criteo_full criteo/$x.tsv ULAb16
   runDML def criteo_full criteo/$x.tsv TAWAb16
   runDML tra criteo_full criteo/$x.tsv TAWAb16
   runDML comp criteo_full criteo/$x.tsv TAWAb16
done
