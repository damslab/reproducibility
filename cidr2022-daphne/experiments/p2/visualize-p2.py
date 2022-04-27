#!/usr/bin/env python3

import os
import stat
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

def getNumLines(filePath):
    numLines = 0
    with open(filePath, "r") as f:
        for line in f:
            numLines += 1
    return numLines

if __name__ == "__main__":
    pathArtifacts = sys.argv[1]
    systems = [
        "DAPHNE",
        "SYSDS",
        "SYSDSP",
        "TF",
        "TFXLA"
    ]
    
    dfs = []
    
    for system in systems:
        csvPath = os.path.join(pathArtifacts,"{}_runtimes.csv".format(system))
        csvPath2 = os.path.join(pathArtifacts,"{}-dataload.csv".format(system))
        csvPath3 = os.path.join(pathArtifacts,"{}-scoring.csv".format(system))

        df = pd.read_csv(csvPath, sep="\t")
        df2 = pd.read_csv(csvPath2, sep="\t")
        df3 = pd.read_csv(csvPath3, sep="\t")
        #print(df2.keys())
        # Discard all individual parts of the runtime.
        df = df[["system", "repIdx", "runtime [ns]"]]        
        #df2 = df2['loadtime [ns]']
        #df = df.join(df2)
        df[["loadtime [ns]"]] =  df2[["runtime [ns]"]]
        df[["scoring [ns]"]] =  df3[["runtime [ns]"]]
        
        dfs.append(df)
    dfAll = pd.concat(dfs)
    
    dfAll["Runtime [s]"] = dfAll["runtime [ns]"] / 1000000000
    dfAll["Loadtime [s]"] = dfAll["loadtime [ns]"] / 1000000000
    dfAll["Scoring [s]"] = dfAll["scoring [ns]"] / 1000000000

    dfAll["System"] = dfAll["system"].map({
        "DAPHNE": "Daphne",
        "SYSDS": "SysDS",
        "SYSDSP": "SysDS-MT",
        "TF": "TF",
        "TFXLA": "TF/XLA",
    })
    
    #dfAll["inference [s]"] = dfAll["runtime [s]"] - dfAll["loadtime [s]"] 
    grouped = dfAll.groupby('System')    
    avg_load = grouped['Loadtime [s]'].agg(np.mean)
    avg_e2e =  grouped['Runtime [s]'].agg(np.mean)
    avg_sco = grouped['Scoring [s]'].agg(np.mean)
    
    print(dfAll)
    print("-----------------------------------------------")
    print(avg_load)
    print("-----------------------------------------------")
    print(avg_e2e)
    print("-----------------------------------------------")
    print(avg_sco)
    print("-----------------------------------------------")
    sns.set_context("paper", 1.4)
    
    fig = plt.figure(figsize=(5, 3))
    ax = fig.add_subplot(111)
    
    colors = iter(sns.color_palette('Set1', n_colors=2, desat=.75))
    
    #chart = sns.barplot(ax=ax, y="runtime [s]", x="system", data=dfAll, color="blue")
    #chart = sns.barplot(ax=ax, y="loadtime [s]", x="system", data=dfAll, color="red")
    c0=sns.color_palette()[0]
    c1=sns.color_palette()[1]
    c2=sns.color_palette()[2]
    chart = sns.barplot(ci=None, ax=ax, y="Runtime [s]", x="System", data=dfAll, color=c0)#, color=next(colors))
    chart = sns.barplot(ci=None, ax=ax, y="Loadtime [s]", x="System", data=dfAll, color=c1)#, color=next(colors))
    #chart = sns.barplot(ax=ax, y="scoring [s]", x="system", data=dfAll, color=c2)#, color=next(colors))

    #chart = sns.barplot(ax=ax, y="runtime [s]", x="system", data=dfAll, hue=["runtime [s]", "loadtime [s]", "inference [s]"])#, color=next(colors))
    chart.set(ylabel="Runtime [s]")

    bar1 = mpatches.Patch(color=c0, label='Scoring')
    bar2 = mpatches.Patch(color=c1, label='Loading')
    #bar3 = mpatches.Patch(color=c2, label='scoring')
    
    #ax.legend(bbox_to_anchor=(0, 1), loc="upper left", handlelength=1, labelspacing=0.25, handletextpad=0.4, frameon=False, handles=[bar1, bar2])
    
    ax.legend(
        bbox_to_anchor=(0.01, 1),
        loc="upper left",
        handlelength=1,
        labelspacing=0.25,
        handletextpad=0.4,
        borderpad=0,
        borderaxespad=0,
        frameon=False,
        handles=[bar1, bar2]
    )
    
    ax.set_ylim(top=ax.get_ylim()[1] * 1.2)
    sns.despine()
    fig.savefig(os.path.join(pathArtifacts, "p2-e2e.pdf"), bbox_inches="tight")
    plt.close(fig)
    
    fig = plt.figure(figsize=(5, 3))
    ax = fig.add_subplot(111)
    chart2 = sns.barplot(ax=ax, y="Runtime [s]", x="System", data=dfAll)#, color=c0)#, color=next(colors))    
    #bar1 = mpatches.Patch(color=c0, label='running')
    
    ax.legend(bbox_to_anchor=(0, 1), loc="upper left", handlelength=1, labelspacing=0.25, handletextpad=0.4, frameon=False)#, handles=[bar1])
    ax.set_ylim(top=ax.get_ylim()[1] * 1.2)
    sns.despine()
    fig.savefig(os.path.join(pathArtifacts, "p2-run.pdf"), bbox_inches="tight")
    plt.close()

    fig = plt.figure(figsize=(5, 3))
    ax = fig.add_subplot(111)
    chart3 = sns.barplot(ax=ax, y="Loadtime [s]", x="System", data=dfAll)#, color=c1)#, color=next(colors))
    #bar2 = mpatches.Patch(color=c1, label='loading')
    ax.legend(bbox_to_anchor=(0, 1), loc="upper left", handlelength=1, labelspacing=0.25, handletextpad=0.4, frameon=False)
    #, handles=[bar2])
    ax.set_ylim(top=ax.get_ylim()[1] * 1.2)
    sns.despine()
    fig.savefig(os.path.join(pathArtifacts, "p2-load.pdf"), bbox_inches="tight")
    plt.close()
    
    fig = plt.figure(figsize=(5, 3))
    ax = fig.add_subplot(111)
    chart4 = sns.barplot(ax=ax, y="Scoring [s]", x="System", data=dfAll)#, color=c2)#, color=next(colors))
    #bar3 = mpatches.Patch(color=c2, label='scoring')
    ax.legend(bbox_to_anchor=(0, 1), loc="upper left", handlelength=1, labelspacing=0.25, handletextpad=0.4, frameon=False)
    #, handles=[bar3])
    ax.set_ylim(top=ax.get_ylim()[1] * 1.2)
    sns.despine()
    fig.savefig(os.path.join(pathArtifacts, "p2-sco.pdf"), bbox_inches="tight")
    plt.close()
    
    # fig = plt.figure(figsize=(5, 3))
    # ax = fig.add_subplot(111)
    # chart5 = sns.barplot(ax=ax, y="loadtime [s]", x="scoring [s]", hue="system", data=dfAll)#, color=c2)#, color=next(colors))
    # #bar3 = mpatches.Patch(color=c2, label='scoring')
    # ax.legend(bbox_to_anchor=(0, 1), loc="upper left", handlelength=1, labelspacing=0.25, handletextpad=0.4, frameon=False)
    # #, handles=[bar3])
    # ax.set_ylim(top=ax.get_ylim()[1] * 1.2)
    # sns.despine()
    # fig.savefig(os.path.join(pathArtifacts, "p2_e2e-hue.pdf"), bbox_inches="tight")
