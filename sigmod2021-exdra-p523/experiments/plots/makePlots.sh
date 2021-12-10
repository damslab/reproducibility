#/bin/bash

source parameters.sh

rm -fr plots/pdfs
mkdir -p plots/pdfs

addressb=(${address[@]})
numWorkers=${#addressb[@]}

SAlgs=("lm l2svm logreg")
Pipelines=("P2v2 P2_FFN")
SupervisedD="P2P"
Algs=("kmeans pca")
networks=("FNN")
CNN=("CNN")

## Generate the csv files containing the extracted results.

python plots/makeTables.py -a $Algs -n $numWorkers -d $SupervisedD -l $main -c "_def" &
python plots/makeTables.py -a $Algs -n $numWorkers -d $SupervisedD -l $local_machine_name -c "_def" &
python plots/makeTables.py -a $SAlgs -n $numWorkers -d $SupervisedD -l $main -c "_def" &
python plots/makeTables.py -a $SAlgs -n $numWorkers -d $SupervisedD -l $local_machine_name -c "_def" &
python plots/makeTables.py -a $Algs -n $numWorkers -d $SupervisedD -l $main -c "_mkl" &

python plots/makeTables.py -a $Algs -n $numWorkers -d $SupervisedD -l $local_machine_name -c "_mkl" &
python plots/makeTables.py -a $Algs -n $numWorkers -d $SupervisedD -l $local_machine_name -c "_sslmkl" &
python plots/makeTables.py -a $SAlgs -n $numWorkers -d $SupervisedD -l $main -c "_mkl" &
python plots/makeTables.py -a $SAlgs -n $numWorkers -d $SupervisedD -l $local_machine_name -c "_mkl" &
python plots/makeTables.py -a $SAlgs -n $numWorkers -d $SupervisedD -l $local_machine_name -c "_sslmkl" &

python plots/makeTables.py -a $networks -n $numWorkers -d $SupervisedD -l $main -c "_mkl" &
python plots/makeTables.py -a $networks -n $numWorkers -d $SupervisedD -l $local_machine_name -c "_mkl" &
python plots/makeTables.py -a $networks -n $numWorkers -d $SupervisedD -l $local_machine_name -c "_sslmkl" &
python plots/makeTables.py -a $CNN -n $numWorkers -d "mnist" -l $main -c "_mkl" &
python plots/makeTables.py -a $CNN -n $numWorkers -d "mnist" -l $local_machine_name -c "_mkl" &
python plots/makeTables.py -a $CNN -n $numWorkers -d "mnist" -l $local_machine_name -c "_sslmkl" &

python plots/makeTables.py -a $Pipelines -n $numWorkers -d "P2" -l $main -c "_mkl" &
python plots/makeTables.py -a $Pipelines -n $numWorkers -d "P2" -l $local_machine_name -c "_mkl" &
python plots/makeTables.py -a $Pipelines -n $numWorkers -d "P2" -l $local_machine_name -c "_sslmkl" &

python plots/makeTableNoFed.py -a $Algs -n $numWorkers -d $SupervisedD -l $main -c "_mkl" &
python plots/makeTableNoFed.py -a $SAlgs -n $numWorkers -d $SupervisedD -l $main -c "_mkl" &

wait 

# Actually plot the results

python plots/linePlots.py -a $Algs -s $SAlgs -n $networks -m $CNN -l $main -d "P2P" -c "_mkl" &
python plots/linePlotsSSL.py -l $main -d "P2P" -c "_mkl" -w $local_machine_name &
python plots/linePlotsPL.py -l $main -d "P2" -c "_mkl" &
python plots/barPlots.py -l $main &

wait
