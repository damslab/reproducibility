#!/bin/bash

echo "Running compression of UCR Time series data"

export LOG4JPROP='code/logging/log4j-compression.properties'

exrep=1
# exrep=1
clear=1
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"
profileEnabled=1
mode="singlenode"


if [ "$HOSTNAME" = "XPS-15-7590" ]; then
    export SYSTEMDS_STANDALONE_OPTS="-Xmx2g -Xms2g -Xmn200m"
elif [ "$HOSTNAME" = "dams-su1" ]; then
    export SYSTEMDS_STANDALONE_OPTS="-Xmx10g -Xms10g -Xmn1g"
else
    echo "unknown machine please add"
    exit -1
fi



techniques=("ULA")

format=("compressed binary")
# format=("compressed")
blockSizes=("0.5 1 2 4 8 16 32")
blockSizes=("0.5 1 8 16")
blockSizes=("1")

lossySetting=("replace q10 q9 q8 q7 q6 q5 q4 q3 q2 q1")
lossySetting=("replace q10 q9 q8 q7 q6 q5 q4 q3 q2 q1")
lossySetting=("qi10 qi9 qi8 qi7 qi6 qi5 qi4 qi3 qi2 qi1 qt10 qt9 qt8 qt7 qt6 qt5 qt4 qt3 qt2 qt1 qti10 qti9 qti8 qti7 qti6 qti5 qti4 qti3 qti2 qti1")
# lossySetting=("original replace q8")
# lossySetting=("q10 q9 q8 q7 q6 q5 q4 q3 q2 q1")
# lossySetting=("qi10 qi9 qi8 qi7 qi6 qi5 qi4 qi3 qi2 qi1")
# lossySetting=("qt10 qt9 qt8 qt7 qt6 qt5 qt4 qt3 qt2 qt1")
# lossySetting=("qti10 qti9 qti8 qti7 qti6 qti5 qti4 qti3 qti2 qti1")
# lossySetting=("replace q10 qi10 qt10 qt5 qti5")
# lossySetting=("q8")
lossySetting=("q5")
# lossySetting=("q1")

readfile() {
    if [ ! -f "$1" ] || [ $clear == 1 ]; then
        rm -f $1

        for i in $(seq $exrep); do
            if [ $profileEnabled == 1 ]; then
                mkdir -p "$1-perf"
                profile="$1-perf/$i.profile.html"
                export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/build/libasyncProfiler.so=start,event=cpu,file=$profile"
            fi
            perf stat -d -d -d \
                timeout 1000 \
                systemds \
                code/ReadWrite/read.dml \
                -config code/conf/${3}b$5.xml \
                -stats 100 \
                -exec "$mode" \
                -debug \
                -seed $seed \
                -args $2 \
                >>$1 2>&1
            export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"
        done

        echo "--- Read  : $1"

    fi
}

writeFormat() {
    if [ ! -f "$1" ] || [ $clear == 1 ]; then
        rm -f $1

        for i in $(seq $exrep); do
            if [ $profileEnabled == 1 ]; then
                mkdir -p "$1-perf"
                profile="$1-perf/$i.profile.html"
                export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/build/libasyncProfiler.so=start,event=cpu,file=$profile"
            fi
            perf stat -d -d -d \
                timeout 1000 \
                systemds \
                code/ReadWrite/lossy/$6.dml \
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
        done
        echo "--- Write : $1"
    fi
}


runExperiment(){
    t=$1
    f=$2
    name=$3
    b=$4
    mode=$5
    lossy=$6
    fullLogName="results/Write-UCR/$HOSTNAME/$t-$f-$name/B$b-$mode-$lossy.log"
    tmpFileName="tmp/Write-UCR/$HOSTNAME/$t-$f-$name/B$b-$mode-$name-$lossy.cla"
    writeFormat $fullLogName $fullFileName $tmpFileName $t $b $lossy $f
    fullLogName="results/Read-UCR/$HOSTNAME/$t-$f-$name/B$b-$mode-$name-$lossy.log"
    readfile $fullLogName $tmpFileName $t $f $s
}

for t in $techniques; do
    for f in $format; do
        for d in data/UCRTime/UCRArchive_2018/*; do
   
            name=${d#*2018/}

            mkdir -p "results/Read-UCR/$HOSTNAME/$t-$f-$name/"
            mkdir -p "results/Write-UCR/$HOSTNAME/$t-$f-$name/"
            mkdir -p "tmp/Write-UCR/$HOSTNAME/$t-$f-$name/"

            fullFileName="$d/${name}_T.data"

            for b in $blockSizes; do
                runExperiment $t $f $name $b $mode "original" &
                if [ $f == "compressed" ]; then    
                    for lossy in $lossySetting; do
                        runExperiment $t $f $name $b $mode $lossy &
                    done
                fi
                wait
            done 
            exit
        done
    done
done
