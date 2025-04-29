import pandas as pd
import plot_util as pu
import math
import matplotlib.pyplot as plt
import numpy as np

import os
mx = 1
mi = 1000000000


def parse(path):
    ids = []
    distinct = []
    time = []

    for i in range(40):
        distinct.append([])
        time.append([])
        ids.append([])
    if os.path.exists(path):
        with open(path) as f:
            for l in f:
                if   "DEBUG encode.CompressedEncode: Encode: columns:" in l:

                    col = int(l[67:71])-1

                    sp = l.split(" distinct: ")[1].split(" time: ")
                    if len(distinct[col]) == 0:
                        distinct[col].append(int((sp[0].split(" size:")[0])))
                        ids[col].append(col)
                    time[col].append(float(sp[1]))

    def stat(data):
        ret = []
        st = []
        for x in data:
            x.sort()
            x = x[3:-3] ## Remove outliers top and bottom
            st.append(np.std(x))
            ret.append(np.mean(x))
        return [[x,y] for x,y  in zip(ret, st)]
        
    stats = stat(time)

    data =[ x + y + z for x,y, z in  zip(distinct, ids, stats)]

    return data

sizes = [100000, 1000000, 10000000, 100000000]
names = ["100K", "1M", "10M", "100M"]
# f1 = "results/otherSystems/dams-su1/def/criteo_full-criteo-day_0_100000.tsv-TAWAb16.log"
fig_size = (3.33, 0.8)


fig, axi = plt.subplots(
        1,
        len(sizes),
        num=None,
        figsize=fig_size,
        dpi=pu.dpi,
        facecolor="w",
        edgecolor="k",
    )
mx = 1
mi = 1000000000

# f1 = "results/otherSystems/dams-su1/def/criteo_full-criteo-day_0_100000.tsv-TAWAb16.log"

for id, ax in enumerate(axi):
    base = "results/otherSystems/dams-su1/def/criteo_full-criteo-day_0_"
    end = ".tsv-TAWAb16.log"
    end_compressed = ".tsv.cla-TAWAb16.log"
    compressing = parse(base + str(sizes[id]) + end )
    compressed  = parse(base + str(sizes[id]) + end_compressed )

    combined = [x + y for x, y in zip(compressing, compressed)]

    combined = sorted(combined, key = lambda x : x[6])

    compressing = [[x[0],x[1], x[2], x[3]] for x in combined]
    compressed = [[x[4],x[5], x[6], x[7]] for x in combined]

    compressing_times = [x[2] for x in compressing]
    compressing_err = [x[3] for x in compressing]
    for i in range(len(compressing_err)):
        while compressing_times[i] - compressing_err[i] < 0:
            compressing_err[i] *= 0.8
    mi = min(min(compressing_times), mi)
    mx = max(max(compressing_times), mx)
    ax.bar(range(len(compressing)), height = compressing_times, color ="tab:orange", label = "Uncompressed",)
    ax.errorbar(range(len(compressing)), compressing_times, color ="black", alpha=0.6,
                 yerr = compressing_err,elinewidth=0.2, ls='none')

    compressed_times = [x[2] for x in compressed]
    compressed_err = [x[3] for x in compressed]
    for i in range(len(compressed_err)):
        while compressed_times[i] - compressed_err[i] < 0:
            compressed_err[i] *= 0.8
    mi = min(min(compressed_times), mi)
    mx = max(max(compressed_times), mx)
    ax.bar(range(len(compressed)),  compressed_times,color =   "tab:brown", label = "Compressed")
    ax.errorbar(range(len(compressed)), compressed_times, color =   "black", alpha=0.6,
                yerr = compressed_err, elinewidth=0.2 , ls='none')
    ax.text(
                0.94,
                0.06,
                names[id],
                bbox=dict(boxstyle="square", pad=0.1, fc="w", ec="k", lw=0.1),
                # rotation=90,
                size=6,
                ha="right",
                va="bottom",
                transform=ax.transAxes,
    )


for id, ax in enumerate(axi):
    ax.set_xticks([])
    ax.set_yscale("log", base=10)
    ax.tick_params(axis="y", labelsize=7)
    ytics = pu.set_tics_y_log10(ax, mi * 0.1, mx * 1.4)
    if id == 0:
        ax.set_ylabel("Time [ms]", size=8)
        ax.yaxis.set_label_coords(-0.4, 0.5)
    else:
        ax.set_yticklabels(["" for x in range(len(ytics))])
    ax.tick_params(axis="x", pad=-0.06)
axi[0].tick_params(axis="y", pad=-0.06)

handles, labels = axi[0].get_legend_handles_labels()

plt.legend(handles,labels,
        loc="lower center",
        bbox_to_anchor=(-1.35, 0.96),
               fontsize=6.3,
        markerscale=0.6,
        ncol = 4,
        handlelength=1.5,
        columnspacing=0.8,
        handletextpad=0.1,
        frameon= True
        )
plt.subplots_adjust(
        left=0.12, right=0.99, top=0.78, bottom=0.01, wspace=0.17, hspace=0.30
)

out  ="plotting/plots/breakdownTime-su1.pdf"
print("Script","plotting/scripts/plot_28_transformEncodeBreakdown.py","out", out)
plt.savefig(out)