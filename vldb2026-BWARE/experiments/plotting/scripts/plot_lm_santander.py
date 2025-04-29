import matplotlib.pyplot as plt
import plot_util as pu
import numpy as np
import pandas as pd
import os


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

mkdir("./plotting/plots")
mkdir("./plotting/plots/lm/")
mkdir("./plotting/plots/lm/santander")


def plot(d1, name):

    fig_size = (4.2, 1.5)
    _, ax = plt.subplots(
        1, 3, num=None, figsize=fig_size, dpi=pu.dpi, facecolor="w", edgecolor="k"
    )

    d1 = d1.loc[d1["Time"] > 0]

    confs = d1.spec.unique()
    min_ts = 130212512
    max_ts = 0

    markers = ["o", "v", "s", "x", "*","1"]
    for ic, c in enumerate(confs):
        d = d1.loc[d1.spec == c].loc[d1.conf == "ULA"]
        # print(d)
        # min_ts = min(min(d.Size), min_ts)
        # max_ts = max(max(d.Size), max_ts)
        label = c.replace("spec_","")
        pu.add_line(
            ax[0], np.array(range(len(d.AUC))) + 1, d.AUC* 100, np.zeros(len(d.Time)), label, "--", marker=markers[ic]
        )
        pu.add_line(
            ax[1], np.array(range(len(d.Time))) + 1, d.Time, np.zeros(len(d.Time)), label, "--", marker=markers[ic]
        )

    for ic, c in enumerate(confs):
        d = d1.loc[d1.spec == c].loc[d1.conf == "TAWA"]
        # print(d)
        # min_ts = min(min(d.Size), min_ts)
        # max_ts = max(max(d.Size), max_ts)
        label = c.replace("spec_","")
        # pu.add_line(
        #     ax[0], np.array(range(len(d.AUC))) + 1, d.AUC* 100, np.zeros(len(d.Time)), label, "--", marker=markers[ic]
        # )
        pu.add_line(
            ax[2], np.array(range(len(d.Time))) + 1, d.Time, np.zeros(len(d.Time)), label, "--", marker=markers[ic]
        )


    ax[0].grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)
    ax[1].grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)


    ax[0].set_xticks([1,3, 5,7,9])
    ax[1].set_xticks([1,3, 5,7,9])
    ax[1].set_xticks([1,3, 5,7,9])
    ax[0].xaxis.set_label_coords(0.5, -0.3)
    ax[1].xaxis.set_label_coords(0.5, -0.3)
    ax[2].xaxis.set_label_coords(0.5, -0.3)
    ax[0].legend(ncol=3, loc="upper center", bbox_to_anchor=(0.32, 1.27), fontsize=3.45)

    ax[0].set_xlabel("Polynomial")
    ax[1].set_xlabel("Polynomial")
    ax[1].set_title("ULA")
    ax[2].set_title("TAWA")
    ax[0].set_ylabel("AUC Percentage")
    ax[1].set_ylabel("Execution Time [s]")
    ax[2].set_ylabel("Execution Time [s]")
    plt.subplots_adjust(
        left=0.18, right=0.97, top=0.85, bottom=0.28, wspace=0.65, hspace=0.35
    )

    plt.savefig("plotting/plots/lm/santander/" + name + ".pdf")



d1 = pd.read_csv("plotting/tables/lm/santander/log_dams-so002.csv")

plot(d1, "lm-so002")

# d1 = pd.read_csv("plotting/tables/kmeans10/criteo/log_dams-su1.csv")
# plot(d1, "kmeans10-su1")

