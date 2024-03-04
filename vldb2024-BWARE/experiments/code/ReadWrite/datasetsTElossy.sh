#!/bin/bash

echo "Running Read and Write Real datasets experiments"

export LOG4JPROP='code/logging/log4j-compression.properties'

exrep=2
clear=1
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"
profileEnabled=1
mode="singlenode"


run() {

    if [ ! -f "$1" ] || [ $clear == 1 ]; then
        if [ -f "$1" ]; then
             mv $1 "$1$(date +"%m-%d-%y-%r").log"
        fi
        
        echo -n "--- Log : $1 "
        for i in $(seq $exrep); do

            rm -rf $2.tmp
            rm -rf $2.tmp.mtd
            rm -rf $2.tmp.dict

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

            rm -rf $2.tmp
            rm -rf $2.tmp.mtd
            rm -rf $2.tmp.dict

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


echo code/ReadWrite/datasetsTElossy.sh




mkdir -p "results/TE_lossy/$HOSTNAME/"

fullLogName="results/TE_lossy/$HOSTNAME/E"




# file="data/adult/adult.csv"
# spec_base="code/scripts/specs/adult"
# ls=("l1 l2 l3 l4 l5 l10 l20 l40")
# run $fullLogName-adult-FM-l0.log $file ULA mtd_te 16 ${spec_base}_full.json
# run $fullLogName-adult-FM-l0-S.log $file ULA mtd_te_nd 16 ${spec_base}_full.json
# run $fullLogName-adult-CFMCMCD-l0.log $file CLA mtd_te_compress 16 ${spec_base}_full.json
# run $fullLogName-adult-FULLCFMCMCD-l0.log $file CLAF mtd_te_compress 16 ${spec_base}_full.json
# run $fullLogName-adult-CFCMCD-l0.log $file TCLA mtd_te_compress 16 ${spec_base}_full.json

# for t in $ls; do
#     run $fullLogName-adult-FM-$t.log $file ULA mtd_te 16 ${spec_base}_$t.json
#     run $fullLogName-adult-CFMCMCD-$t.log $file CLA mtd_te_compress 16 ${spec_base}_$t.json
#     run $fullLogName-adult-CFCMCD-$t.log $file TCLA mtd_te_compress 16 ${spec_base}_$t.json
# done 



# file="data/cat/train.csv"
# spec_base="code/scripts/specs/catindat"
# ls=("l1 l2 l3 l5 l10 l20 l40 l80 l160 l320 l640")
# ls=("l320")
# run $fullLogName-cat-FM-l0.log $file ULA mtd_te 16 ${spec_base}_full.json
# run $fullLogName-cat-FM-l0-S.log $file ULA mtd_te_nd 16 ${spec_base}_full.json
# run $fullLogName-cat-CFMCMCD-l0.log $file CLA mtd_te_compress 16 ${spec_base}_full.json
# run $fullLogName-cat-FULLCFMCMCD-l0.log $file CLAF mtd_te_compress 16 ${spec_base}_full.json
# run $fullLogName-cat-CFCMCD-l0.log $file TCLA mtd_te_compress 16 ${spec_base}_full.json

# for t in $ls; do
#     run $fullLogName-cat-FM-$t.log $file ULA mtd_te 16 ${spec_base}_$t.json
#     run $fullLogName-cat-CFMCMCD-$t.log $file CLA mtd_te_compress 16 ${spec_base}_$t.json
#     run $fullLogName-cat-CFCMCD-$t.log $file TCLA mtd_te_compress 16 ${spec_base}_$t.json
# done 





# file="data/kdd98/cup98val.csv"
# spec_base="code/scripts/specs/kdd"
# ls=("l1 l2 l3 l5 l10 l20 l40 l80 l160 l320 l640 l1280 l2560")

# run $fullLogName-kdd-FM-l0.log $file ULA mtd_te 16 ${spec_base}_full.json
# run $fullLogName-kdd-FM-l0-S.log $file ULA mtd_te_nd 16 ${spec_base}_full.json
# run $fullLogName-kdd-CFMCMCD-l0.log $file CLA mtd_te_compress 16 ${spec_base}_full.json
# run $fullLogName-kdd-FULLCFMCMCD-l0.log $file CLAF mtd_te_compress 16 ${spec_base}_full.json
# run $fullLogName-kdd-CFCMCD-l0.log $file TCLA mtd_te_compress 16 ${spec_base}_full.json

# for t in $ls; do
#     run $fullLogName-kdd-FM-$t.log $file ULA mtd_te 16 ${spec_base}_$t.json
#     run $fullLogName-kdd-CFMCMCD-$t.log $file CLA mtd_te_compress 16 ${spec_base}_$t.json
#     run $fullLogName-kdd-CFCMCD-$t.log $file TCLA mtd_te_compress 16 ${spec_base}_$t.json
# done 





# file="data/salaries/train.csv"
# spec_base="code/scripts/specs/salaries"
# ls=("l0.6 l1 l2 l3 l5 l10 l20")
# # ls=("l20")

# run $fullLogName-salaries-FM-l0.log $file ULA mtd_te 16 ${spec_base}_full.json
# run $fullLogName-salaries-FM-l0-S.log $file ULA mtd_te_nd 16 ${spec_base}_full.json
# run $fullLogName-salaries-CFMCMCD-l0.log $file CLA mtd_te_compress 16 ${spec_base}_full.json
# run $fullLogName-salaries-FULLCFMCMCD-l0.log $file CLAF mtd_te_compress 16 ${spec_base}_full.json
# run $fullLogName-salaries-CFCMCD-l0.log $file TCLA mtd_te_compress 16 ${spec_base}_full.json

# for t in $ls; do
#     run $fullLogName-salaries-FM-$t.log $file ULA mtd_te 16 ${spec_base}_$t.json
#     run $fullLogName-salaries-CFMCMCD-$t.log $file CLA mtd_te_compress 16 ${spec_base}_$t.json
#     run $fullLogName-salaries-CFCMCD-$t.log $file TCLA mtd_te_compress 16 ${spec_base}_$t.json
# done 





# file="data/santander/train.csv"
# spec_base="code/scripts/specs/santander"
# ls=("l1 l2 l3 l5 l10 l20 l40 l80 l160 l320 l640 l1280 l2560")

# run $fullLogName-santander-FM-l0.log $file ULA mtd_te 16 ${spec_base}_full.json
# run $fullLogName-santander-FM-l0-S.log $file ULA mtd_te_nd 16 ${spec_base}_full.json
# run $fullLogName-santander-CFMCMCD-l0.log $file CLA mtd_te_compress 16 ${spec_base}_full.json
# run $fullLogName-santander-FULLCFMCMCD-l0.log $file CLAF mtd_te_compress 16 ${spec_base}_full.json
# run $fullLogName-santander-CFCMCD-l0.log $file TCLA mtd_te_compress 16 ${spec_base}_full.json

# for t in $ls; do
#     run $fullLogName-santander-FM-$t.log $file ULA mtd_te 16 ${spec_base}_$t.json
#     run $fullLogName-santander-CFMCMCD-$t.log $file CLA mtd_te_compress 16 ${spec_base}_$t.json
#     run $fullLogName-santander-CFCMCD-$t.log $file TCLA mtd_te_compress 16 ${spec_base}_$t.json
# done 





# file="data/home/train.csv"
# spec_base="code/scripts/specs/home"
# ls=("l1 l2 l3 l5 l10 l20 l40 l80 l160 l320 l640 l1280 l2560 l5120")
# # ls=("l160")
# run $fullLogName-home-FM-l0.log $file ULA mtd_te 16 ${spec_base}_full.json
# run $fullLogName-home-FM-l0-S.log $file ULA mtd_te_nd 16 ${spec_base}_full.json
# run $fullLogName-home-CFMCMCD-l0.log $file CLA mtd_te_compress 16 ${spec_base}_full.json
# run $fullLogName-home-FULLCFMCMCD-l0.log $file CLAF mtd_te_compress 16 ${spec_base}_full.json
# run $fullLogName-home-CFCMCD-l0.log $file TCLA mtd_te_compress 16 ${spec_base}_full.json

# for t in $ls; do
#     run $fullLogName-home-FM-$t.log $file ULA mtd_te 16 ${spec_base}_$t.json
#     run $fullLogName-home-CFMCMCD-$t.log $file CLA mtd_te_compress 16 ${spec_base}_$t.json
#     run $fullLogName-home-CFCMCD-$t.log $file TCLA mtd_te_compress 16 ${spec_base}_$t.json
# done 





file="data/crypto/train.csv"
spec_base="code/scripts/specs/crypto"
ls=("l1 l2 l3 l5 l10 l20 l40 l80 l160 l320 l640 l1280 l2560")

# run $fullLogName-crypto-FM-l0.log $file ULA mtd_te 16 ${spec_base}_full.json
# run $fullLogName-crypto-FM-l0-S.log $file ULA mtd_te_nd 16 ${spec_base}_full.json
run $fullLogName-crypto-CFMCMCD-l0.log $file CLA mtd_te_compress 16 ${spec_base}_full.json
run $fullLogName-crypto-FULLCFMCMCD-l0.log $file CLAF mtd_te_compress 16 ${spec_base}_full.json
run $fullLogName-crypto-CFCMCD-l0.log $file TCLA mtd_te_compress 16 ${spec_base}_full.json

for t in $ls; do
    run $fullLogName-crypto-FM-$t.log $file ULA mtd_te 16 ${spec_base}_$t.json
    run $fullLogName-crypto-CFMCMCD-$t.log $file CLA mtd_te_compress 16 ${spec_base}_$t.json
    run $fullLogName-crypto-CFCMCD-$t.log $file TCLA mtd_te_compress 16 ${spec_base}_$t.json
done 

file="data/criteo/day_0_10000000.tsv"
spec_base="code/scripts/specs/criteo"
ls=("l1 l2 l3 l5 l10 l20 l40 l80 l160 l320 l640 l1280 l2560 l5120")
# ls=("l20 l40 l80 l160 l320 l640 l1280 l2560 l5120")

# run $fullLogName-criteo-FM-l0.log $file ULA mtd_te 16 ${spec_base}_full.json
# run $fullLogName-criteo-FM-l0-S.log $file ULA mtd_te_nd 16 ${spec_base}_full.json
run $fullLogName-criteo-CFMCMCD-l0.log $file CLA mtd_te_compress 16 ${spec_base}_full.json
run $fullLogName-criteo-FULLCFMCMCD-l0.log $file CLAF mtd_te_compress 16 ${spec_base}_full.json
run $fullLogName-criteo-CFCMCD-l0.log $file TCLA mtd_te_compress 16 ${spec_base}_full.json

for t in $ls; do
    run $fullLogName-criteo-FM-$t.log $file ULA mtd_te 16 ${spec_base}_$t.json
    run $fullLogName-criteo-CFMCMCD-$t.log $file CLA mtd_te_compress 16 ${spec_base}_$t.json
    run $fullLogName-criteo-CFCMCD-$t.log $file TCLA mtd_te_compress 16 ${spec_base}_$t.json
done 
















