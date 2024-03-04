#!/bin/bash

source parameters.sh

echo "$(date) Starting Plotting Pipeline"

mkdir -p plotting/plots/ReadWrite
mkdir -p plotting/plots/ReadWrite/$HOSTNAME
mkdir -p plotting/plots/ReadWrite/dams-su1
mkdir -p plotting/plots/ReadWrite/dams-so010

mkdir -p plotting/tables/ReadWrite
mkdir -p plotting/tables/ReadWrite/$HOSTNAME
mkdir -p plotting/tables/ReadWrite/dams-su1
mkdir -p plotting/tables/ReadWrite/dams-so010

mkdir -p plotting/plots/ReadWriteFrame
mkdir -p plotting/plots/ReadWriteFrame/$HOSTNAME
mkdir -p plotting/plots/ReadWriteFrame/dams-su1
mkdir -p plotting/plots/ReadWriteFrame/dams-so010

mkdir -p plotting/tables/ReadWriteFrame
mkdir -p plotting/tables/ReadWriteFrame/$HOSTNAME
mkdir -p plotting/tables/ReadWriteFrame/dams-su1
mkdir -p plotting/tables/ReadWriteFrame/dams-so010

mkdir -p plotting/plots/Performance
mkdir -p plotting/plots/Performance/$HOSTNAME
mkdir -p plotting/plots/Performance/dams-so002
mkdir -p plotting/plots/Performance/dams-so009
mkdir -p plotting/plots/Performance/dams-so010
mkdir -p plotting/plots/Performance/dams-so011


# python ./plotting/scripts/table_readWrite_matrix.py &
# python ./plotting/scripts/table_readWrite_frame.py &
# python ./plotting/scripts/table_UCR.py &
# python ./plotting/scripts/table_transform.py &

python plotting/scripts/table_kmeans.py &
python plotting/scripts/table_kmeans10.py &
python plotting/scripts/table_readWrite_New.py &
python plotting/scripts/table_transform_encode_real_new.py &
python plotting/scripts/table_transform_encode_lossy.py &
python plotting/scripts/table_transform_encode_time.py &
python plotting/scripts/table_acc_lm_santander.py &
python plotting/scripts/table_19_baselineLM.py &

python plotting/scripts/table_20_lossyLM.py &
python plotting/scripts/table_21_scaling.py &
python plotting/scripts/table_22_poly.py &
python plotting/scripts/table_23_algorithm.py & 
python plotting/scripts/table_25_others.py & 


wait
echo "$(date) Done Making tables"

# Figure 2
python ./plotting/scripts/plot_distinct_motivation.py &

# Figure 3
python ./plotting/scripts/plot_lossy_binning.py &

# Figure 4
python ./plotting/scripts/plot_micro_scale_size.py &

# Figure 5
python ./plotting/scripts/plot_corr.py &

# Figure 6
python ./plotting/scripts/plot_motivation_breakdown.py &

# Figure 16 
python ./plotting/scripts/plot_compression_size.py &
python ./plotting/scripts/plot_compression_size_disk.py &
python ./plotting/scripts/plot_compression_size_time.py &
python ./plotting/scripts/plot_compression_size_time_write.py &

# Figure 18
python ./plotting/scripts/plot_lossy_transform.py &
python ./plotting/scripts/plot_lossy_transform_disk.py &
python ./plotting/scripts/plot_lossy_transform_time.py &

# Figure 17
python ./plotting/scripts/plot_TE_size.py &
python ./plotting/scripts/plot_TE_size_disk.py &
python ./plotting/scripts/plot_TE_size_time.py &
python ./plotting/scripts/plot_TE_size_time_read.py &
python ./plotting/scripts/plot_TE_size_time_TE.py &

python ./plotting/scripts/plot_19_lmBaseline.py & 
python ./plotting/scripts/plot_20_lmlossy.py &
python ./plotting/scripts/plot_21_scaling.py &
python ./plotting/scripts/plot_22_poly.py &
python ./plotting/scripts/plot_23_algorithms.py &
python ./plotting/scripts/plot_25_others.py & 


### OLD!
# python ./plotting/scripts/plot_WInM.py &
# python ./plotting/scripts/plot_Serialization.py &
# python ./plotting/scripts/plot_sparse0.5-64k-Binary.py &
# python ./plotting/scripts/plot_sparse0.5-256k-Binary.py &
# python ./plotting/scripts/plot_sparse1.0-64k-Ternary.py &
# python ./plotting/scripts/plot_sparsities-64k.py &
# python ./plotting/scripts/plot_sparsities-256k.py &
# python ./plotting/scripts/plot_distict-64k.py &
# python ./plotting/scripts/plot_readWriteFrame_sparse0.5_64k_Binary.py &

wait
echo "$(date) Done Making Plots"
