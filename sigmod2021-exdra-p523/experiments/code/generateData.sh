#!/bin/bash

source parameters.sh

# Activate the python environment.
source "$VENV_PATH/bin/activate"

mkdir -p results
mkdir -p data
mkdir -p tmp

if [[ "1" -eq "$portForward" ]]; then
    if [[ "$HOSTNAME" -eq $local_machine_name ]]; then
        address=("localhost localhost localhost localhost localhost localhost localhost")
    fi
fi

nr_data=$(ls data | wc -l)

addressb=(${address[@]})

## Generate json files that map to federated locations this have to be done on the local machine and main machine.
for index in ${!addressb[*]}; do
    numWorkers=$((index + 1))
    python code/dataGen/federatedMetaDataGenerator.py \
        -a $address -p $ports -n $numWorkers -d "mnist_features_" \
        -f 784 -e 60000 &
    python code/dataGen/federatedMetaDataGenerator.py \
        -a $address -p $ports -n $numWorkers -d "mnist_labels_" \
        -f 10 -e 60000 &
    python code/dataGen/federatedMetaDataGenerator.py \
        -a $address -p $ports -n $numWorkers -d "P2_features_" \
        -f 1001 -e 1000000 &
    python code/dataGen/federatedMetaDataGenerator.py \
        -a $address -p $ports -n $numWorkers -d "P2P_features_" \
        -f 1050 -e 1000000 &
    python code/dataGen/federatedMetaDataGenerator.py \
        -a $address -p $ports -n $numWorkers -d "P2_labels_" \
        -f 1 -e 1000000 &
    python code/dataGen/federatedMetaDataGenerator.py \
        -a $address -p $ports -n $numWorkers -d "P2P_labels_" \
        -f 1 -e 1000000 &
done

wait 

# Create main dataset locally and on main machine since test data part is used for WAN
python code/dataGen/generate_mnist.py 
systemds code/dataGen/P2datagen.dml -config code/conf/def.xml 

if [[ $HOSTNAME == "$main" ]]; then
    ## only create the data paritions on the main machine.

    ## Make slices of the data
    datasets=("mnist_features mnist_labels P2_features P2_labels P2P_features P2P_labels")
    for name in $datasets; do
        for index in ${!addressb[*]}; do
            numWorkers=$((index + 2))
            if [[ $numWorkers -lt $((${#addressb[@]} + 1)) ]]; then
                echo "Generating data/${name}_${numWorkers}_1.data"
                systemds code/dataGen/slice.dml \
                    -config code/conf/def.xml \
                    -args $name $numWorkers &
            fi
        done

        wait
    done


    # Remove old data folders. and put in the new data.
    for index in ${!addressb[*]}; do
        ssh -T ${addressb[$index]} " cd $remoteDir; rm -r data; mkdir data" &
    done

    wait
    ## Distribute the individual workers data.
    for index in ${!addressb[*]}; do
        fileId=$((index + 1))
        for worker in ${!addressb[*]}; do
            numWorkers=$((worker + 1))
            ## Get results:
            if (($fileId <= $numWorkers)); then
                if [ "${addressb[$index]}" != "localhost" ]; then
                    sleep 0.1
                    rsync -ah -e ssh --include="*_${numWorkers}_${fileId}.dat*" --exclude='*' "data/" ${addressb[$index]}:$remoteDir/data/ &
                    sleep 0.1
                    rsync -ah -e ssh --include="*_${numWorkers}_${fileId}.data***" --exclude='*' "data/" ${addressb[$index]}:$remoteDir/data/ &
                fi
            fi
        done
        rsync -ah -e ssh --include="*_features.dat***" --exclude='*' "data/" ${addressb[0]}:$remoteDir/data/ &
        rsync -ah -e ssh --include="*_labels.dat*" --exclude='*' "data/" ${addressb[0]}:$remoteDir/data/ &
    done
    
    # Create python readable versions of the data
    # (don't wait for this because it is super slow, so instead we just let it run in the background)
    python code/dataGen/createData.py -p "P2P_features" &
    python code/dataGen/createData.py -p "P2P_labels" &

    wait

    echo -e "--------------\nDONE ON MAIN\n--------------"
else 
    echo -e "--------------\nDONE ON LOCAL\n--------------"
fi

# deactivate the python vertual environement
deactivate
