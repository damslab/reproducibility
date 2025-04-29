#!/bin/bash

echo "Running Transform experiments"

export LOG4JPROP='code/logging/log4j-compression.properties'

exrep=1
clear=1
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"
profileEnabled=1
mode="singlenode"

techniques=("ULA CLA TCLA")
# techniques=("ULA CLA")
# techniques=("ULA")
# techniques=("CLA")
techniques=("TCLA")
format=("binary compressed")
format=("compressed")
format=("binary")
# blockSizes=("1")
blockSizes=("16")
# blockSizes=("32")
# blockSizes=("64")
# blockSizes=("128")
# blockSizes=("256")
# blockSizes=("500")

criteoSizes=("1000 10000 100000 1000000")
criteoSizes=("1000 10000 100000")
# criteoSizes=("1000 10000")
criteoSizes=("1000")
# criteoSizes=("10000")
# criteoSizes=("100000")
# criteoSizes=("1000000")

transform() {
    # 1 : log file
    # 2 : confType
    # 3 : block size
    # 4 : Frame file (with mtd)
    # 5 : Transform spec file
    # 6 : ScriptFile
    if [ ! -f "$1" ] || [ $clear == 1 ]; then
        rm -f $1

        for i in $(seq $exrep); do
            if [ $profileEnabled == 1 ]; then
                mkdir -p "$1-perf"
                profile="$1-perf/$i.profile.html"
                export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/build/libasyncProfiler.so=start,event=cpu,file=$profile"
            fi
            perf stat -d -d -d \
                systemds \
                code/Transform/$6.dml \
                -config code/conf/${2}b${3}.xml \
                -stats 100 \
                -exec "$mode" \
                -debug \
                -seed $seed \
                -args $4 $5 $7 $8 $9 \
                >>$1 2>&1
            # Disk size add.
            du $4 >>$1
            du $7 >>$1
            du $8 >>$1
            export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"
        done
        echo "--- Write : $1"

    fi
}

writeFormat() {
    if [ ! -f "$1" ] || [ $clear == 1 ]; then
        rm -f $1

        if [ $profileEnabled == 1 ]; then
            mkdir -p "$1-perf"
            profile="$1-perf/$i.profile.html"
            export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/build/libasyncProfiler.so=start,event=cpu,file=$profile"
        fi
        perf stat -d -d -d \
            systemds \
            code/ReadWrite/dataset/$6.dml \
            -config code/conf/${4}b${5}.xml \
            -stats 100 \
            -exec "$mode" \
            -debug \
            -seed $seed \
            -args $2 $3 $7 \
            >>$1 2>&1
        # -explain "recompile_hops" \
        # Disk size add.
        du $2 >>$1
        du $3 >>$1
        export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"

        echo "--- Write : $1"
    fi
}

for t in $techniques; do
    specs=("criteo_spec1 criteo_spec2")
    specs=("criteo_fe1 criteo_fe2 criteo_fe3 criteo_fe4 criteo_fe5 criteo_fe6")
    specs=("criteo_fe1 ")
    # specs=("criteo_fe3 ")
    # specs=("criteo_spec1")
    # specs=("criteo_spec2")
    # for s in $criteoSizes; do
    #     fullFileName="data/criteo/day_0_$s.tsv"
    #     # fullLogName="results/ReadRealFrame/$HOSTNAME/$t/B1-$mode-day_0_$s-tsv-Read.log"
    #     # readfile $fullLogName $fullFileName $t "tsv" 1

    #     for f in $format; do
    #         mkdir -p "results/Transform/$HOSTNAME/$t-$f/"
    #         mkdir -p "tmp/Transform/$HOSTNAME/$t-$f/"
    #         for b in $blockSizes; do
    #             fullLogName="results/Transform/$HOSTNAME/$t-$f/B$b-$mode-day_0_$s-tsv.log"
    #             tmpFileName="tmp/Transform/$HOSTNAME/$t-$f/B$b-$mode-day_0_$s.in"
    #             writeFormat $fullLogName $fullFileName $tmpFileName $t $b "tsv_write" $f
    #             for z in $specs; do
    #                 fullLogName="results/Transform/$HOSTNAME/$t-$f/B$b-$mode-day_0_$s-$z.log"
    #                 tmpData="tmp/Transform/$HOSTNAME/$t-$f/B$b-$mode-day_0_$s-$z.data"
    #                 tmpMeta="tmp/Transform/$HOSTNAME/$t-$f/B$b-$mode-day_0_$s-$z.meta"
    #                 sp="code/Transform/specs/$z.json"
    #                 transform $fullLogName $t $b $tmpFileName $sp "transform" $tmpData $tmpMeta $f
    #             done
    #         done
    #     done
    # done
    
    fullFileName="data/kdd98/cup98val.csv"
    # fullLogName="results/Transform/$HOSTNAME/$t/B1-$mode-kdd-cup98-Read.log"
    # readfile $fullLogName $fullFileName $t "csv" 1
    specs=("kdd_spec1")
    for f in $format; do
        mkdir -p "results/Transform/$HOSTNAME/$t-$f/"
        mkdir -p "tmp/Transform/$HOSTNAME/$t-$f/"
        for b in $blockSizes; do
            fullLogName="results/Transform/$HOSTNAME/$t-$f/B$b-$mode-cup98val-tsv-Write.log"
            tmpFileName="tmp/Transform/$HOSTNAME/$t-$f/B$b-$mode-cup98val.in"
            writeFormat $fullLogName $fullFileName $tmpFileName $t $b "csv_write" $f
            for s in $specs; do
                fullLogName="results/Transform/$HOSTNAME/$t-$f/B$b-$mode-cup98val-$s.log"
                tmpData="tmp/Transform/$HOSTNAME/$t-$f/B$b-$mode-cup98val-$s.data"
                tmpMeta="tmp/Transform/$HOSTNAME/$t-$f/B$b-$mode-cup98val-$s.meta"
                sp="code/Transform/specs/$s.json"
                transform $fullLogName $t $b $tmpFileName $sp "transform" $tmpData $tmpMeta $f
            done
        done
    done

    # fullFileName="data/adult/adult.csv"
    # # fullLogName="results/Transform/$HOSTNAME/$t/B1-$mode-adult-Read.log"
    # # readfile $fullLogName $fullFileName $t "csv_nohead" 1
    # specs=("adult_spec2")

    # for f in $format; do
    #     mkdir -p "results/Transform/$HOSTNAME/$t-$f/"
    #     mkdir -p "tmp/Transform/$HOSTNAME/$t-$f/"
    #     for b in $blockSizes; do
    #         fullLogName="results/Transform/$HOSTNAME/$t-$f/B$b-$mode-adult-csv.log"
    #         tmpFileName="tmp/Transform/$HOSTNAME/$t-$f/B$b-$mode-adult.in"
    #         writeFormat $fullLogName $fullFileName $tmpFileName $t $b "csv_nohead_write" $f
    #         for s in $specs; do
    #             fullLogName="results/Transform/$HOSTNAME/$t-$f/B$b-$mode-adult-$s.log"
    #             tmpData="tmp/Transform/$HOSTNAME/$t-$f/B$b-$mode-adult-$s.data"
    #             tmpMeta="tmp/Transform/$HOSTNAME/$t-$f/B$b-$mode-adult-$s.meta"
    #             sp="code/Transform/specs/$s.json"
    #             transform $fullLogName $t $b $tmpFileName $sp "transform" $tmpData $tmpMeta $f
    #         done
    #     done
    # done
done
