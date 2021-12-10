#/bin/bash -u

# start python vertual environment
source parameters.sh

if [[ ! -d "$VENV_PATH" ]]; then
    echo "Creating Python Virtual Enviroment"
    python3 -m venv $VENV_PATH
    echo "$HOSTNAME"
fi

source "$VENV_PATH/bin/activate"

pip install -q -r requirements.txt

mkdir -p results
mkdir -p data
mkdir -p tmp

if [[ "$HOSTNAME" -eq "XPS-15-7590" ]]; then
    address=("localhost localhost localhost localhost localhost localhost localhost")
fi

nr_data=$(ls data | wc -l)

addressb=(${address[@]})

# for N in $Ns; do
#     for M in $Ms; do
#         for sp in $Sps; do
#             name="data/Gen5of5_${N}_${M}_${sp}"
#             if [[ -f "$name" ]]; then
#                 printf "%25s %-30s %25s\n" "$HOSTNAME" ": SystemDS Data created already" "${N}_${M}_${sp}"
#             else
#                 if [[ -d "$name" ]]; then
#                     printf "%25s %-30s %25s\n" "$HOSTNAME" ": SystemDS Data created already" "${N}_${M}_${sp}"
#                 else
#                     systemds code/dataGen/createData.dml -args $N $M $sp
#                     echo "SystemDS data created  ${N}_${M}_${sp}"
#                 fi
#             fi
#             name="data/Gen_${N}_${M}_${sp}.data.npy"
#             if [[ -f "$name" ]]; then
#                 printf "%25s %-30s %25s\n" "$HOSTNAME" ": Numpy data created already" "${N}_${M}_${sp}"
#             else
#                 python code/dataGen/createData.py -n $N -m $M -s $sp &
#                 echo "Python data created  ${N}_${M}_${sp}"
#             fi
#         done
#     done
# done

# Siemens first dataset.
# if [[ -f "datasets/anonymized_data.csv" ]]; then
#     #Unzip
#     if [[ ! -f "datasets/anonymized_data.csv" ]]; then
#         unzip datasets/anonymized_data.zip -d ./datasets/
#     fi

#     # Sample
#     if [[ ! -f "data/anonymized_data_modified_$smSize.csv" ]]; then
#         python code/dataPrep/make_csv_siemens.py \
#             -i "datasets/anonymized_data.csv" \
#             -o "data/anonymized_data_modified" \
#             -s $smSize
#     fi

#     # Make systemds files
#     if [ ! -f "data/siemens_$smSize.data.mtd" ]; then
#         systemds code/dataPrep/saveTrainSiemens.dml \
#             -config code/conf/def.xml \
#             -args "data/anonymized_data_modified_$smSize.csv" \
#             "data/siemens_$smSize.data"
#         echo "Data creation finished $HOSTNAME"
#     fi

#     # Create federated partitions
#     name="siemens_$smSize"
#     for index in ${!addressb[*]}; do
#         numWorkers=$((index + 1))
#         if [[ ! -f "data/${name}_${numWorkers}_1.data.mtd" ]]; then
#             systemds code/dataGen/slice.dml \
#                 -config code/conf/def.xml \
#                 -args $name $numWorkers &
#         fi
#         if [[ ! -f "data/fed_${name}_$numWorkers.json" ]]; then
#             python code/dataGen/federatedMetaDataGenerator.py \
#                 -a $address -p $ports -n $numWorkers -d "${name}_" \
#                 -f 68 -e $smSize &
#         fi
#     done

#     wait

# else
#     echo "Missing Siemens Data"
# fi

# if [[ -f "datasets/exdra_use_case_2_anonymized.zip" ]]; then
#     # Siemens secound dataset.
#     if [[ ! -f "data/exdra_use_case_2_anonymized_features.csv" ]]; then
#         unzip datasets/exdra_use_case_2_anonymized.zip -d ./data/
#     fi

#     dataOrg2=(exdra_use_case_2_anonymized_features exdra_use_case_2_anonymized_target_0 exdra_use_case_2_anonymized_target_1)

#     data2=(uc2_features uc2_labels_1 uc2_labels_2)
#     data2cols=(80 1 1)

