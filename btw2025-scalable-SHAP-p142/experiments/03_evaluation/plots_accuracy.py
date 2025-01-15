#!/usr/bin/env python
# coding: utf-8

# # Compute Accuracy of linear models

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import shap
import sklearn as sk
import sklearn.metrics
from joblib import load

import argparse
parser=argparse.ArgumentParser(description="Plot runtime graphs..")
parser.add_argument("--data-dir", default="../10_data/", help="Path to dir where runtimes are stored.")
parser.add_argument("--plots-path", default="../10_results/", help="Path to dir where resulting plots should be stored.")
parser.add_argument("--max-computations", default="100", help="Max Computations used during accuracy experiment.")
parser.add_argument('--show', action='store_true', help='Try to display plots during computation.')
args=parser.parse_args()

# In[16]:

data_dir = args.data_dir
max_computations = int(args.max_computations)

print(f"Loading data from {data_dir}")
# load prepared data into dataframe
data_adult_x = pd.read_csv(data_dir+"adult/Adult_X.csv", header=None)
data_adult_y = pd.read_csv(data_dir+"adult/Adult_y.csv", header=None)

data_census_x = pd.read_csv(data_dir+"census/Census_X.csv", header=None)
data_census_y = pd.read_csv(data_dir+"census/Census_y_corrected.csv", header=None)

# In[17]:
print("Preparing LinearExplainer for comparison")
# load/create models for LinearExplainer
multiLinLogReg = load(data_dir+"adult/models/multiLogReg.joblib")
svm_coef = np.genfromtxt(data_dir+"census/models/Census_SVM.csv", delimiter=',')

# In[18]:
print("Computing SHAP values with LinearExplainer")
# linear explainer
explainer_multiLinLogReg_inter = shap.explainers.LinearExplainer(multiLinLogReg,data_adult_x)
explainer_svm_inter = shap.explainers.LinearExplainer((svm_coef,0),data_census_x)

# In[19]:

# compute shap values using linear explainer
adult_shap_values = explainer_multiLinLogReg_inter(data_adult_x.iloc[0:50])
census_shap_values = explainer_svm_inter(data_census_x.iloc[0:50])

# In[20]:

# transform from logit to probabilities

# Function to transform log-odds SHAP values to probability space
def logit_to_prob(logit):
    return 1 / (1 + np.exp(-logit))

# Function to transform log-odds SHAP values to probability space
def transform_logit_proba(model, shap_values_logit, base_logit):
    # Apply the transformation to align SHAP values
    aligned_shap_values = []
    for i in range(len(shap_values_logit)):
        instance_shap_values = shap_values_logit[i]
        new_probs = logit_to_prob(base_logit + instance_shap_values) - logit_to_prob(base_logit)
        aligned_shap_values.append(new_probs)
    return np.array(aligned_shap_values)


# In[21]:
print("Transforming to probabilities")
# Compute base logit (mean logit of the background data)
base_logit = np.mean(multiLinLogReg.decision_function(data_adult_x))
adult_shap_values_proba = transform_logit_proba(multiLinLogReg, adult_shap_values.values, base_logit)

print(f"Saving values from linear explainer to {data_dir}accuracy/shap-values_permutation_linear_adult.csv")
pd.DataFrame(adult_shap_values_proba).to_csv(data_dir+"accuracy/shap-values_permutation_linear_adult.csv", index=False)
pd.DataFrame(census_shap_values.values).to_csv(data_dir+"accuracy/shap-values_permutation_linear_census.csv", index=False)

# In[22]:

print(f"Loading shape values from large baseline at:")
print(data_dir+"accuracy/shap-values_permutation_large_adult_linlogreg_python.csv")
print(data_dir+"accuracy/shap-values_permutation_large_census_l2svm_python.csv")
#load large python
adult_vals_large = np.genfromtxt(data_dir+"accuracy/shap-values_permutation_large_adult_linlogreg_python.csv", delimiter=',', skip_header=1)
census_vals_large = np.genfromtxt(data_dir+"accuracy/shap-values_permutation_large_census_l2svm_python.csv", delimiter=',', skip_header=1)

