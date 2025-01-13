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
parser.add_argument("--plots-path", default="./plots/", help="Path to dir where resulting pltos should be stored.")
parser.add_argument('--local', action='store_true', help='Compute plots for local experiments.')
parser.add_argument('--distributed', action='store_true', help='Compute plots for distributed experiments.')
parser.add_argument('--show', action='store_true', help='Try to display plots during computation.')
args=parser.parse_args()

data_path = args.data_dir
plots_path = args.plots_path

if args.local:
    # In[2]:
    print(f"Plotting local experiments to {plots_path} using data from {data_path}.")

    data_all = pd.read_csv(data_path+"runtimes_local.csv")

    # In[3]:

    # adult linlogreg
    data_adult_linlogreg = data_all[data_all['exp_type'] == "adult_linlogreg"].drop(columns=['exp_type'])
    data_adult_linlogreg = data_adult_linlogreg.groupby('instances').mean()

    # In[18]:

    # adult fnn
    data_adult_fnn = data_all[data_all['exp_type'].isin(["adult_ffn", "adult_fnn"])].drop(columns=['exp_type'])
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
    print(f"Writing plot to {plots_path}runtimes_linear_models_btw25.pdf")
    plt.savefig(plots_path+"runtimes_linear_models_btw25.pdf", bbox_inches='tight')
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
    print(f"Writing plot to {plots_path}runtimes_fnn_btw25.pdf")
    plt.savefig(plots_path+"runtimes_fnn_btw25.pdf", bbox_inches='tight')
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
    print(f"Writing plot to {plots_path}runtimes_speedup_max_10000_btw25.pdf")
    plt.savefig(plots_path+"runtimes_speedup_max_10000_btw25.pdf", bbox_inches='tight')
    if args.show:
        plt.show()
    print("Done")