#     for index in ${!data2[*]}; do
#         if [[ ! -f "data/${data2[$index]}_$uc2smSize.csv" ]]; then
#             python code/dataPrep/make_csv_siemens.py \
#                 -i "data/${dataOrg2[$index]}.csv" \
#                 -o "data/${data2[$index]}" \
#                 -s $uc2smSize &
#         fi
#     done
#     wait
#     for index in ${!data2[*]}; do
#         if [ ! -f "data/${data2[$index]}_$uc2smSize.data.mtd" ]; then
#             systemds code/dataPrep/saveTrainSiemens.dml \
#                 -debug \
#                 -config code/conf/def.xml \
#                 -args "data/${data2[$index]}_$uc2smSize.csv" \
#                 "data/${data2[$index]}_$uc2smSize.data" &

#         fi
#     done
#     wait
#     for index in ${!data2[*]}; do
#         name="${data2[$index]}_$uc2smSize"
#         for wi in ${!addressb[*]}; do
#             numWorkers=$((wi + 1))
#             if [[ -f "data/${name}_${numWorkers}_1.data" ]] || [[ -d "data/${name}_${numWorkers}_1.data" ]]; then
#                 sleep 0
#             else
#                 systemds code/dataGen/slice.dml \
#                     -config code/conf/def.xml \
#                     -args $name $numWorkers &
#             fi
#             if [[ ! -f "data/fed_${name}_$numWorkers.json" ]]; then
#                 python code/dataGen/federatedMetaDataGenerator.py \
#                     -a $address -p $ports -n $numWorkers -d "${name}_" \
#                     -f ${data2cols[$index]} -e $uc2smSize &
#             fi
#         done
#     done
#     wait

# fi

## Mnist

for index in ${!addressb[*]}; do
    numWorkers=$((index + 1))
    if [[ ! -f "data/fed_mnist_features_${numWorkers}.json" ]]; then
        python code/dataGen/federatedMetaDataGenerator.py \
            -a $address -p $ports -n $numWorkers -d "mnist_features_" \
            -f 784 -e 60000 &
        python code/dataGen/federatedMetaDataGenerator.py \
            -a $address -p $ports -n $numWorkers -d "mnist_labels_" \
            -f 10 -e 60000 &
    fi
    if [[ ! -f "data/fed_P2_features_${numWorkers}.json" ]]; then
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
    fi
done

if [[ $HOSTNAME == "charlie" ]]; then
    if [[ ! -f "data/mnist_features.data.mtd" ]] && [[ ! -f "data/mnist_labels.data.mtd" ]]; then
        python code/dataGen/generate_mnist.py &
    fi

    # echo "P2 usecase"
    if [[ ! -f "data/P2_features.data.mtd" ]] || [[ ! -f "data/P2_labels.data.mtd" ]] ||
        [[ ! -f "data/P2P_features.data.mtd" ]] || [[ ! -f "data/P2P_labels.data.mtd" ]] ||
        [[ ! -f "data/P2P_features.csv.mtd" ]] || [[ ! -f "data/P2P_labels.csv.mtd" ]]; then
        echo "generating P2 data"
        systemds code/dataGen/P2datagen.dml \
            -config code/conf/def.xml

    fi

    if [[ ! -f "data/P2P_features.npy" ]]; then
        python code/dataGen/createData.py -p "P2P_features" &
    fi
    if [[ ! -f "data/P2P_labels.npy" ]]; then
        python code/dataGen/createData.py -p "P2P_labels" &
    fi

    ## Make Slices Mnist
    datasets=("mnist_features mnist_labels P2_features P2_labels P2P_features P2P_labels")
    # datasets=("P2_features P2_labels P2P_features P2P_labels")
    for name in $datasets; do
        for index in ${!addressb[*]}; do
            numWorkers=$((index + 2))
            if [[ ! -f "data/${name}_${numWorkers}_1.data.mtd" ]] && [[ $numWorkers -lt $((${#addressb[@]} + 1)) ]]; then
                echo "Generating data/${name}_${numWorkers}_1.data"
                systemds code/dataGen/slice.dml \
                    -config code/conf/def.xml \
                    -args $name $numWorkers &
            fi
        done

        wait
    done

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
        rsync -ah -e ssh --include="*_features.dat*" --exclude='*' "data/" ${addressb[0]}:$remoteDir/data/ &
        rsync -ah -e ssh --include="*_features.dat***" --exclude='*' "data/" ${addressb[0]}:$remoteDir/data/ &
        rsync -ah -e ssh --include="*_labels.dat*" --exclude='*' "data/" ${addressb[0]}:$remoteDir/data/ &
    done
fi

wait
# deactivate the python vertual environement
deactivate
