import pandas as pd
import matplotlib.pyplot as plt
import math
import plot_util as pu


plt.rcParams["axes.unicode_minus"]= True

# def plot(name):
	
fig, ax = plt.subplots(1, 2, num=None, figsize=((3.33*2 + 0.1) / 3, 0.8),
      dpi=pu.dpi, facecolor="w", edgecolor="k")
# marker='o'
# # markersize=0.01
for id, name in enumerate(["crypto","santander"]):
	dis = pd.read_csv("results/lossy_binning/"+name+"_equi_width.csv", header=None)
	ax[id].plot(dis[0], dis[3]*100,  label="Equi-width",  linestyle="-", linewidth=1, alpha = 0.7)
	ax[id].fill_between(dis[0], dis[1]*100, dis[2]*100, alpha=0.3)
	dis = pd.read_csv("results/lossy_binning/"+name+"_equi_height.csv", header=None)
	ax[id].plot(dis[0], dis[3]*100,  label="Equi-height",  linestyle="--", linewidth=1, alpha = 0.7)
	ax[id].fill_between(dis[0], dis[1]*100, dis[2]*100, alpha=0.3)
	# ax.set_ylim(0, max(dis[3]))
	ax[id].set_yscale('log', base=10)
	ax[id].set_xscale('log', base=10)
	# # ax.set_xscale('log', base=2)
	ytics = pu.set_tics_y_log10(ax[id], 0.01, 110, 6)
	ax[id].set_xticks([1,10,100,1000])
	ax[id].tick_params(axis="y",labelsize=7)
	ax[id].tick_params(axis="x",labelsize=7)
	if(id == 0):
		ax[id].set_ylabel("MAE", size= 8 )
		ax[id].yaxis.set_label_coords(-0.21, 0.5)
		ax[id].set_yticklabels(["$10^{^{\u20102}}$","","$10^{^{0}}$", "", "$10^{^{2}}$"])
	else:
		ax[id].set_yticklabels(["" for x in range(len(ytics))])

	ax[id].xaxis.set_label_coords(0.5, -0.35)
	ax[id].set_xmargin(0)
	ax[id].text(0.02,0.04, name.capitalize(), 
			 bbox=dict(boxstyle="square",pad=0.1, fc="w", ec="k", lw=0.1),
	
				 rotation=0,size=6, ha="left", va="bottom",transform=ax[id].transAxes)
	ax[id].grid(True, "major", axis='both', ls='--', linewidth=0.3, alpha=1.0)
	ax[id].grid(True, "minor", axis="y", ls="dotted", linewidth=0.2, alpha=0.9)
   
ax[1].legend(ncol=5, loc="upper center", bbox_to_anchor=(0.0, 1.53),
	              fontsize=6)

fig.text(0.50,0,"# Bins", size=8)
for i in [0,1]:
    ax[i].tick_params(axis="x", pad=-0.06)
    ax[i].tick_params(axis="y", pad=-0.06)

plt.subplots_adjust(left=0.13, right=0.995, top=0.78,
	                        bottom=0.29, wspace=0.15, hspace=0.35)
plt.savefig("plotting/plots/micro/lossyBinning_combined.pdf", dpi=1600)
plt.close()
print("script:","plotting/scripts/plot_lossy_binning.py", "out:", "plotting/plots/micro/lossyBinning_combined.pdf")