# In[23]:

#row wise mse
def rowwise_mse(array1, array2):
    # Ensure the arrays have the same shape
    if array1.shape != array2.shape:
        raise ValueError("Both arrays must have the same shape")

    # Compute the squared differences
    squared_differences = (array1 - array2) ** 2

    # Compute the mean of the squared differences for each row
    return np.mean(squared_differences)


# In[24]:

def create_row_inter_mse(exp_type, permutations, samples, sysds_vals, python_vals, shap_vals, large_vals):
    data_row = {
        'exp_type': exp_type,
        'permutations': permutations,
        'samples': samples,
        'total': samples*permutations,
        'mse_systemds_linear': rowwise_mse(sysds_vals,shap_vals),
        'mse_python_linear': rowwise_mse(python_vals,shap_vals),
        'mse_systemds_python': rowwise_mse(sysds_vals,python_vals),
        'mse_systemds_large': rowwise_mse(sysds_vals,large_vals),
        'mse_python_large': rowwise_mse(python_vals,large_vals)
    }
    return data_row

# In[25]:

def load_systemds_vals(permutations, samples, exp_type, n):
    sysds_vals = None
    for i in range(n):
        try:
            sysds_vals_tmp = np.genfromtxt(f'{data_dir}accuracy/systemds/shap-values_permutation_{permutations}perm_{samples}samples_{exp_type}_systemds_{i+1}.csv', delimiter=',')
        except FileNotFoundError as e:
            print(f"File {data_dir}accuracy/systemds/shap-values_permutation_{permutations}perm_{samples}samples_{exp_type}_systemds_{i+1}.csv not found! Skipping...")
            continue
        
        if sysds_vals is None:
            sysds_vals = sysds_vals_tmp
        else:
            sysds_vals = sysds_vals + sysds_vals_tmp
    
    if sysds_vals is not None: sysds_vals = sysds_vals / n
    
    return sysds_vals


def load_python_vals(permutations, samples, exp_type, n):
    python_vals = None
    for i in range(n):
        try:
            python_vals_tmp = np.genfromtxt(f'{data_dir}accuracy/python/shap-values_permutation_{permutations}perm_{samples}samples_{exp_type}_python_{i+1}.csv', delimiter=',', skip_header=1)
        except FileNotFoundError as e:
            print(f"File {data_dir}accuracy/python/shap-values_permutation_{permutations}perm_{samples}samples_{exp_type}_systemds.csv not found! Skipping...")
            continue

        if python_vals is None:
            python_vals = python_vals_tmp
        else:
            python_vals = python_vals + python_vals_tmp
    if python_vals is not None: python_vals = python_vals / n
    return python_vals


def load_vals(permutations, samples, exp_type, n):
    return load_systemds_vals(permutations, samples, exp_type, n), load_python_vals(permutations, samples, exp_type, n)

# In[26]:

# iterate through csvs with shap values and compute average MSE for each combination of permutations and samples
print("Loading vals from systemds and python to compute MSE.")
new_rows=[]

exp_types = ['census_l2svm', 'adult_linlogreg']
for exp_type in exp_types:
    permutations = 10
    samples = 100
    sysds_vals, python_vals = load_vals(permutations, samples, exp_type, max_computations)
    
    if sysds_vals is None or python_vals is None:
        print("There was an error during loading of shap values from files.")
    
    shap_vals=None
    large_vals=None
    if exp_type == 'adult_linlogreg':
        shap_vals = np.genfromtxt(data_dir+"accuracy/shap-values_permutation_linear_adult.csv", delimiter=',', skip_header=1)
        large_vals = adult_vals_large
    else:

        shap_vals = np.genfromtxt(data_dir+"accuracy/shap-values_permutation_linear_census.csv", delimiter=',', skip_header=1)
        large_vals = census_vals_large
    
    row = create_row_inter_mse(exp_type, permutations, samples, sysds_vals, python_vals, shap_vals, large_vals)
    
    new_rows.append(row)

data_convergence = pd.DataFrame(new_rows)

# In[28]:

