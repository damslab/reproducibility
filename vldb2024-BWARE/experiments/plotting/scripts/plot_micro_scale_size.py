import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

import plot_util as pu
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset


dis = pd.read_csv("results/MicroScaleSize/ccDistinct.log")
# fig_size = (2.7*2, 1.4/3 * 2*1.5)
_, ax = plt.subplots(1, 3, num=None, figsize=pu.fig_size,
        dpi=pu.dpi, facecolor="w", edgecolor="k")


ax[0].plot(dis["Distinct"], dis["Dense"], label="Dense", linestyle="-", linewidth=1)
ax[0].plot(dis["Distinct"], dis["MCSR"],  label="MCSR",  linestyle="--", linewidth=1)
ax[0].plot(dis["Distinct"], dis["COO"],   label="COO",   linestyle="-.", linewidth=1)
ax[0].plot(dis["Distinct"], dis["CSR"],   label="CSR",   linestyle=(0,(1,1)), linewidth=1)
ax[0].plot(dis["Distinct"], dis["Comp"],  label="DDC",   linestyle="-", linewidth=1)

ax[0].set_yscale('log', base=10)
ax[0].set_xscale('log', base=10)
pu.set_tics_y_log10(ax[0], 100, 1000000000000)
pu.set_tics_x_log10(ax[0], 1, 100000, 4)
ax[0].grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)
ax[0].set_ylabel("Size [B]", size= 8)
ax[0].set_xlabel("# Distinct", size= 8)
ax[0].xaxis.set_label_coords(0.5, -0.35)

ax[0].tick_params(axis="y",labelsize=7)
ax[0].tick_params(axis="x",labelsize=7)


axins = zoomed_inset_axes(ax[0], 4, loc="upper left")

axins.plot(dis["Distinct"], dis["Dense"], label="Dense", linestyle="-", linewidth=1)
axins.plot(dis["Distinct"], dis["MCSR"],  label="MCSR",  linestyle="--", linewidth=1)
axins.plot(dis["Distinct"], dis["COO"],   label="COO",   linestyle="-.", linewidth=1)
axins.plot(dis["Distinct"], dis["CSR"],   label="CSR",   linestyle=(0,(1,1)), linewidth=1)
axins.plot(dis["Distinct"], dis["Comp"],  label="DDC",   linestyle="-", linewidth=1)

axins.set_yscale('log', base=10)
axins.set_xscale('log', base=10)
x1, x2, y1, y2 = 200, 600, 5*10**6, 2*10**7
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.tick_params(labelsize=1)
axins.set_xticks([], minor=True)
axins.set_yticks([], minor=True)
for axis in ['top','bottom','left','right']:
    axins.spines[axis].set_linewidth(0.2)
axins.tick_params(width=0.2, size = 1)

mark_inset(ax[0], axins, loc1=3, loc2=1, 
            linewidth = 0.2, zorder = 3)




rows = pd.read_csv("results/MicroScaleSize/ccRows.log")

ax[1].plot((rows["Rows"]), rows["Dense"], label="Dense", linestyle="-", linewidth=1)
ax[1].plot((rows["Rows"]), rows["MCSR"],  label="MCSR",  linestyle="--",      linewidth=1)
ax[1].plot((rows["Rows"]), rows["COO"],   label="COO",   linestyle="-.",      linewidth=1)
ax[1].plot((rows["Rows"]), rows["CSR"],   label="CSR",   linestyle=(0,(1,1)), linewidth=1)
ax[1].plot((rows["Rows"]), rows["Comp"],  label="DDC",   linestyle="-",      linewidth=1)
ax[1].set_yscale('log', base=10)
ax[1].set_xscale('log', base=10)
ax[1].grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)
ax[1].set_xlabel("# Rows", size= 8)
pu.set_tics_y_log10(ax[1], 100, 100000000000)
pu.set_tics_x_log10(ax[1], 1, 100000,4)
ax[1].xaxis.set_label_coords(0.5, -0.35)

ax[1].tick_params(axis="y",labelsize=7)
ax[1].tick_params(axis="x",labelsize=7)


