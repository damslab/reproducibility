#!/bin/bash

echo "Running Read and Write Real datasets experiments"

export LOG4JPROP='code/logging/log4j-compression.properties'

exrep=3
clear=1
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"
profileEnabled=1
mode="singlenode"

run() {

    if [ ! -f "$1" ] || [ $clear == 1 ]; then
        if [ -f "$1" ]; then
             mv $1 "$1$(date +"%m-%d-%y-%r").log"
        fi


        echo -n "--- Read  : $1   "

        for i in $(seq $exrep); do
            if [ $profileEnabled == 1 ]; then
                mkdir -p "$1-perf"
                profile="$1-perf/$i.profile.html"
                export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/lib/libasyncProfiler.so=start,event=cpu,file=$profile"
            fi
            perf stat -d -d -d \
                timeout 200 \
                systemds \
                code/ReadWrite/dataset/$4.dml \
                -config code/conf/${3}b$5.xml \
                -stats 100 \
                -exec "$mode" \
                -debug \
                -seed $seed \
                -args $2 $6\
                >>$1 2>&1
            
            du $2.tmp >>$1
            du $2.tmp.mtd >>$1
            if [ -f "$2.tmp.dict" ]; then
                du $2.tmp.dict >>$1
            fi
            du $2 >>$1
            du $2.mtd >>$1
            export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"

            echo -n "."
        done

        echo ""
    fi
}

removetmp(){
    rm -fr $1.tmp
    rm -fr $1.tmp.dict
    rm -fr $1.tmp.mtd
    rm -fr $1.tmp.tmp
    rm -fr $1.tmp.tmp.dict
    rm -fr $1.tmp.tmp.mtd
}


echo code/ReadWrite/datasetsTE.sh

mkdir -p "results/TE/$HOSTNAME/"

fullLogName="results/TE/$HOSTNAME/FM-"

file="data/cat/train.csv"
spec="code/scripts/specs/catindat_full.json"
run $fullLogName-cat-FM.log $file ULA mtd_te 16 $spec
removetmp $file
run $fullLogName-cat-FMCD.log $file ULA mtd_te_compress 16 $spec
removetmp $file
run $fullLogName-cat-FCMD.log $file TULA mtd_te 16 $spec
run $fullLogName-cat-FCMCD.log $file TULA mtd_te_compress 16 $spec
removetmp $file
run $fullLogName-cat-CFCMD.log $file TCLA mtd_te 16 $spec
run $fullLogName-cat-CFCMCD.log $file TCLA mtd_te_compress 16 $spec
removetmp $file
run $fullLogName-cat-uf.log $file ULA mtd_detect 16
run $fullLogName-cat-RFCMCD.log $file.tmp TCLA mtd_te_compress 16 $spec
removetmp $file
run $fullLogName-cat-cf.log $file ULA mtd_compress 16
run $fullLogName-cat-RCFCMCD.log $file.tmp TCLA mtd_te_compress 16 $spec
run $fullLogName-cat-RCFMCD.log $file.tmp TULA mtd_te_compress 16 $spec
removetmp $file





file="data/adult/adult.csv"
spec="code/scripts/specs/adult_full.json"
run $fullLogName-adult-FM.log $file ULA mtd_te 16 $spec
removetmp $file
run $fullLogName-adult-FMCD.log $file ULA mtd_te_compress 16 $spec
removetmp $file
run $fullLogName-adult-FCMD.log $file TULA mtd_te 16 $spec
removetmp $file
run $fullLogName-adult-FCMCD.log $file TULA mtd_te_compress 16 $spec
removetmp $file
run $fullLogName-adult-CFCMD.log $file TCLA mtd_te 16 $spec
removetmp $file
run $fullLogName-adult-CFCMCD.log $file TCLA mtd_te_compress 16 $spec
removetmp $file

run $fullLogName-adult-uf.log $file ULA mtd_detect 16
run $fullLogName-adult-RFCMCD.log $file.tmp TCLA mtd_te_compress 16 $spec
removetmp $file

run $fullLogName-adult-cf.log $file ULA mtd_compress 16
run $fullLogName-adult-RCFCMCD.log $file.tmp TCLA mtd_te_compress 16 $spec
run $fullLogName-adult-RCFMCD.log $file.tmp TULA mtd_te_compress 16 $spec
removetmp $file





