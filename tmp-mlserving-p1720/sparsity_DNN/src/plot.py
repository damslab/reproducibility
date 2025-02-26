import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import ast

plt.rcParams.update({'text.usetex': True
                            , 'pgf.rcfonts': False
                            , 'text.latex.preamble': r"""\usepackage{iftex}
                                            \ifxetex
                                                \usepackage[libertine]{newtxmath}
                                                \usepackage[tt=false]{libertine}
                                                \setmonofont[StylisticSet=3]{inconsolata}
                                            \else
                                                \RequirePackage[tt=false, type1=true]{libertine}
                                            \fi"""
                         })
fontsize = 26

df = pd.read_csv('~/llm_adapt_serving/data/artifacts/prunning_results_latency.csv', na_values=['None'])
df = df.fillna('None')

# Filter rows where z != "condition" for the line plot
filtered_df = df[df['model name'] != 'resnet50_original']

# Extract rows where z = "condition" for horizontal bars
condition_df = df[df['model name'] == 'resnet50_original']

original_latencies = condition_df['latency'].to_list()
original_latencies = [np.mean(np.array(ast.literal_eval(l))) for l in original_latencies]
baseline_latency = np.mean(original_latencies)

accuracy_per_subset = condition_df[['subset', 'accuracy']].set_index('subset').to_dict()['accuracy']
latency_per_subset = condition_df[['subset', 'latency']].set_index('subset').to_dict()['latency']

x_axis = [0.1, 0.2, 0.3, 0.4, 0.5]
fig, ax = plt.subplots(figsize=(8, 6))
for ids, subset in enumerate(filtered_df['subset'].unique()):
    # Plot the line plot
    # plt.figure(figsize=(10, 6))
    if subset == 'None':
        subset_df = filtered_df[filtered_df['subset'] == subset]
        subset_latencies = subset_df['latency'].to_list()
        subset_latencies = [np.mean(np.array(ast.literal_eval(l))) for l in subset_latencies]

        # baseline_latency = np.mean(original_latencies)
        ax.plot(x_axis, subset_latencies, marker='o', label='Pruned ResNet50', color='#d95f02')
        # flatten_axes[ids].set_title(subset)
        
        ax.set_ylabel('Latency [s]', fontsize=fontsize)
        ax.set_xlabel('Pruning Ratio', fontsize=fontsize)

        
        ax.axhline(y=baseline_latency, color='#7570b3', linestyle='--', alpha=1, label=f"Baseline ResNet50", linewidth=4)
        ax.tick_params(axis="x", labelsize=fontsize-5)  # Set x-tick font size  
        ax.tick_params(axis="y", labelsize=fontsize-5)  # Set y-tick font size  

        handles1, labels1 = ax.get_legend_handles_labels()
        # handles2, labels2 = ax2.get_legend_handles_labels()

        # Combine them
        handles = handles1
        labels = labels1

        # Move the legend above the plot
        # Add a combined legend to the figure
        fig.legend(handles, labels, loc="upper center", ncol=2, fontsize=fontsize-5, bbox_to_anchor=(0.53, 1.10))

        # plt.legend(fontsize=fontsize)
        # flatten_axes[-1].set_visible(False)
        # if m == 'latency':
        #     fig.suptitle('Pruning + Quantization - Batch size=512 - CPU only', fontsize=16)
        # plt.show()
        plt.tight_layout()
        plt.savefig(f"{'/Users/ricardosalazar/llm_adapt_serving/plots/latency_pruning'}.png", bbox_inches='tight')
        plt.savefig(f"{'/Users/ricardosalazar/llm_adapt_serving/plots/latency_pruning'}.svg", bbox_inches='tight')
        

####### Accuracy

df = pd.read_csv('~/llm_adapt_serving/data/artifacts/prunning_results_accuracy.csv', na_values=['None'])
df = df.fillna('None')
# Filter rows where z != "condition" for the line plot
filtered_df = df[df['model name'] != 'resnet50_original']

# Extract rows where z = "condition" for horizontal bars
condition_df = df[df['model name'] == 'resnet50_original']

# original_latencies = condition_df['latency'].to_list()
# original_latencies = [np.mean(np.array(ast.literal_eval(l))) for l in original_latencies]
# baseline_latency = np.mean(original_latencies)

accuracy_per_subset = condition_df[['subset', 'accuracy']].set_index('subset').to_dict()['accuracy']
latency_per_subset = condition_df[['subset', 'latency']].set_index('subset').to_dict()['latency']

fig, ax = plt.subplots(figsize=(8, 6))

colors = {'None': '#006837','animals': '#31a354', 'traffic': '#78c679'}
for ids, subset in enumerate(filtered_df['subset'].unique()):
    if subset in ['None', 'animals', 'traffic']:
        subset_df = filtered_df[filtered_df['subset'] == subset]
        accuracy = subset_df['accuracy'].to_numpy()
        baseline_accuracy = accuracy_per_subset[subset]
        ax.plot(x_axis, accuracy, marker='o', label=f'{subset} - Pruned ResNet50', color=colors[subset])

ax.set_ylabel('Accuracy', fontsize=fontsize)
ax.set_xlabel('Pruning Ratio', fontsize=fontsize)
ax.axhline(y=baseline_accuracy, color='#7570b3', linestyle='--', alpha=1, label=f"Baseline ResNet50", linewidth=4)

ax.tick_params(axis="x", labelsize=fontsize-5)  # Set x-tick font size  
ax.tick_params(axis="y", labelsize=fontsize-5)  # Set y-tick font size  

handles1, labels1 = ax.get_legend_handles_labels()
# handles2, labels2 = ax2.get_legend_handles_labels()

# Combine them
handles = handles1
labels = labels1

# Move the legend above the plot
# Add a combined legend to the figure
fig.legend(handles, labels, loc="upper center", ncol=2, fontsize=fontsize-5, bbox_to_anchor=(0.53, 1.16))

# plt.legend(fontsize=fontsize)
# flatten_axes[-1].set_visible(False)
# if m == 'latency':
#     fig.suptitle('Pruning + Quantization - Batch size=512 - CPU only', fontsize=16)
# plt.show()
plt.tight_layout()
plt.savefig(f"{'/Users/ricardosalazar/llm_adapt_serving/plots/accuracy_pruning'}.png", bbox_inches='tight')
plt.savefig(f"{'/Users/ricardosalazar/llm_adapt_serving/plots/accuracy_pruning'}.svg", bbox_inches='tight')