axins = zoomed_inset_axes(ax[1], 4, loc="upper left")

axins.plot((rows["Rows"]), rows["Dense"], label="Dense", linestyle="-", linewidth=1)
axins.plot((rows["Rows"]), rows["MCSR"],  label="MCSR",  linestyle="--",      linewidth=1)
axins.plot((rows["Rows"]), rows["COO"],   label="COO",   linestyle="-.",      linewidth=1)
axins.plot((rows["Rows"]), rows["CSR"],   label="CSR",   linestyle=(0,(1,1)), linewidth=1)
axins.plot((rows["Rows"]), rows["Comp"],  label="DDC",   linestyle="-",      linewidth=1)
axins.set_yscale('log', base=10)
axins.set_xscale('log', base=10)
x1, x2, y1, y2 = 200, 600, 2*10**4, 8*10**4
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.tick_params(labelsize=1)
axins.set_xticks([], minor=True)
axins.set_yticks([], minor=True)
for axis in ['top','bottom','left','right']:
    axins.spines[axis].set_linewidth(0.2)
axins.tick_params(width=0.2, size = 1)

mark_inset(ax[1], axins, loc1=3, loc2=1, 
            linewidth = 0.2, zorder = 3)



cols = pd.read_csv("results/MicroScaleSize/ccCols.log")

ax[2].plot((cols["Cols"]), cols["Dense"], label="Dense", linestyle="-", linewidth=1)
ax[2].plot((cols["Cols"]), cols["MCSR"],  label="MCSR",  linestyle="--",      linewidth=1)
ax[2].plot((cols["Cols"]), cols["COO"],   label="COO",   linestyle="-.",      linewidth=1)
ax[2].plot((cols["Cols"]), cols["CSR"],   label="CSR",   linestyle=(0,(1,1)), linewidth=1)
ax[2].plot((cols["Cols"]), cols["Comp"],  label="DDC",   linestyle="-",       linewidth=1)
ax[2].set_yscale('log', base=10)
ax[2].set_xscale('log', base=10)
ax[2].grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)
ax[2].set_xlabel("# Cols", size= 8)
ax[2].xaxis.set_label_coords(0.5, -0.35)
pu.set_tics_y_log10(ax[2], 100000, 100000000000000)
pu.set_tics_x_log10(ax[2], 1, 30000,4)


ax[2].legend(ncol=5, loc="upper center", bbox_to_anchor=(-1.0, 1.45),
              fontsize=7, markerscale= 0.6, handlelength =1.5,
              columnspacing= 0.8, handletextpad = 0.1)



ax[2].tick_params(axis="y",labelsize=7)
ax[2].tick_params(axis="x",labelsize=7)

axins = zoomed_inset_axes(ax[2], 4, loc="upper left")
axins.plot((cols["Cols"]), cols["Dense"], label="Dense", linestyle="-", linewidth=1)
axins.plot((cols["Cols"]), cols["MCSR"],  label="MCSR",  linestyle="--",      linewidth=1)
axins.plot((cols["Cols"]), cols["COO"],   label="COO",   linestyle="-.",      linewidth=1)
axins.plot((cols["Cols"]), cols["CSR"],   label="CSR",   linestyle=(0,(1,1)), linewidth=1)
axins.plot((cols["Cols"]), cols["Comp"],  label="DDC",   linestyle="-",       linewidth=1)
axins.set_yscale('log', base=10)
axins.set_xscale('log', base=10)
x1, x2, y1, y2 = 200, 600, 2*10**8, 8*10**8
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.tick_params(labelsize=1)
axins.set_xticks([], minor=True)
axins.set_yticks([], minor=True)
for axis in ['top','bottom','left','right']:
    axins.spines[axis].set_linewidth(0.2)
axins.tick_params(width=0.2, size = 1)

mark_inset(ax[2], axins, loc1=3, loc2=1, 
            linewidth = 0.2, zorder = 3)


plt.subplots_adjust(left=0.15, right=0.995, top=0.8,
                        bottom=0.28, wspace=0.45, hspace=0.35)
plt.savefig("plotting/plots/micro/Scale.pdf", dpi=1600)
plt.close()
