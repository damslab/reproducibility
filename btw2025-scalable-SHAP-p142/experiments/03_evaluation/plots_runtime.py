#!/usr/bin/env python
# coding: utf-8

# # Plots to evaluate runtimes on different models and setups

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

import argparse
parser=argparse.ArgumentParser(description="Plot runtime graphs..")
parser.add_argument("--data-dir", default="../10_data/", help="Path to dir where runtimes are stored.")
parser.add_argument("--plots-path", default="../11_results/", help="Path to dir where resulting pltos should be stored.")
parser.add_argument('--distributed', action='store_true', help='Also compute plots for distributed experiments.')
parser.add_argument('--show', action='store_true', help='Try to display plots during computation.')
args=parser.parse_args()

data_path = args.data_dir
plots_path = args.plots_path


# In[2]:
print(f"Plotting experiments to {plots_path} using data from {data_path}.")
print("Computing plots for runtime and speedup of local experiment.")

data_all = pd.read_csv(data_path+"runtimes_local.csv")

# In[3]:

# adult linlogreg
data_adult_linlogreg = data_all[data_all['exp_type'] == "adult_linlogreg"].drop(columns=['exp_type'])
data_adult_linlogreg = data_adult_linlogreg.groupby('instances').mean()

# In[18]:

# adult fnn
data_adult_fnn = data_all[data_all['exp_type'] ==  "adult_fnn"].drop(columns=['exp_type'])
data_adult_fnn = data_adult_fnn.groupby('instances').mean()

# In[11]:

# census svm
data_census_svm = data_all[data_all['exp_type'] == "census_l2svm"].drop(columns=['exp_type'])
data_census_svm = data_census_svm.groupby('instances').mean()

# In[6]:

# Define a custom formatter function
def thousands_formatter(x, pos):
    return '%1.1f' % (x * 1e-3)


# In[12]:

font = {'size': 12}

matplotlib.rc('font', **font)

# Create a figure and three subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# adult linlogreg
data_adult_linlogreg_tmp = data_adult_linlogreg.loc[data_adult_linlogreg.index <= 10000]
ax1.plot(data_adult_linlogreg_tmp.runtime_legacy_iterative[data_adult_linlogreg_tmp.runtime_legacy_iterative.notna()]/60, label="Iterative Preparation", color="tab:purple")
ax1.plot(data_adult_linlogreg_tmp.runtime_legacy[data_adult_linlogreg_tmp.runtime_legacy.notna()]/60, label="Vectorized Preparation", color="tab:cyan")
ax1.plot(data_adult_linlogreg_tmp.runtime_row/60, label="Parallel", color="tab:blue")
ax1.plot(data_adult_linlogreg_tmp.runtime_python/60, label="SHAP Python Package", linestyle="--", color="tab:red")

ax1.set_title("Logistic Regression \n Adult Dataset (107 Features)")
ax1.set_xlabel("# Instances")
ax1.set_ylabel("Runtime in Minutes")

# census svm
data_tmp = data_census_svm.loc[data_census_svm.index <= 10000]
ax2.plot(data_tmp.runtime_legacy_iterative/60, color="tab:purple")
ax2.plot(data_tmp.runtime_row/60, color="tab:blue")
ax2.plot(data_tmp.runtime_legacy/60, color="tab:cyan")

ax2.plot(data_tmp.runtime_python/60, linestyle="--", color="tab:red")

ax2.set_title("Linear Support Vector Machine \n Census Dataset (371 Features)")
ax2.set_xlabel("# Instances")
ax2.set_ylabel("Runtime in Minutes")

fig.legend(loc='upper center', ncol=4, bbox_to_anchor=(0.5, 0))
# Display the plot
plt.tight_layout()
print(f"Writing plot to {plots_path}Fig4_runtimes_linear_models_btw25.pdf")
plt.savefig(plots_path+"Fig4_runtimes_linear_models_btw25.pdf", bbox_inches='tight')
if args.show:
    plt.show()

# In[19]:

font = {'size': 12}

matplotlib.rc('font', **font)
# adult fnn
# data_tmp = data_adult_fnn.loc[data_adult_fnn.index <= 10000]
data_tmp = data_adult_fnn.groupby('instances').agg(['mean']).loc[data_adult_fnn.index <= 10000].dropna()
fig, (ax1) = plt.subplots(1, 1, figsize=(4, 3))

ax1.plot(data_tmp.runtime_legacy_iterative/60, label="Iterative Preparation", color="tab:purple")

