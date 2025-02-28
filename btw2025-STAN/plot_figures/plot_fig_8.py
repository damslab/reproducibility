import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
custom_palette = sns.color_palette("light:#5A9")


custom_cmap = ListedColormap(custom_palette)

palette = sns.light_palette("#5A9", n_colors=4)
reversed_palette = list(reversed(palette))
try:
    acf_stan_ucr_results = np.loadtxt(os.path.join("results", "stan_ucr_results.txt"))
    mwf_ucr_results = np.loadtxt(os.path.join("results", "stan_ucr_results_mwf.txt"))
    fourier_ucr_results = np.loadtxt(os.path.join("results", "stan_ucr_results_dominant_fourier_freq.txt"))
except:
    print("UCR results are not complete.")
    print("Run stan.py alternatives to generate the ucr results.")
    exit()

data = {"ACF": np.mean(acf_stan_ucr_results), "MWF": np.mean(mwf_ucr_results), "FFT": np.mean(fourier_ucr_results)}
df123 = pd.DataFrame(list(data.items()), columns=['Method', 'Accuracy'])
plt.figure(figsize=(5, 3))
sns.barplot(x="Method", y = "Accuracy", palette = reversed_palette, data = df123)
plt.xlabel("") 
plt.ylabel('UCR Score', fontsize = 13)
plt.tight_layout()
plt.savefig(os.path.join("results", "figures", "fig_8.png"))
plt.show()
