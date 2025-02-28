import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import seaborn as sns
import os
from matplotlib.colors import ListedColormap
custom_palette = sns.color_palette("light:#5A9")

custom_cmap = ListedColormap(custom_palette)

statistics: list[str] = ['std', 'min', 'max', 'kurtosis', 'skew', 'point_anomaly', 'count_direction_changes', 'mean']


def collect_statistic_results(statistics):
    try:
        statistic_results = np.loadtxt(os.path.join("results", f"stan_ucr_results_{'_'.join(statistics)}.txt"))
    except:
        print(f"UCR results for {'_'.join(statistics)} are not complete.")
        print("Run stan.py aggregates to generate the ucr results.")
        exit()
    return {'statistics': f'+{statistics[-1]}', 'ucr': np.mean(statistic_results)}
    
if __name__ == '__main__':
    all_results = pd.DataFrame()

    for i in range(1, len(statistics)+1):
        statistics_ucr = collect_statistic_results(statistics[:i])
        all_results = pd.concat([all_results, pd.DataFrame(statistics_ucr)], axis=1)
        

    all_results.set_index("statistics", inplace=True)
    plt.figure(figsize=(4, 7))
    hi = sns.barplot(all_results)
    hi.set_ylabel('UCR Score')
    plt.tight_layout()
    plt.savefig(os.path.join("results", "figures", "fig_6.png"))
    plt.show()


