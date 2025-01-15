#!/bin/bash
#-------------------------------------------------------------
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
#-------------------------------------------------------------
#
#Runs systemds multiple times and stores resulting runtimes and sample sizes in file

data_file="${1:-../10_data/runtimes_local.csv}"
incr_instances="${2:-250}"
max_instances="${3:-15000}"
stderr_file="${4:-errors_local.log}"
permutations=3
samples=100

num_samp_per_config=3
if [ "${SHAP_FAST_EXP}" = "1" ]; then
  echo "SHAP_FAST_EXP is set. Running with just 1 run per configuration and 2500 instances added ech run to be faster."
  num_samp_per_config=1
  incr_instances=2500
fi


#logreg
adult_data_sysds_str="data_dir=../10_data/adult/ X_bg_path=Adult_X.csv B_path=models/Adult_MLR.csv metadata_path=Adult_partitions.csv model_type=multiLogRegPredict"
adult_data_python_str="--data-dir=../10_data/adult/ --data-x=Adult_X.csv --model-type=multiLogReg"

#fnn
adult_fnn_data_sysds_str="data_dir=../10_data/adult/ X_bg_path=Adult_X.csv B_path=models/Adult_FNN.bin metadata_path=Adult_partitions.csv model_type=ffPredict"
adult_fnn_data_python_str="--data-dir=../10_data/adult/ --data-x=Adult_X.csv --model-type=fnn"

census_data_sysds_str="data_dir=../10_data/census/ X_bg_path=Census_X.csv B_path=models/Census_SVM.csv metadata_path=Census_partitions.csv model_type=l2svmPredict"
census_data_python_str="--data-dir=../10_data/census/ --data-x=Census_X.csv --data-y=Census_y_corrected.csv --model-type=l2svm"

exp_type_array=("adult_linlogreg" "census_l2svm" "adult_fnn")

echo "Outputfile: $data_file"
echo "Errors got to $stderr_file"
echo "Exp types: ${exp_type_array[@]}"

echo "Errors from run at $(date +"%Y-%m-%d %H:%M:%S")" > $stderr_file
echo "exp_type,instances,runtime_python,runtime_row,runtime_row_non_var,runtime_row_partitioned,runtime_permutation,runtime_legacy,runtime_legacy_iterative" | tee "$data_file"
for instances in $(seq 0 $incr_instances $max_instances); do
    #set to 1 on first run
    [[ $instances -eq 0 ]] && instances=1

    #take three samples per size
    for j in $(seq 1 $num_samp_per_config); do
      for exp_type in "${exp_type_array[@]}"; do
	  if [ "$exp_type" = "adult_linlogreg" ]; then
	      data_str=$adult_data_sysds_str
              py_str=$adult_data_python_str
          elif [ "$exp_type" = "census_l2svm" ]; then
              data_str=$census_data_sysds_str
              py_str=$census_data_python_str
          elif [ "$exp_type" = "adult_fnn" ]; then
              data_str=$adult_fnn_data_sysds_str
              py_str=$adult_fnn_data_python_str
          else
              echo "Exp type unknown: $exp_type"
              exit 1
          fi
	  
	  echo "--> Model type $exp_type | $permutations permutations | $instances instances..."
          echo -n "${exp_type},${instances}," | tee -a "$data_file"
	  runtime_python=$(python ./shap-experiment-python.py ${py_str} --n-permutations=${permutations} --n-instances=${instances} --silent --just-print-t 2>>/dev/null)
          echo -n "${runtime_python}," | tee -a "$data_file"

          #by-row
          runtime_r=$(./runSystemDS_local -f ./shap-experiment.dml -stats 1 -nvargs ${data_str} n_permutations=${permutations} integration_samples=${samples} rows_to_explain=${instances} write_to_file=0 execution_policy=by-row 2>>$stderr_file | grep "Total elapsed time" | awk '{print $4}' | tr \, \.)
          echo -n "${runtime_r}," | tee -a "$data_file"

          #by-row non var
          runtime_r_non_var="-1" #$(./runSystemDS_local -f ./shap-experiment.dml -stats 1 -nvargs ${data_str} remove_non_var=1 n_permutations=${permutations} integration_samples=${samples} rows_to_explain=${instances} write_to_file=0 execution_policy=by-row 2>>$stderr_file | grep "Total elapsed time" | awk '{print $4}' | tr \, \.)
          echo -n "${runtime_r_non_var}," | tee -a "$data_file"

          #by-row partitioned
          runtime_r_partitioned="-1" #$(./runSystemDS_local -f ./shap-experiment.dml -stats 1 -nvargs ${data_str} remove_non_var=0 use_partitions=1 n_permutations=${permutations} integration_samples=${samples} rows_to_explain=${instances} write_to_file=0 execution_policy=by-row  2>>$stderr_file | grep "Total elapsed time" | awk '{print $4}' | tr \, \.)
          echo -n "${runtime_r_partitioned}," | tee -a "$data_file"

          #by-permutation
          runtime_p="-1" #$(./runSystemDS_local -f ./shap-experiment.dml -stats 1 -nvargs ${data_str} n_permutations=${permutations} integration_samples=${samples} rows_to_explain=${instances} write_to_file=0 execution_policy=by-permutation 2>>$stderr_file | grep "Total elapsed time" | awk '{print $4}' | tr \, \.)
          echo -n "${runtime_p}," | tee -a "$data_file"
          unset runtime_p

          #legacy
          runtime_l=$(./runSystemDS_local -f ./shap-experiment.dml -stats 1 -nvargs ${data_str} n_permutations=${permutations} integration_samples=${samples} rows_to_explain=${instances} write_to_file=0 execution_policy=legacy 2>>$stderr_file | grep "Total elapsed time" | awk '{print $4}' | tr \, \.)
          echo -n "${runtime_l}," | tee -a "$data_file"
          unset runtime_l

          #legacy-iterative
          runtime_l_i=$(./runSystemDS_local -f ./shap-experiment.dml -stats 1 -nvargs ${data_str} n_permutations=${permutations} integration_samples=${samples} rows_to_explain=${instances} write_to_file=0 execution_policy=legacy-iterative 2>>$stderr_file | grep "Total elapsed time" | awk '{print $4}' | tr \, \.)
          echo -n "${runtime_l_i}" | tee -a "$data_file"
          unset runtime_l_i

          #newline
          echo "" | tee -a "$data_file"
        done
    done
done
