import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plot_util as pu

from matplotlib.colors import LinearSegmentedColormap
from threading import Thread

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

import os

G_data = None
G_cards = None

def cardinalities(data):
    cards = np.zeros((len(data.columns), len(data.columns)), dtype=np.float64)
    for ic, c in enumerate(data.columns):
        for icc, cc in enumerate(data.columns):
            if ic < icc:
                continue
            v = data.groupby([c, cc]).size().shape[0]

            cards[ic, icc] = v
            cards[icc, ic] = v

    for ic, c in enumerate(data.columns):
        for icc, cc in enumerate(data.columns):
            if ic == icc:
                continue
            if ic < icc:
                continue

            m = cards[ic, ic] + cards[icc, icc]
            v = cards[ic, icc] * 2 / (m)
            # print(cards[icc,icc], cards[ic,ic],  cards[ic, icc], m, v)
            # print(v)
            cards[icc, ic] = v
            cards[ic, icc] = v

    for ic, c in enumerate(data.columns):
        cards[ic, ic] = 1
    return cards


def bool_card(ic, c):
    for icc, cc in enumerate(G_data.columns):
        if ic < icc:
            continue
        if int(c.split("_")[0]) == int(
            cc.split("_")[0]
        ):  # prefix same aka same original column.
            G_cards[icc, ic] = 2
            G_cards[ic, icc] = 2
        else:
            v = G_data.groupby([c, cc]).size().shape[0]
            G_cards[ic, icc] = v
            G_cards[icc, ic] = v

    print("Done:", str(ic))


def boolean_cardinality(data):
    cards = G_cards
    P = []
    for ic, c in enumerate(data.columns):
        p = Thread(target=bool_card, args=(ic, c))
        p.start()
        P.append(p)
        # if(ic > 150):
        #     break;
    for p in P:
        p.join()

    for ic, c in enumerate(data.columns):
        for icc, cc in enumerate(data.columns):
            if ic == icc:
                continue
            if ic < icc:
                continue
            m = cards[ic, ic] + cards[icc, icc]
            v = cards[ic, icc] * 2 / (m)
            cards[icc, ic] = v
            cards[ic, icc] = v

    for ic, c in enumerate(data.columns):
        cards[ic, ic] = 1
    return cards


def one_hot(data):
    names = []
    for ic, c in enumerate(data.columns):
        names.append(c)

    for c in names:
        hot = pd.get_dummies(data[c], prefix=c)
        print("Column HotSize: ", c, hot.shape[1])
        # print(hot)
        data = data.drop(c, axis=1)
        data = data.join(hot)
        # print("hot: " + str(c))
    return data


adult = pd.read_csv("data/adult/adult.csv", header=None)

# print(adult)
# print(adult.columns)
adult = adult.drop([2], axis=1)

cards = cardinalities(adult)

if os.path.exists("tmp/adultOneHotCorr.npy") :
    cards_hot = np.load("tmp/adultOneHotCorr.npy")
else:
    adult_hot = one_hot(adult)
    G_data = adult_hot
    G_cards = np.ones((len(adult_hot.columns), len(adult_hot.columns)), dtype=np.float64)*2
    cards_hot = boolean_cardinality(adult_hot)
    np.save("tmp/adultOneHotCorr", cards_hot)

_, ax = plt.subplots(
    1, 2, num=None, figsize=pu.fig_size, dpi=pu.dpi, facecolor="w", edgecolor="k"
)

cmapBlue = LinearSegmentedColormap.from_list("cold", ["white", (42/256,186/256,212/256)], N=5000)
cmaphot = LinearSegmentedColormap.from_list("cold", ["white", (42/256,186/256,212/256), "tab:orange", (196/256, 13/256, 30/256)], N=5000)

im = ax[0].imshow(cards, origin="lower",  interpolation  ="none", cmap=cmaphot, norm="log")
ax[0].set_yticks([cards.shape[0]-1])
ax[0].set_yticklabels([cards.shape[0]])
ax[0].set_xticks([])
ax[0].tick_params(axis="y",labelsize=7)
ax[0].tick_params(axis="x",labelsize=7)
ax[0].set_ylabel("Original", size=8)
ax[0].yaxis.set_label_coords(-0.01, 0.4)
cb = plt.colorbar(im)
cb.ax.tick_params(axis="y",labelsize=7)
im = ax[1].imshow(cards_hot, origin="lower", interpolation  ="none", cmap=cmapBlue)

axins = zoomed_inset_axes(ax[1], 4, loc="lower right") 
axins.imshow(cards_hot, interpolation="none", origin="lower", cmap=cmapBlue)

for spine in axins.spines.values():
    spine.set_edgecolor("tab:orange")
    spine.set_linewidth(0.5)

x1, x2, y1, y2 = 75, 125, 75, 125
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_xticks([])
axins.set_yticks([])

plt.xticks(visible=False)
plt.yticks(visible=False)

mark_inset(ax[1], axins, loc1=2, loc2=3, fc="none", linewidth = 1.0, color="tab:orange")

ax[1].set_yticks([cards_hot.shape[0]-1])
ax[1].set_yticklabels([cards_hot.shape[0]])
ax[1].set_xticks([])
ax[1].tick_params(axis="y",labelsize=7)
ax[1].tick_params(axis="x",labelsize=7)
ax[1].set_ylabel("One-Hot", size=8)
ax[1].yaxis.set_label_coords(-0.01, 0.45)
cb = plt.colorbar(im)
cb.ax.tick_params(axis="y",labelsize=7)
cb.ax.set_yticks([1.0, 1.5, 2.0])
cb.ax.set_ylabel("Distinct scaling", size=7)



plt.subplots_adjust(left=-0.05, right=0.93, top=0.94,
	                        bottom=0.05, wspace=0.05, hspace=0.35)

plt.savefig("plotting/plots/micro/correlation.pdf")
