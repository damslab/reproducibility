#/bin/bash

source parameters.sh

rm -fr plots/pdfs
mkdir -p plots/pdfs

addressb=(${address[@]})

SAlgs=("lm l2svm logreg")
Pipelines=("P2v2 P2_FFN")
SupervisedD="P2P"
Algs=("kmeans pca")
networks=("TwoNN")
CNN=("CNN")


python plots/makeTables.py -a $Algs -n ${#addressb[@]} -d $SupervisedD -l "charlie" -c "_def" &
python plots/makeTables.py -a $Algs -n ${#addressb[@]} -d $SupervisedD -l "XPS-15-7590" -c "_def" &
python plots/makeTables.py -a $SAlgs -n ${#addressb[@]} -d $SupervisedD -l "charlie" -c "_def" &
python plots/makeTables.py -a $SAlgs -n ${#addressb[@]} -d $SupervisedD -l "XPS-15-7590" -c "_def" &
python plots/makeTables.py -a $Algs -n ${#addressb[@]} -d $SupervisedD -l "charlie" -c "_mkl" &

python plots/makeTables.py -a $Algs -n ${#addressb[@]} -d $SupervisedD -l "XPS-15-7590" -c "_mkl" &
python plots/makeTables.py -a $Algs -n ${#addressb[@]} -d $SupervisedD -l "XPS-15-7590" -c "_sslmkl" &
python plots/makeTables.py -a $SAlgs -n ${#addressb[@]} -d $SupervisedD -l "charlie" -c "_mkl" &
python plots/makeTables.py -a $SAlgs -n ${#addressb[@]} -d $SupervisedD -l "XPS-15-7590" -c "_mkl" &
python plots/makeTables.py -a $SAlgs -n ${#addressb[@]} -d $SupervisedD -l "XPS-15-7590" -c "_sslmkl" &

python plots/makeTables.py -a $networks -n ${#addressb[@]} -d $SupervisedD -l "charlie" -c "_mkl" &
python plots/makeTables.py -a $networks -n ${#addressb[@]} -d $SupervisedD -l "XPS-15-7590" -c "_mkl" &
python plots/makeTables.py -a $networks -n ${#addressb[@]} -d $SupervisedD -l "XPS-15-7590" -c "_sslmkl" &
python plots/makeTables.py -a $CNN -n ${#addressb[@]} -d "mnist" -l "charlie" -c "_mkl" &
python plots/makeTables.py -a $CNN -n ${#addressb[@]} -d "mnist" -l "XPS-15-7590" -c "_mkl" &
python plots/makeTables.py -a $CNN -n ${#addressb[@]} -d "mnist" -l "XPS-15-7590" -c "_sslmkl" &

python plots/makeTables.py -a $Pipelines -n ${#addressb[@]} -d "P2" -l "charlie" -c "_mkl" &
python plots/makeTables.py -a $Pipelines -n ${#addressb[@]} -d "P2" -l "XPS-15-7590" -c "_mkl" &
python plots/makeTables.py -a $Pipelines -n ${#addressb[@]} -d "P2" -l "XPS-15-7590" -c "_sslmkl" &


python plots/makeTableNoFed.py -a $Algs -n ${#addressb[@]} -d $SupervisedD -l "charlie" -c "_mkl" &
python plots/makeTableNoFed.py -a $SAlgs -n ${#addressb[@]} -d $SupervisedD -l "charlie" -c "_mkl" &

wait 

python plots/linePlots.py -a $Algs -s $SAlgs -n $networks -m $CNN -l "charlie" -d "P2P" -c "_mkl" &

python plots/linePlotsSSL.py -l "charlie" -d "P2P" -c "_mkl" &
python plots/linePlotsPL.py -l "charlie" -d "P2" -c "_mkl" &
python plots/barPlots.py &

wait