ax1.plot(data_tmp.runtime_legacy/60, label="Vectorized Preparation", color="tab:cyan")
ax1.plot(data_tmp.runtime_row['mean']/60, label="Parallel", color="tab:blue")

# ax1.plot(data_tmp.runtime_row_non_var['mean']/60, label="Parallel\n(Non-var. Feat. removed)", color="tab:orange")
# ax1.plot(data_tmp.runtime_row_partitioned['mean']/60, label="Parallel\n(Partitioned)", color="tab:olive")

ax1.plot(data_tmp.runtime_python['mean']/60, label="SHAP Python Package", linestyle="--", color="tab:red")

ax1.set_ylim(-.1,15)
ax1.set_xlabel("# Instances")
ax1.set_ylabel("Runtime in Minutes")
# fig.legend(loc='upper right', ncol=2, bbox_to_anchor=(1.15, 0.05), fontsize=11)
ax1.legend(loc='upper right', fontsize=11)
# ax1.set_title("Runtime for Feed-Forward Neural Network \n on Adult Dataset with 107 Features (14 Partitions)")
plt.tight_layout()
print(f"Writing plot to {plots_path}Fig5_runtimes_fnn_btw25.pdf")
plt.savefig(plots_path+"Fig5_runtimes_fnn_btw25.pdf", bbox_inches='tight')
if args.show:
    plt.show()

    # In[27]:

# compute speedup
data_adult_linlogreg['speedup'] = data_adult_linlogreg.runtime_python/data_adult_linlogreg.runtime_row
data_census_svm['speedup'] = data_census_svm.runtime_python/data_census_svm.runtime_row
data_adult_fnn['speedup'] = data_adult_fnn.runtime_python/data_adult_fnn.runtime_row

# In[29]:

# speedup
cutoff = 10000
plt.subplots(1, 1, figsize=(8, 3))

plt.plot(data_adult_fnn.speedup.loc[data_adult_fnn.index <= cutoff].dropna(), label=f"Feed-Forward Neural Network - Adult (Max Speedup: {data_adult_fnn.speedup.loc[data_adult_fnn.index <= cutoff].max():.2f})")
plt.plot(data_census_svm.speedup.loc[data_census_svm.index <= cutoff].dropna(), label=f"Linear Support Vector Machine - Census 1990 (Max Speedup: {data_census_svm.speedup.loc[data_census_svm.index <= cutoff].max():.2f})")
plt.plot(data_adult_linlogreg.speedup.loc[data_adult_linlogreg.index <= cutoff].dropna(), label=f"Linear Logistic Regression - Adult (Max Speedup: {data_adult_linlogreg.speedup.loc[data_adult_linlogreg.index <= cutoff].max():.2f})")
plt.axhline(y=1, color='r', linestyle='--', alpha=.5)

plt.xlabel("# Instances")
plt.ylabel("Speedup")
plt.grid(True, alpha=.3)
# plt.gca().xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(thousands_formatter))

# Place the text box in the plot
props = dict(boxstyle='round', facecolor='white', alpha=1)
# plt.text(3300,1.5,"Speedup = 1", verticalalignment='top', bbox=props)
# plt.text(5300, 12.5, speedup_text, fontsize=12,verticalalignment='top', bbox=props)

# plt.title("Speedup of Row-wise Parallelized Permutation Sampling over \n PermutationExplainer of the shap Python Package")
plt.tight_layout()
# plt.yscale('log')
# plt.xscale('log')
plt.legend(loc='upper center', ncol=1, bbox_to_anchor=(0.51, -0.25))
print(f"Writing plot to {plots_path}Fig6_runtimes_speedup_max_10000_btw25.pdf")
plt.savefig(plots_path+"Fig6_runtimes_speedup_max_10000_btw25.pdf", bbox_inches='tight')
if args.show:
    plt.show()
print("Done with plots for local experiments.")

