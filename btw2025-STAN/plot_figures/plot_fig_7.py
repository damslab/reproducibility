"""
SPDX-FileCopyrightText: 2022 German Aerospace Center, Ferdinand Rewicki

SPDX-License-Identifier: Apache-2.0
"""
# We slighly modified this utsadbench code snippet to read the results from the mlflow tracking server.

import mlflow
import pathlib
import seaborn as sns
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from typing import List
from matplotlib.colors import ListedColormap

custom_palette = sns.color_palette("light:#5A9")

custom_cmap = ListedColormap(custom_palette)

palette = sns.light_palette("#5A9", n_colors=12)
reversed_palette = list(reversed(palette))


DATASET_BASEPATH  = './data/ucraa'
TRACKING_SERVER_URL = 'http://localhost:5000'

def parse_duration(df: pd.DataFrame, outcolumn="seconds"):
    df["start_time"] = pd.to_datetime(df["start_time"], utc=True).astype('int64')
    df["end_time"] = pd.to_datetime(df["end_time"], utc=True).astype('int64')
    df[outcolumn] = (df["end_time"] - df["start_time"]) / 1e9
    
    return df

def add_ts_length_data(df: pd.DataFrame, datapath: str):
    timeseries = {}
    for file in pathlib.Path(datapath).glob(f'*.txt'):
        parts = file.as_posix().split('/')[-1].split('.')[0].split('_')

        name = f'{parts[0]}_{parts[1]}_{parts[3]}'
        normal_until = int(parts[4])
        anomaly_start = int(parts[5])
        anomaly_end = int(parts[6])

        data = np.loadtxt(file.as_posix())

        timeseries[name] = {
            "full": file.as_posix().split('/')[-1], 
            "tags.timeseries": name,
            "length": data.shape[0],
            "anomaly length": (anomaly_end - anomaly_start + 1),
            #"data": data
        }
    timeseries_df = pd.DataFrame.from_dict(timeseries).transpose()
    df_with_tsdata = pd.merge(df, timeseries_df, on="tags.timeseries", how="inner")
    
    return df_with_tsdata, timeseries_df


mlflow.set_tracking_uri(TRACKING_SERVER_URL)
df = mlflow.search_runs(experiment_names=["MDI", "RRCF", "AE", "GANF", "TRANAD"], filter_string="attributes.status = 'FINISHED'")
df = df[["start_time", "end_time", "params.model.name", "tags.run_id", "tags.timeseries", "metrics.auroc", "metrics.f1", "metrics.ucr score"]]
df = parse_duration(df)
df, length_df = add_ts_length_data(df, DATASET_BASEPATH)
df = df.rename(columns={
        "metrics.auroc": "AUC ROC",
        "metrics.f1": "F1 Score",
        "metrics.ucr score": "UCR Score",
    })


# fig = grouped_bar_chart(df, "params.model.name", bars=df["params.model.name"].unique(), xticks=metrics, colors=colors, width=700, height=450, errorbars=True)
grouped_df = df.groupby(['tags.run_id', 'params.model.name'])["seconds"].mean().reset_index()
try:
    stan_ucr_results = np.loadtxt(os.path.join("results", "stan_exec_time.txt"))
except:
    print("Stan UCR results are not complete. Run python stan_alone/stan.py to generate the ucr results.")
    exit()

try:
    merlin_ucr_results = np.loadtxt(os.path.join("results", "merlin_exec_time.txt"))
except:
    print("Merlin UCR results are not complete. Run python merlin_alone/merlin.py to generate the ucr results.")
    exit()

if stan_ucr_results.shape[0] != 250:
    print("Stan UCR results are not complete.")
    print("File has been corrected")
    exit()

if merlin_ucr_results.shape[0] != 250:
    print("Merlin UCR results are not complete.")
    print("Run merlin.py to generate the ucr results.")
    exit()
    
grouped_df = pd.concat([grouped_df, pd.DataFrame({"tags.run_id": [1, 1], "params.model.name": ["STAN", "MERLIN"], "seconds": [stan_ucr_results.mean(), merlin_ucr_results.mean()]})])


plt.figure(figsize=(10, 5))
sns.barplot(x='params.model.name', y='seconds', palette = reversed_palette, data=grouped_df)
plt.xticks(fontsize = 11.5)
plt.xlabel('')
plt.ylabel('Execution Time', fontsize = 11.5)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join("results", "figures", "fig_7.png"))
plt.show()

