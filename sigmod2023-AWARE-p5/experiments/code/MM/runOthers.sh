#/bin/bash

#Setup
mkdir -p results/MatrixVector/others

logstart="results/MatrixVector/others/"
for x in mv vm; do
    for y in tf np pandas; do
        echo "$x-$y"
        fullLogname=$logstart$y-$x-covtype-output.log
        rm -f $fullLogname
        for i in {1..1}; do
            python \
                code/MatrixVector/$y/$x.py \
                --rep 1000 \
                --data "data/covtype/removecol1.csv" \
                2>&1 | tee -a $fullLogname
        done
    done
done