if args.distributed:
    print("Computing plots for cluster runtime and speedup.")

    # In[33]:

    data_cluster_all = pd.read_csv(data_path+"runtimes_distributed.csv")

    # adult linlogreg
    data_cluster_adult_linlogreg = data_cluster_all[data_cluster_all['exp_type'] == "adult_linlogreg"].drop(columns=['exp_type'])

    # adult fnn
    data_cluster_adult_fnn = data_cluster_all[data_cluster_all['exp_type'] == "adult_fnn"].drop(columns=['exp_type'])

    # census svm
    data_cluster_census_svm = data_cluster_all[data_cluster_all['exp_type'] == "census_l2svm"].drop(columns=['exp_type'])

    # In[35]:

    # combined plot

    font = {'size': 12}

    matplotlib.rc('font', **font)

    # Create a figure and three subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 3.5), sharey='row')

    # adult linlogreg
    xlim = 16000

    ax1.plot(data_adult_linlogreg.runtime_row.loc[data_adult_linlogreg.index <= xlim]/60, label="Parallel", color="tab:blue")
    # ax1.plot(data_adult_linlogreg.runtime_row_partitioned.loc[data_adult_linlogreg.index <= xlim]/60, label="Parallel (Partitioned)", color="tab:olive")

    t_data = data_cluster_adult_linlogreg[data_cluster_adult_linlogreg.executors_cluster == 8].drop(columns=['executors_cluster']).groupby('instances').mean()
    ax1.plot(t_data.runtime_cluster.loc[t_data.index <= xlim]/60, label=f'Parallel (8 Node Cluster)', color="tab:orange")
    # ax1.plot(t_data.runtime_cluster_partitioned.loc[t_data.index <= xlim]/60, label=f'Parallel (8 Nodes, Partitioned)', color="green")
    ax1.plot(data_adult_linlogreg.runtime_python.loc[data_adult_linlogreg.index <= xlim]/60, label="SHAP Python Package", linestyle="--", color="tab:red")
    ax1.set_title("Logistic Regression\nAdult Dataset\n(107 Features)")#., 13 Partitions)")
    ax1.set_xlabel("# Instances")
    ax1.set_ylabel("Runtime in Minutes\n")

    # census svm
    t_data = data_cluster_census_svm[data_cluster_census_svm.executors_cluster == 8].drop(columns=['executors_cluster']).groupby('instances').mean()
    ax2.plot(t_data.runtime_cluster.loc[t_data.index <= xlim]/60, color="tab:orange")
    # ax2.plot(t_data.runtime_cluster_partitioned.loc[t_data.index <= xlim]/60, color="green")

    ax2.plot(data_census_svm.runtime_row.loc[data_census_svm.index <= xlim]/60, color="tab:blue")
    # ax2.plot(data_census_svm.runtime_row_partitioned.loc[data_census_svm.index <= xlim]/60, color="tab:olive")

    ax2.plot(data_census_svm.runtime_python.loc[data_census_svm.index <= 6000]/60, linestyle="--", color="tab:red")

    ax2.set_title("Linear Support Vector Machine\nCensus Dataset\n(371 Features)")#., 68 Partitions)")
    ax2.set_xlabel("# Instances")
    # ax2.set_ylabel("Runtime in Minutes")
    ax2.set_ylim(-1,8)

    ax3.plot(data_adult_fnn.runtime_row.loc[data_adult_fnn.index <= xlim].dropna()/60, color="tab:blue")
    # ax3.plot(data_adult_fnn_tmp.runtime_row_partitioned.loc[data_adult_fnn_tmp.index <= xlim]/60, color="tab:olive")
    ax3.plot(data_adult_fnn.runtime_python.loc[data_adult_fnn.index <= xlim]/60, linestyle="--", color="tab:red")
    t_data = data_cluster_adult_fnn[data_cluster_adult_fnn.executors_cluster == 8].drop(columns=['executors_cluster']).groupby('instances').mean()
    ax3.plot(t_data.runtime_cluster.loc[t_data.index <= xlim]/60, color="tab:orange")
    # ax3.plot(t_data.runtime_cluster_partitioned.loc[t_data.index <= xlim]/60, color="green")

    ax3.set_xlabel("# Instances")
    ax3.set_ylabel("Runtime in Minutes")
    ax3.set_ylim(0,8)
    ax3.set_title("Feed-Forward Neural Netw.\nAdult Dataset\n(107 Features)")
    # ax3.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(thousands_formatter))

    fig.legend(loc='upper center', ncol=3, bbox_to_anchor=(0.5, 0.05))
    # Display the plot
    plt.tight_layout()
    print(f"Writing plot to {plots_path}Fig7_runtimes_models_cluster_btw25.pdf")
    plt.savefig(plots_path+"Fig7_runtimes_models_cluster_btw25.pdf", bbox_inches='tight')
    if args.show:
        plt.show()

    # In[37]:

    data_speedup_cluster = data_cluster_census_svm[['instances','runtime_cluster','executors_cluster']].groupby(['executors_cluster','instances']).mean().join(data_census_svm[['runtime_row','runtime_row_partitioned']], on='instances')
    data_speedup_cluster['speedup_row'] = data_speedup_cluster.runtime_row / data_speedup_cluster.runtime_cluster
    data_speedup_cluster['speedup_row_partitioned'] = data_speedup_cluster.runtime_row_partitioned / data_speedup_cluster.runtime_cluster
    data_speedup_cluster = data_speedup_cluster.reset_index(level=0)

    # In[38]:

    # combined plot

    font = {'size': 12}

    matplotlib.rc('font', **font)

    # Create a figure and three subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 3), sharey='row')

    xlim = 15000

    # prep linlogreg data
    # prep svm data
    data_scalability_cluster_adult_linlogreg = data_cluster_adult_linlogreg[['instances','runtime_cluster','executors_cluster']].groupby(['executors_cluster','instances']).mean().join(data_adult_linlogreg[['runtime_row','runtime_row_partitioned']], on='instances')
    data_scalability_cluster_adult_linlogreg['scalability_row'] = data_scalability_cluster_adult_linlogreg.runtime_row / data_scalability_cluster_adult_linlogreg.runtime_cluster
    data_scalability_cluster_adult_linlogreg['scalability_row_partitioned'] = data_scalability_cluster_adult_linlogreg.runtime_row_partitioned / data_scalability_cluster_adult_linlogreg.runtime_cluster
    data_scalability_cluster_adult_linlogreg = data_scalability_cluster_adult_linlogreg.reset_index(level=0)

    for executors in [2,4,8]:
        t_data = data_scalability_cluster_adult_linlogreg[data_scalability_cluster_adult_linlogreg.executors_cluster == executors]
        t_max = t_data.loc[t_data.index<=xlim].scalability_row.max()
        ax1.plot(t_data.scalability_row.loc[t_data.index <= xlim]/executors)

    ax1.set_title("Log. Reg. on Adult (107  Feat.)")
    # ax2.legend(ncol=1)
    ax1.set_xlabel("# Instances")
    ax1.set_ylabel("Efficiency")
    ax1.set_xlim(-1000,xlim+1000)

    # prep svm data
    data_scalability_cluster_census_svm = data_cluster_census_svm[['instances','runtime_cluster','executors_cluster']].groupby(['executors_cluster','instances']).mean().join(data_census_svm[['runtime_row','runtime_row_partitioned']], on='instances')
    data_scalability_cluster_census_svm['scalability_row'] = data_scalability_cluster_census_svm.runtime_row / data_scalability_cluster_census_svm.runtime_cluster
    data_scalability_cluster_census_svm['scalability_row_partitioned'] = data_scalability_cluster_census_svm.runtime_row_partitioned / data_scalability_cluster_census_svm.runtime_cluster
    data_scalability_cluster_census_svm = data_scalability_cluster_census_svm.reset_index(level=0)

    for executors in [2,4,8]:
        t_data = data_scalability_cluster_census_svm[data_scalability_cluster_census_svm.executors_cluster == executors]
        t_max = t_data.loc[t_data.index<=xlim].scalability_row.max()
        ax2.plot(t_data.scalability_row.loc[t_data.index <= xlim]/executors, label=f'{executors} Nodes')

    ax2.set_title("SVM on Census (371 Feat.)")
    # ax2.legend(ncol=1)
    ax2.set_xlabel("# Instances")
    ax2.set_xlim(-1000, xlim+1000)

    # prep fnn data
    data_scalability_cluster_adult_fnn = data_cluster_adult_fnn[['instances','runtime_cluster','executors_cluster']].groupby(['executors_cluster','instances']).mean().join(data_adult_fnn[['runtime_row','runtime_row_partitioned']], on='instances')
    data_scalability_cluster_adult_fnn['scalability_row'] = data_scalability_cluster_adult_fnn.runtime_row / data_scalability_cluster_adult_fnn.runtime_cluster
    data_scalability_cluster_adult_fnn['scalability_row_partitioned'] = data_scalability_cluster_adult_fnn.runtime_row_partitioned / data_scalability_cluster_adult_fnn.runtime_cluster
    data_scalability_cluster_adult_fnn = data_scalability_cluster_adult_fnn.reset_index(level=0)

    for executors in [2,4,8]:
        t_data = data_scalability_cluster_adult_fnn[data_scalability_cluster_adult_fnn.executors_cluster == executors]
        t_max = t_data.loc[t_data.index<=xlim].scalability_row.max()
        ax3.plot(t_data.scalability_row.loc[t_data.index <= xlim]/executors)

    ax3.set_title("FNN on Adult (107  Feat.)")
    # ax2.legend(ncol=1)
    ax3.set_xlabel("# Instances")
    ax3.set_xlim(-1000,xlim+1000)




    # fig.suptitle("Cluster Scalability of Row-wise Parallelized Permutation Sampling\nSVM on Census with 371 Features")
    plt.tight_layout()
    fig.legend(loc='upper center', ncol=3, bbox_to_anchor=(0.5, 0.05))
    print(f"Writing plot to {plots_path}Fig8_runtimes_scalability_btw25.pdf")
    plt.savefig(plots_path+"Fig8_runtimes_scalability_btw25.pdf", bbox_inches='tight')
    if args.show:
        plt.show()

    # In[ ]:

    data_weak_scaling = pd.read_csv(data_path+"runtimes_cluster_weak_scaling.csv")
    data_instance_scaling = data_weak_scaling[data_weak_scaling['exp_type'] == 'instance_scaling_census_svm'] \
        .drop(columns=['exp_type','start','end']).groupby(['num_executors','instances']).mean().reset_index()
    data_instance_scaling_singlenode = data_instance_scaling[data_instance_scaling['num_executors']==1]
    data_instance_scaling = data_instance_scaling.loc[data_instance_scaling.groupby('num_executors')['instances'].idxmin()]

    data_feature_scaling = data_weak_scaling[data_weak_scaling['exp_type'] == 'feature_scaling_census_svm'] \
        .drop(columns=['exp_type','start','end']).groupby(['num_executors','features']).mean().reset_index()
    data_feature_scaling_singlenode = data_feature_scaling[data_feature_scaling['num_executors']==1]
    data_feature_scaling = data_feature_scaling.loc[data_feature_scaling.groupby('num_executors')['features'].idxmin()]

    data_layer_scaling = data_weak_scaling[data_weak_scaling['exp_type'] == 'layer_scaling_adult_fnn'] \
        .drop(columns=['exp_type','start','end']).groupby(['num_executors','fnn_layers']).mean().reset_index()
    data_layer_scaling_singlenode = data_layer_scaling[data_layer_scaling['num_executors']==1]
    data_layer_scaling = data_layer_scaling.loc[data_layer_scaling.groupby('num_executors')['fnn_layers'].idxmin()]

    # In[ ]:

    # weakscaling, single plot
    font = {'size': 12}

    matplotlib.rc('font', **font)

    fig, (ax1) = plt.subplots(1, 1, figsize=(4, 3))

    # instance scaling
    # ax1.set_title("Weak Scaling")
    ax1.plot(data_instance_scaling_singlenode.instances/3500, data_instance_scaling_singlenode.runtime/60, color="tab:blue", linestyle=":")
    ax1.plot(data_instance_scaling.instances/3500, data_instance_scaling.runtime/60, color="tab:blue")
    ax1.set_xlabel("Scaling Factor")

    ax1.plot(data_feature_scaling_singlenode.features/45, data_feature_scaling_singlenode.runtime/60, color="tab:orange", linestyle=":")
    ax1.plot(data_feature_scaling.features/45, data_feature_scaling.runtime/60, color="tab:orange")

    ax1.plot(data_layer_scaling.fnn_layers, data_layer_scaling.runtime/60, color="tab:green")
    ax1.plot(data_layer_scaling_singlenode.fnn_layers, data_layer_scaling_singlenode.runtime/60, color="tab:green", linestyle=":")

    ax1.set_ylabel("Runtime in Minutes")
    ax1.set_ylim(0,15)

    custom_handles = [
        matplotlib.lines.Line2D([0], [0], color='black', linestyle=':', lw=2, label='Singlenode'),
        matplotlib.lines.Line2D([0], [0], color='black', linestyle='-', lw=2, label='Proportional Nodescaling (1-8)'),
        matplotlib.patches.Patch(color='tab:blue', label='Instance Scaling (3.5k-28k, SVM Census)'),
        matplotlib.patches.Patch(color='tab:orange', label='Feature Scaling (45-360, SVM Census)'),
        matplotlib.patches.Patch(color='tab:green', label='Hidden Layer Scaling (1-8, FNN Adult)'),
    ]

    fig.legend(loc='upper center', ncol=1, bbox_to_anchor=(0.525, 0.05), handles=custom_handles, prop={'size': 11})
    # Display the plot
    plt.tight_layout()
    print(f"Writing plot to {plots_path}Fig9_weak_scaling_btw25.pdf")
    plt.savefig(plots_path+"Fig9_weak_scaling_btw25.pdf", bbox_inches='tight')
    if args.show:
        plt.show()
