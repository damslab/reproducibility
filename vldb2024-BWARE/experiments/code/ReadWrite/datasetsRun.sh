#!/bin/bash

echo "Running Read and Write Real datasets experiments"

export LOG4JPROP='code/logging/log4j-compression.properties'

exrep=4
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
                systemds \
                code/ReadWrite/dataset/$4.dml \
                -config code/conf/${3}b$5.xml \
                -stats 100 \
                -exec "$mode" \
                -debug \
                -seed $seed \
                -args $2 \
                >>$1 2>&1

            if [ -f "$2.tmp" ] || [ -d "$2.tmp" ]; then
                du $2.tmp >>$1
                du $2.tmp.mtd >>$1
            fi
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

cleanup() {
    rm -fr $1.tmp
    rm -fr $1.tmp.mtd
    rm -fr $1.tmp.tmp
    rm -fr $1.tmp.tmp.mtd
}

echo code/ReadWrite/datasetsRun.sh

mkdir -p "results/ReadRealFrame/$HOSTNAME/"
fullLogName="results/ReadRealFrame/$HOSTNAME/FM-"

cleanup $file

file="data/criteo/day_0_10000000.tsv"
# run $fullLogName-criteo-uf.log $file ULA mtd_detect 1
run $fullLogName-criteo-cf.log $file ULA mtd_compress 1
# run $fullLogName-criteo-rc.log $file.tmp ULA mtd 1
# run $fullLogName-criteo-uf-SNAPPY.log $file SNAPPY mtd_detect 1
run $fullLogName-criteo-cf-SNAPPY.log $file SNAPPY mtd_compress 1
# run $fullLogName-criteo-uf-ZStd.log $file Zstd mtd_detect 1
run $fullLogName-criteo-cf-ZStd.log $file Zstd mtd_compress 1
cleanup $file

file="data/cat/train.csv"
# run $fullLogName-cat-uf.log $file ULA mtd_detect 1
run $fullLogName-cat-cf.log $file ULA mtd_compress 1
# run $fullLogName-cat-rc.log $file.tmp ULA mtd 1
# run $fullLogName-cat-uf-SNAPPY.log $file SNAPPY mtd_detect 1
run $fullLogName-cat-cf-SNAPPY.log $file SNAPPY mtd_compress 1
# run $fullLogName-cat-uf-ZStd.log $file Zstd mtd_detect 1
run $fullLogName-cat-cf-ZStd.log $file Zstd mtd_compress 1
cleanup $file

file="data/adult/adult.csv"
# run $fullLogName-adult-uf.log $file ULA mtd_detect 1
run $fullLogName-adult-cf.log $file ULA mtd_compress 1
# run $fullLogName-adult-rc.log $file.tmp ULA mtd 1
# run $fullLogName-adult-uf-SNAPPY.log $file SNAPPY mtd_detect 1
run $fullLogName-adult-cf-SNAPPY.log $file SNAPPY mtd_compress 1
# run $fullLogName-adult-uf-ZStd.log $file Zstd mtd_detect 1
run $fullLogName-adult-cf-ZStd.log $file Zstd mtd_compress 1
cleanup $file

file="data/crypto/train.csv"
# run $fullLogName-crypto-uf.log $file ULA mtd_detect 1
run $fullLogName-crypto-cf.log $file ULA mtd_compress 1
# run $fullLogName-crypto-rc.log $file.tmp ULA mtd 1
# run $fullLogName-crypto-uf-SNAPPY.log $file SNAPPY mtd_detect 1
run $fullLogName-crypto-cf-SNAPPY.log $file SNAPPY mtd_compress 1
# run $fullLogName-crypto-uf-ZStd.log $file Zstd mtd_detect 1
run $fullLogName-crypto-cf-ZStd.log $file Zstd mtd_compress 1
cleanup $file

file="data/kdd98/cup98val.csv"
# run $fullLogName-kdd-uf.log $file ULA mtd_detect 1
run $fullLogName-kdd-cf.log $file ULA mtd_compress 1
# run $fullLogName-kdd-rc.log $file.tmp ULA mtd 1
# run $fullLogName-kdd-uf-SNAPPY.log $file SNAPPY mtd_detect 1
run $fullLogName-kdd-cf-SNAPPY.log $file SNAPPY mtd_compress 1
# run $fullLogName-kdd-uf-ZStd.log $file Zstd mtd_detect 1
run $fullLogName-kdd-cf-ZStd.log $file Zstd mtd_compress 1
cleanup $file

file="data/salaries/train.csv"
# run $fullLogName-salaries-uf.log $file ULA mtd_detect 1
run $fullLogName-salaries-cf.log $file ULA mtd_compress 1
# run $fullLogName-salaries-rc.log $file.tmp ULA mtd 1
# run $fullLogName-salaries-uf-SNAPPY.log $file SNAPPY mtd_detect 1
run $fullLogName-salaries-cf-SNAPPY.log $file SNAPPY mtd_compress 1
# run $fullLogName-salaries-uf-ZStd.log $file Zstd mtd_detect 1
run $fullLogName-salaries-cf-ZStd.log $file Zstd mtd_compress 1
cleanup $file

file="data/santander/train.csv"
# run $fullLogName-santander-uf.log $file ULA mtd_detect 1
run $fullLogName-santander-cf.log $file ULA mtd_compress 1
# run $fullLogName-santander-rc.log $file.tmp ULA mtd 1
# run $fullLogName-santander-uf-SNAPPY.log $file SNAPPY mtd_detect 1
run $fullLogName-santander-cf-SNAPPY.log $file SNAPPY mtd_compress 1
# run $fullLogName-santander-uf-ZStd.log $file Zstd mtd_detect 1
run $fullLogName-santander-cf-ZStd.log $file Zstd mtd_compress 1
cleanup $file

file="data/home/train.csv"
# run $fullLogName-home-uf.log $file ULA mtd_detect 1
run $fullLogName-home-cf.log $file ULA mtd_compress 1
# run $fullLogName-home-rc.log $file.tmp ULA mtd 1
# run $fullLogName-home-uf-SNAPPY.log $file SNAPPY mtd_detect 1
run $fullLogName-home-cf-SNAPPY.log $file SNAPPY mtd_compress 1
# run $fullLogName-home-uf-ZStd.log $file Zstd mtd_detect 1
run $fullLogName-home-cf-ZStd.log $file Zstd mtd_compress 1
cleanup $file
