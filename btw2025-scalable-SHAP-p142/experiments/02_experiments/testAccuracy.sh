#!/bin/bash
set -e

n_computations="${1:-100}"

mkdir -p "../10_data/accuracy/python"
mkdir -p "../10_data/accuracy/systemds"
source ../python-venv/bin/activate

adult_data_sysds_str="data_dir=../10_data/adult/ X_bg_path=Adult_X.csv B_path=models/Adult_MLR.csv metadata_path=Adult_partitions.csv model_type=multiLogRegPredict"
adult_data_python_str="--data-dir=../10_data/adult/ --data-x=Adult_X.csv --model-type=multiLogReg"

census_data_sysds_str="data_dir=../10_data/census/ X_bg_path=Census_X.csv B_path=models/Census_SVM.csv metadata_path=Census_partitions.csv model_type=l2svmPredict"
census_data_python_str="--data-dir=../10_data/census/ --data-x=Census_X.csv --data-y=Census_y_corrected.csv --model-type=l2svm"

exp_type_array=("adult_linlogreg" "census_l2svm")

instances=50
permutations=10
samples=100



 for exp_type in "${exp_type_array[@]}"; do

    if [ "$exp_type" = "adult_linlogreg" ]; then
       data_str=$adult_data_sysds_str
       py_str=$adult_data_python_str
    elif [ "$exp_type" = "census_l2svm" ]; then
       data_str=$census_data_sysds_str
       py_str=$census_data_python_str
    else
       echo "Exp type unknown: $exp_type"
       exit 1
    fi

    echo "------ Running $exp_type for $permutations permutrations and $samples samples... ------"
    for n in $(seq 1 ${n_computations}); do
       echo "N: $n"
       echo "systemds..."
       #by-row
       ./runSystemDS_local -f ./shap-experiment.dml -nvargs ${data_str} n_permutations=${permutations} integration_samples=${samples} rows_to_explain=${instances} write_to_file=1 execution_policy=by-row output_dir="../10_data/accuracy/systemds/" file_tag="_${exp_type}_systemds_${n}"


    	echo "python..."
    	#python
    	#we compute values when plotting, since we only compare for 50 instances, thats fast enough
    	python3 ./shap-experiment-python.py ${py_str} --n-permutations=${permutations} --n-instances=${instances} --n-samples=${samples}  --result-file-name="../10_data/accuracy/python/shap-values_permutation_${permutations}perm_${samples}samples_${exp_type}_python_${n}.csv" --silent
    done
    echo "---------------------------------------------------------------------------------------"
done