# dataset metrics
d_adult = data_convergence[data_convergence.exp_type=='adult_linlogreg'].sort_values(by=['total']).drop(columns=['exp_type'])
d_census = data_convergence[data_convergence.exp_type=='census_l2svm'].sort_values(by=['total']).drop(columns=['exp_type'])

adult_sysds_vals, adult_python_vals = load_vals(10, 100, 'adult_linlogreg', max_computations)
census_sysds_vals, census_python_vals = load_vals(10, 100, 'census_l2svm', max_computations)

print(f"Writing MSEs to {args.plots_path}mse_results.txt")
with open(args.plots_path+"mse_results.txt", "w") as file:
    file.write('Errors for our method and python method\n\n')
    file.write('============= ADULT ============\n')
    file.write('Shap values metrics:\n')
    file.write(f'Max: {abs(adult_sysds_vals).max():.2f} Mean: {abs(adult_sysds_vals).mean():.2f}\n')
    file.write('====== MSE =====================\n')
    file.write(' --> Our Method\n')
    file.write(f'exact ground truth: {d_adult[d_adult.samples == 100].mse_systemds_linear.mean():.2e}\n')
    file.write(f'large ground truth: {d_adult[d_adult.samples == 100].mse_systemds_large.mean():.2e}\n')
    file.write(' --> Python\n')
    file.write(f'exact ground truth: {d_adult[d_adult.samples == 100].mse_python_linear.mean():.2e}\n')
    file.write(f'large ground truth: {d_adult[d_adult.samples == 100].mse_python_large.mean():.2e}\n')
    file.write(' --> Ours vs. Python\n')
    file.write(f'sysds - python: {d_adult[d_adult.samples == 100].mse_systemds_python.mean():.2e}\n')
    file.write('\n')
    file.write('============= CENSUS ===========\n')
    file.write('Shap values metrics:\n')
    file.write(f'Max: {abs(census_sysds_vals).max():.2f} Mean: {abs(census_sysds_vals).mean():.2f}\n')
    file.write('====== MSE =====================\n')
    file.write(' --> Our Method\n')
    file.write(f'large ground truth: {d_census[d_census.samples == 100].mse_systemds_large.mean():.2e}\n')
    file.write(' --> Python\n')
    file.write(f'large ground truth: {d_census[d_census.samples == 100].mse_python_large.mean():.2e}\n')

# In[15]:

font = {'size': 14}

matplotlib.rc('font', **font)

# load data
adult_sysds_vals, adult_python_vals = load_vals(10, 100, 'adult_linlogreg', max_computations)

t_adult_exact = np.genfromtxt(data_dir+"accuracy/shap-values_permutation_linear_adult.csv", delimiter=',', skip_header=1)[1]
t_adult_sysds = adult_sysds_vals[1]
t_adult_python = adult_python_vals[1]

# Create a figure and a single subplot
fig, ax1 = plt.subplots(figsize=(8, 4))

# Define the positions of the bars
bar_width = 0.3
index = np.arange(len(t_adult_sysds))
ax1.bar(index - bar_width, t_adult_sysds, bar_width, label='Parallel')

ax1.bar(index, t_adult_python, bar_width, label='Python')

ax1.bar(index+bar_width, t_adult_exact, bar_width, label='Exact')
# Reduce the number of y-ticks
ax1.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=10))

#text for mse
mse_sysds = np.mean((t_adult_sysds - t_adult_exact) ** 2)
mse_python = np.mean((t_adult_python - t_adult_exact) ** 2)
ax1.text(1, -0.12, f'MSE Parallel: {mse_sysds:.1e}\nMSE Python: {mse_python:.1e}',multialignment='right', fontsize=12)

#limits
ax1.set_xlim(-1,67)

# Set labels and title
ax1.set_xlabel('Feature Index')
ax1.set_ylabel('SHAP Values')
ax1.legend(ncol=2, prop={'size': 12})


# Show the plot
fig.tight_layout()
print(f"Writing plot to {args.plots_path}Fig3_accuracy_example_adult_btw25.pdf")
fig.savefig(args.plots_path+"Fig3_accuracy_example_adult_btw25.pdf", bbox_inches='tight')
if args.show:
    plt.show()

