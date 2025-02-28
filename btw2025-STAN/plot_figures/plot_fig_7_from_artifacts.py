import sqlite3
import pandas as pd
import seaborn as sns
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

custom_palette = sns.color_palette("light:#5A9")

custom_cmap = ListedColormap(custom_palette)

palette = sns.light_palette("#5A9", n_colors=12)
reversed_palette = list(reversed(palette))


# Connect to the SQLite database
conn = sqlite3.connect(os.path.join("artifacts", "mlflow.sqlite"))

# SQL query
query = """
SELECT
    r.start_time,
    r.end_time,
    p.value AS model_name,
    t1.value AS run_id,
    t2.value AS timeseries,
    m1.value AS auroc,
    m2.value AS f1,
    m3.value AS ucr_score
FROM runs r
LEFT JOIN params p ON r.run_uuid = p.run_uuid AND p.key = 'model.name'
LEFT JOIN tags t1 ON r.run_uuid = t1.run_uuid AND t1.key = 'run_id'
LEFT JOIN tags t2 ON r.run_uuid = t2.run_uuid AND t2.key = 'timeseries'
LEFT JOIN metrics m1 ON r.run_uuid = m1.run_uuid AND m1.key = 'auroc'
LEFT JOIN metrics m2 ON r.run_uuid = m2.run_uuid AND m2.key = 'f1'
LEFT JOIN metrics m3 ON r.run_uuid = m3.run_uuid AND m3.key = 'ucr score'
WHERE r.status = 'FINISHED';
"""

# Execute the query and load results into a DataFrame
df = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

def parse_duration(df: pd.DataFrame, outcolumn="seconds"):
    df["start_time"] = pd.to_datetime(df["start_time"], utc=True).astype('int64')
    df["end_time"] = pd.to_datetime(df["end_time"], utc=True).astype('int64')
    df[outcolumn] = (df["end_time"] - df["start_time"]) / 1000

parse_duration(df)

grouped_df = df.groupby(['run_id', 'model_name'])["seconds"].mean().groupby('model_name').mean().reset_index()

stan_time_results = np.loadtxt(os.path.join("results", "stan_exec_time.txt"))
merlin_time_results = np.loadtxt(os.path.join("results", "merlin_exec_time.txt"))
grouped_df = pd.concat([grouped_df, pd.DataFrame({"run_id": [1, 1], "model_name": ["STAN", "MERLIN"], "seconds": [stan_time_results[1], merlin_time_results[1]]})])


plt.figure(figsize=(10, 5))
sns.barplot(x='model_name', y='seconds', palette = reversed_palette, data=grouped_df)
plt.xticks(fontsize = 11.5)
plt.xlabel('')
plt.ylabel('Execution Time', fontsize = 11.5)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join("results", "figures", "fig_7.png"))
plt.show()