file="data/kdd98/cup98lrn.csv"
spec="code/scripts/specs/kdd_full.json"
run $fullLogName-kdd-FM.log $file ULA mtd_te 16 $spec
removetmp $file
run $fullLogName-kdd-FMCD.log $file ULA mtd_te_compress 16 $spec
removetmp $file
run $fullLogName-kdd-FCMD.log $file TULA mtd_te 16 $spec
run $fullLogName-kdd-FCMCD.log $file TULA mtd_te_compress 16 $spec
removetmp $file
run $fullLogName-kdd-CFCMD.log $file TCLA mtd_te 16 $spec
run $fullLogName-kdd-CFCMCD.log $file TCLA mtd_te_compress 16 $spec
removetmp $file

run $fullLogName-kdd-uf.log $file ULA mtd_detect 16
run $fullLogName-kdd-RFCMCD.log $file.tmp TCLA mtd_te_compress 16 $spec
removetmp $file

run $fullLogName-kdd-cf.log $file ULA mtd_compress 16
run $fullLogName-kdd-RCFCMCD.log $file.tmp TCLA mtd_te_compress 16 $spec
run $fullLogName-kdd-RCFMCD.log $file.tmp TULA mtd_te_compress 16 $spec
removetmp $file



file="data/salaries/train.csv"
spec="code/scripts/specs/salaries_full.json"
run $fullLogName-salaries-FM.log $file ULA mtd_te 16 $spec
removetmp $file
run $fullLogName-salaries-FMCD.log $file ULA mtd_te_compress 16 $spec
removetmp $file
run $fullLogName-salaries-FCMD.log $file TULA mtd_te 16 $spec
run $fullLogName-salaries-FCMCD.log $file TULA mtd_te_compress 16 $spec
removetmp $file
run $fullLogName-salaries-CFCMD.log $file TCLA mtd_te 16 $spec
run $fullLogName-salaries-CFCMCD.log $file TCLA mtd_te_compress 16 $spec
removetmp $file

run $fullLogName-salaries-uf.log $file ULA mtd_detect 16
run $fullLogName-salaries-RFCMCD.log $file.tmp TCLA mtd_te_compress 16 $spec
removetmp $file

run $fullLogName-salaries-cf.log $file ULA mtd_compress 16
run $fullLogName-salaries-RCFCMCD.log $file.tmp TCLA mtd_te_compress 16 $spec
run $fullLogName-salaries-RCFMCD.log $file.tmp TULA mtd_te_compress 16 $spec
removetmp $file



file="data/santander/train.csv"
spec="code/scripts/specs/santander_full.json"
run $fullLogName-santander-FM.log $file ULA mtd_te 16 $spec
removetmp $file
run $fullLogName-santander-FMCD.log $file ULA mtd_te_compress 16 $spec
removetmp $file
run $fullLogName-santander-FCMD.log $file TULA mtd_te 16 $spec
run $fullLogName-santander-FCMCD.log $file TULA mtd_te_compress 16 $spec
removetmp $file
run $fullLogName-santander-CFCMD.log $file TCLA mtd_te 16 $spec
run $fullLogName-santander-CFCMCD.log $file TCLA mtd_te_compress 16 $spec
removetmp $file

run $fullLogName-santander-uf.log $file ULA mtd_detect 16
run $fullLogName-santander-RFCMCD.log $file.tmp TCLA mtd_te_compress 16 $spec
removetmp $file

run $fullLogName-santander-cf.log $file ULA mtd_compress 16
run $fullLogName-santander-RCFCMCD.log $file.tmp TCLA mtd_te_compress 16 $spec
run $fullLogName-santander-RCFMCD.log $file.tmp TULA mtd_te_compress 16 $spec
removetmp $file




file="data/home/train.csv"
spec="code/scripts/specs/home_full.json"
run $fullLogName-home-FM.log $file ULA mtd_te 16 $spec
removetmp $file
run $fullLogName-home-FMCD.log $file ULA mtd_te_compress 16 $spec
removetmp $file
run $fullLogName-home-FCMD.log $file TULA mtd_te 16 $spec
run $fullLogName-home-FCMCD.log $file TULA mtd_te_compress 16 $spec
removetmp $file
run $fullLogName-home-CFCMD.log $file TCLA mtd_te 16 $spec
run $fullLogName-home-CFCMCD.log $file TCLA mtd_te_compress 16 $spec
removetmp $file

