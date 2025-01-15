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

data_file="${1:-../10_data/runtimes_cluster_weak_scaling.csv}"
permutations=3
samples=100
instances=30000

num_samp_per_config=6
if [ "${SHAP_FAST_EXP}" = "1" ]; then
  echo "SHAP_FAST_EXP is set. Running with just 1 run per configuration to be faster."
  num_samp_per_config=2
fi

#types
instance_scaling=true
feature_scaling=true
layer_scaling=true

hdfs_dir="/user/hadoop/scalable-shap/10_data/"

#svm
census_data_sysds_str="data_dir=$hdfs_dir/census/ X_bg_path=Census_X.csv B_path=models/Census_SVM.csv model_type=l2svmPredict"

echo "Outputfile: $data_file"

echo "exp_type,num_executors,instances,features,fnn_layers,start,end,runtime" | tee "$data_file"
for j in $(seq 1 $num_samp_per_config); do
   for scaling_factor in 1 2 4 8 ; do
	
  	#scale executors on every odd run
	if (( j % 2 != 0 )); then
		num_executors=$scaling_factor
	else
		num_executors=1
	fi

	if [ $instance_scaling = true ]; then  
    	  echo -e "\n\n===============\nINSTANCE SCALING\n\n"
	  #instance scaling
	  inst_scaling=$((3500*scaling_factor))
	  start=`date '+%F_%H:%M:%S'`
	  echo -n "instance_scaling_census_svm,${num_executors},${inst_scaling},371,NaN,${start}," | tee -a "$data_file"
	  runtime_instances=$(./runSystemDS_distributed ${num_executors} -f ./shap-experiment-distributed.dml -stats 1 -nvargs remove_non_var=0 use_partitions=0 n_permutations=${permutations} integration_samples=${samples} rows_to_explain=${inst_scaling} write_to_file=0 execution_policy=by-row metadata_path=Census_partitions.csv ${census_data_sysds_str})
    	  echo "$runtime_instances"
	  runtime_instances=$(echo "$runtime_instances" | grep "Total elapsed time" | awk '{print $4}' | tr \, \.)
	  end=`date '+%F_%H:%M:%S'`
    	  echo "${end},${runtime_instances}" | tee -a "$data_file"
    	  unset runtime_instances
	fi	
	if [ $feature_scaling = true ]; then
    	  echo -e "\n\n===============\nFEATURE SCALING\n\n"
	  #feature scaling
	  n_features=$((45*scaling_factor))
	  start=`date '+%F_%H:%M:%S'`
	  echo -n "feature_scaling_census_svm,${num_executors},${instances},${n_features},NaN,${start}," | tee -a "$data_file"
	  runtime_features=$(./runSystemDS_distributed ${num_executors} -f ./shap-experiment-distributed.dml -stats 1 -nvargs remove_non_var=0 use_partitions=1 n_permutations=${permutations} integration_samples=${samples} rows_to_explain=${instances} write_to_file=0 execution_policy=by-row metadata_path=partitions_${n_features}.csv ${census_data_sysds_str})
	  end=`date '+%F_%H:%M:%S'`
    	  echo "$runtime_features"
	  runtime_features=$(echo "$runtime_features" | grep "Total elapsed time" | awk '{print $4}' | tr \, \.)
    	  echo "${end},${runtime_features}" | tee -a "$data_file"
    	  unset runtime_features
	fi
	if [ $layer_scaling = true ]; then
    	  echo -e "\n\n===============\nLAYER SCALING\n\n"
	  #layer scaling
	  start=`date '+%F_%H:%M:%S'`
	  
	  echo -n "layer_scaling_adult_fnn,${num_executors},${instances},107,${scaling_factor},${start}," | tee -a "$data_file"
	  runtime_layers=$(./runSystemDS_distributed ${num_executors} -f ./shap-experiment-distributed.dml -stats 1 -nvargs remove_non_var=0 use_partitions=0 n_permutations=${permutations} integration_samples=${samples} rows_to_explain=${instances} write_to_file=0 execution_policy=by-row data_dir=$hdfs_dir/adult/ X_bg_path=Adult_X.csv B_path=models/Adult_FNN_${scaling_factor}l.bin metadata_path=Adult_partitions.csv model_type=ffPredict_${scaling_factor}l)
	  end=`date '+%F_%H:%M:%S'`

    	  echo "$runtime_layers"
	  runtime_layers=$(echo "$runtime_layers" | grep "Total elapsed time" | awk '{print $4}' | tr \, \.)
    	  echo "${end},${runtime_layers}" | tee -a "$data_file"
    	  unset runtime_layers
	fi
    done
done
