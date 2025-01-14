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

data_file="${1:-../10_data/runtimes_distributed.csv}"
permutations=3
samples=100

hdfs_dir="/user/hadoop/scalable-shap/10_data/"

#logreg
adult_data_sysds_str="data_dir=${hdfs_dir}adult/ X_bg_path=Adult_X.csv B_path=models/Adult_MLR.csv metadata_path=Adult_partitions.csv model_type=multiLogRegPredict"

#fnn
adult_ffn_data_sysds_str="data_dir=${hdfs_dir}adult/ X_bg_path=Adult_X.csv B_path=models/Adult_FNN.bin metadata_path=Adult_partitions.csv model_type=ffPredict"

#svm
census_data_sysds_str="data_dir=${hdfs_dir}census/ X_bg_path=Census_X.csv B_path=models/Census_SVM.csv metadata_path=Census_partitions.csv model_type=l2svmPredict"

exp_type_array=("adult_linlogreg" "census_l2svm" "adult_fnn")
echo "Outputfile: $data_file"

echo "exp_type,instances,runtime_row,runtime_row_non_var,runtime_row_partitioned,runtime_permutation,runtime_cluster,runtime_cluster_partitioned,executors_cluster" | tee "$data_file"
for instances in $(seq 0 1000 16000); do
    #set to 1 on first run
    [[ $instances -eq 0 ]] && instances=1

    #take three samples per size
    for j in {1..3}; do
      for num_executors in 2 4 8 ; do
        for exp_type in "${exp_type_array[@]}"; do
          if [ "$exp_type" = "adult_linlogreg" ]; then
            data_str=$adult_data_sysds_str
          elif [ "$exp_type" = "adult_fnn" ]; then
            data_str=$adult_ffn_data_sysds_str
          elif [ "$exp_type" = "census_l2svm" ]; then
            data_str=$census_data_sysds_str
          else
            echo "Exp type unknown: $exp_type"
            exit 1
          fi

          # we dont rerun all the local experiments since we already have that data
          #by-row
          runtime_r=''
          #$(systemds ./shapley-permutation-experiment.dml -stats 1 -nvargs ${data_str} n_permutations=${permutations} integration_samples=${samples} rows_to_explain=${instances} write_to_file=0 execution_policy=by-row 2>/dev/null | grep "Total elapsed time" | awk '{print $4}' | tr \, \.)
          echo -n "${exp_type},${instances},${runtime_r}," | tee -a "$data_file"

          #by-row non var
          runtime_r_non_var=''
          #$(systemds ./shapley-permutation-experiment.dml -stats 1 -nvargs ${data_str} remove_non_var=1 n_permutations=${permutations} integration_samples=${samples} rows_to_explain=${instances} write_to_file=0 execution_policy=by-row 2>/dev/null | grep "Total elapsed time" | awk '{print $4}' | tr \, \.)
          echo -n "${runtime_r_non_var}," | tee -a "$data_file"

          #by-row partitioned
          runtime_r_partitioned=''
          #runtime_r_partitioned=$(systemds ./shapley-permutation-experiment.dml -stats 1 -nvargs ${data_str} remove_non_var=0 use_partitions=1 n_permutations=${permutations} integration_samples=${samples} rows_to_explain=${instances} write_to_file=0 execution_policy=by-row  2>/dev/null | grep "Total elapsed time" | awk '{print $4}' | tr \, \.)
          echo -n "${runtime_r_partitioned}," | tee -a "$data_file"

          #by-permutation
          [[ $instances -le 10000 ]] && runtime_p=''
          #runtime_p=$(systemds ./shapley-permutation-experiment.dml -stats 1 -nvargs ${data_str} n_permutations=${permutations} integration_samples=${samples} rows_to_explain=${instances} write_to_file=0 execution_policy=by-permutation 2>/dev/null | grep "Total elapsed time" | awk '{print $4}' | tr \, \.)
          echo -n "${runtime_p}," | tee -a "$data_file"
          unset runtime_p

          #cluster
          runtime_cluster=$(./runSystemDS_distributed ${num_executors} -f  ./shap-experiment-distributed.dml -stats 1 -nvargs remove_non_var=0 use_partitions=0 n_permutations=${permutations} integration_samples=${samples} rows_to_explain=${instances} write_to_file=0 execution_policy=by-row ${data_str})
          runtime_cluster=$(echo "$runtime_cluster" | grep "Total elapsed time" | awk '{print $4}' | tr \, \.)
          echo -n "${runtime_cluster}," | tee -a "$data_file"
          unset runtime_cluster

          runtime_cluster_partitioned=''
	  #$(./runSystemDS_distributed ${num_executors} -f /home/lepage/scripts/shap/examples/shapley-permutation-experiment-spark.dml -stats 1 -nvargs remove_non_var=0 use_partitions=1 n_permutations=${permutations} integration_samples=${samples} rows_to_explain=${instances} write_to_file=0 execution_policy=by-row ${data_str})
          #echo "$runtime_cluster_partitioned"
          #runtime_cluster_partitioned=$(echo "$runtime_cluster_partitioned" | grep "Total elapsed time" | awk '{print $4}' | tr \, \.)
          echo -n "${runtime_cluster_partitioned},${num_executors}" | tee -a "$data_file"
          unset runtime_cluster_partitioned

          #newline
          echo "" | tee -a "$data_file"
        done
	    done
    done
done