run $fullLogName-home-uf.log $file ULA mtd_detect 16
run $fullLogName-home-RFCMCD.log $file.tmp TCLA mtd_te_compress 16 $spec
removetmp $file

run $fullLogName-home-cf.log $file ULA mtd_compress 16
run $fullLogName-home-RCFCMCD.log $file.tmp TCLA mtd_te_compress 16 $spec
run $fullLogName-home-RCFMCD.log $file.tmp TULA mtd_te_compress 16 $spec
removetmp $file




file="data/crypto/train.csv"
spec="code/scripts/specs/crypto_full.json"
run $fullLogName-crypto-FM.log $file ULA mtd_te 16 $spec
removetmp $file
run $fullLogName-crypto-FMCD.log $file ULA mtd_te_compress 16 $spec
run $fullLogName-crypto-FCMD.log $file TULA mtd_te 16 $spec
removetmp $file
run $fullLogName-crypto-FCMCD.log $file TULA mtd_te_compress 16 $spec
removetmp $file
run $fullLogName-crypto-CFCMD.log $file TCLA mtd_te 16 $spec
run $fullLogName-crypto-CFCMCD.log $file TCLA mtd_te_compress 16 $spec
removetmp $file

run $fullLogName-crypto-uf.log $file ULA mtd_detect 16
run $fullLogName-crypto-RFCMCD.log $file.tmp TCLA mtd_te_compress 16 $spec
removetmp $file

run $fullLogName-crypto-cf.log $file ULA mtd_compress 16
run $fullLogName-crypto-RCFCMCD.log $file.tmp TCLA mtd_te_compress 16 $spec
run $fullLogName-crypto-RCFMCD.log $file.tmp TULA mtd_te_compress 16 $spec
removetmp $file




file="data/criteo/day_0_10000000.tsv"
spec="code/scripts/specs/criteo_full.json"
run $fullLogName-criteo-FM.log $file ULA mtd_te 16 $spec
removetmp $file
run $fullLogName-criteo-FMCD.log $file ULA mtd_te_compress 16 $spec
removetmp $file
run $fullLogName-criteo-FCMD.log $file TULA mtd_te 16 $spec
run $fullLogName-criteo-FCMCD.log $file TULA mtd_te_compress 16 $spec
removetmp $file
run $fullLogName-criteo-CFCMD.log $file TCLA mtd_te 16 $spec
run $fullLogName-criteo-CFCMCD.log $file TCLA mtd_te_compress 16 $spec
removetmp $file

run $fullLogName-criteo-uf.log $file ULA mtd_detect 16
run $fullLogName-criteo-RFCMCD.log $file.tmp TCLA mtd_te_compress 16 $spec
removetmp $file

run $fullLogName-criteo-cf.log $file ULA mtd_compress 16
run $fullLogName-criteo-RCFCMCD.log $file.tmp TCLA mtd_te_compress 16 $spec
run $fullLogName-criteo-RCFMCD.log $file.tmp TULA mtd_te_compress 16 $spec
removetmp $file














echo "DONE Datasets TE"
echo ""
echo "" 









# file="data/criteo/day_0_1000000.tsv"
# spec="code/scripts/specs/criteo_full.json"
# run $fullLogName-criteo-FM.log $file ULA mtd_te 16 $spec
# removetmp $file
# run $fullLogName-criteo-FMCD.log $file ULA mtd_te_compress 16 $spec
# removetmp $file
# run $fullLogName-criteo-FCMD.log $file TULA mtd_te 16 $spec
# run $fullLogName-criteo-FCMCD.log $file TULA mtd_te_compress 16 $spec
# run $fullLogName-criteo-FCMCD.log $file TULA mtd_te_compress 16 $spec
# removetmp $file
# run $fullLogName-criteo-CFCMD.log $file TCLA mtd_te 16 $spec
# run $fullLogName-criteo-CFCMCD.log $file TCLA mtd_te_compress 16 $spec
# removetmp $file

# run $fullLogName-criteo-uf.log $file ULA mtd_detect 16
# run $fullLogName-criteo-RFCMCD.log $file.tmp TCLA mtd_te_compress 16 $spec
# removetmp $file

# run $fullLogName-criteo-cf.log $file ULA mtd_compress 16
# run $fullLogName-criteo-RCFCMCD.log $file.tmp TCLA mtd_te_compress 16 $spec
# run $fullLogName-criteo-RCFMCD.log $file.tmp TULA mtd_te_compress 16 $spec
# removetmp $file
