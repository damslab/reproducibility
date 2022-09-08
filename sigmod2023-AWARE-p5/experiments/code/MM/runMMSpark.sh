#/bin/bash

source parameters.sh

export SYSDS_DISTRIBUTED=1

logstart="results/MM"

for d in $data; do
    if [[ "$d" =~ "infimnist" ]]; then
        folder="infimnist"
    elif [[ "$d" =~ "binarymnist" ]]; then
        folder="binarymnist"
    elif [[ "$d" =~ "census" ]]; then
        folder="census"
    else
        folder=$d
    fi
    for x in $mm; do
        for s in $mVSizes; do
            for y in $techniques; do

                mkdir -p "$logstart/$x-$s/$d/$HOSTNAME/"
                fullLogname="$logstart/$x-$s/$d/$HOSTNAME/$y-$mode.log"
                if [ ! -f "$fullLogname" ] || [ $clear == 1 ]; then
                    rm -f $fullLogname
                    perf stat -d -d -d -r $exrep \
                        systemds \
                        code/MM/$x.dml \
                        -config code/conf/$y.xml \
                        -stats 100 \
                        -debug \
                        -exec "$mode" \
                        -args "data/$folder/train_$d.data" $inrep $s \
                        "data/$folder/train_$d_labels.data" \
                        >>$fullLogname 2>&1

                    echo "------------------------------------"
                    rm -f $fullLogname.res
                    echo "$HOSTNAME - $d-$x-$s-$y"
                    cat $fullLogname | grep -E '1  r| ba| compress |Total elapsed time| instructions |  cycles  | CPUs utilized | tsmm | \*   ' | tee -a $fullLogname.res
                    echo "$HOSTNAME - $d-$x-$s-$y"
                    echo "------------------------------------"
                fi
            done
        done
    done
done
