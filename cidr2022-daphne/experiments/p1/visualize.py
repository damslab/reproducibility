#!/usr/bin/env python3

import os
import stat
import sys

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

def getNumLines(filePath):
    numLines = 0
    with open(filePath, "r") as f:
        for line in f:
            numLines += 1
    return numLines

if __name__ == "__main__":
    pathArtifacts = sys.argv[1]
    sf = int(sys.argv[2])
    queryNo = sys.argv[3]
    systems = [
        "Daphne",
        #"MDBTF_preloaded",
        #"MDBTF_scratch",
        "MDBTF_tmptbl",
        #"PDTF_stored",
        "PDTF_direct",
        #"DDBTF_stored",
        "DDBTF_direct",
    ]
    
    dfs = []
    
    if queryNo == "a":
        params = [(0, 19950802), (2, 19950802), (4, 19950802)]
    elif queryNo == "b":
        params = [(0, 19980202), (2, 19950802), (4, 19920802)]
    else:
        raise RuntimeError("unexpected query number: {}".format(queryNo))
    
    for mktSegUpper, orderDateLower in params:
        queryResPath = os.path.join(
                pathArtifacts,
                "results_sf{}_q{}".format(sf, queryNo),
                # Doesn't matter which system, since the query result is the same.
                "query_MDBTF_tmptbl_msu{}_odl{}.csv".format(mktSegUpper, orderDateLower)
        )
        queryResNumRows = getNumLines(queryResPath)
        queryResSel = queryResNumRows / (sf * 150000)
        queryResFileSize = os.stat(queryResPath)[stat.ST_SIZE]
        for system in systems:
            csvPath = os.path.join(
                    pathArtifacts,
                    "runtimes_sf{}_q{}".format(sf, queryNo),
                    "{}_msu{}_odl{}.csv".format(system, mktSegUpper, orderDateLower)
            )
            df = pd.read_csv(csvPath, sep="\t")
            
            G = 1000 * 1000 * 1000
            if True: # the old way
                if system == "Daphne":
                    df["A [s]"] = (df["runtime load [ns]"] + df["runtime query [ns]"]) / G
                    df["B [s]"] = df["runtime cast [ns]"] / G
                    df["C [s]"] = df["runtime train+save [ns]"] / G
                    df["X [s]"] = 0
                if system == "MDBTF_preloaded":
                    df["A [s]"] = df["runtime load+query [ns]"] / G
                    df["B [s]"] = (df["runtime load+query+isave [ns]"] - df["runtime load+query [ns]"]) / G + df["runtime iload [s]"] + df["runtime cast [s]"]
                    df["C [s]"] = df["runtime train+save [s]"]
                    df["X [s]"] = df["runtime pyload1 [s]"] + df["runtime pyload2 [s]"]
                if system == "MDBTF_scratch":
                    df["A [s]"] = df["runtime load+query [ns]"] / G
                    df["B [s]"] = (df["runtime load+query+isave [ns]"] - df["runtime load+query [ns]"]) / G + df["runtime iload [s]"] + df["runtime cast [s]"]
                    df["C [s]"] = df["runtime train+save [s]"]
                    df["X [s]"] = df["runtime createdb [ns]"] / G + df["runtime pyload1 [s]"] + df["runtime pyload2 [s]"]
                if system == "MDBTF_tmptbl":
                    df["A [s]"] = df["runtime load+query [ns]"] / G
                    df["B [s]"] = (df["runtime load+query+isave [ns]"] - df["runtime load+query [ns]"]) / G + df["runtime iload [s]"] + df["runtime cast [s]"]
                    df["C [s]"] = df["runtime train+save [s]"]
                    df["X [s]"] = df["runtime pyload1 [s]"] + df["runtime pyload2 [s]"]
                if system == "PDTF_stored":
                    df["A [s]"] = df["runtime load [s]"] + df["runtime query [s]"]
                    df["B [s]"] = df["runtime isave [s]"] + df["runtime iload [s]"] + df["runtime cast [s]"]
                    df["C [s]"] = df["runtime train+save [s]"]
                    df["X [s]"] = df["runtime pyload1a [s]"] + df["runtime pyload1b [s]"] + df["runtime pyload2b [s]"]
                if system == "PDTF_direct":
                    df["A [s]"] = df["runtime load [s]"] + df["runtime query [s]"]
                    df["B [s]"] = df["runtime cast [s]"]
                    df["C [s]"] = df["runtime train+save [s]"]
                    df["X [s]"] = df["runtime pyload1 [s]"] + df["runtime pyload2 [s]"]
                if system == "DDBTF_stored":
                    df["A [s]"] = df["runtime load [s]"] + df["runtime query [s]"]
                    df["B [s]"] = df["runtime isave [s]"] + df["runtime iload [s]"] + df["runtime cast [s]"]
                    df["C [s]"] = df["runtime train+save [s]"]
                    df["X [s]"] = df["runtime pyload1a [s]"] + df["runtime pyload2a [s]"] + df["runtime pyload1b [s]"] + df["runtime pyload3b [s]"]
                if system == "DDBTF_direct":
                    df["A [s]"] = df["runtime load [s]"] + df["runtime query [s]"]
                    df["B [s]"] = df["runtime cast [s]"]
                    df["C [s]"] = df["runtime train+save [s]"]
                    df["X [s]"] = df["runtime pyload1 [s]"] + df["runtime pyload2 [s]"] + df["runtime pyload3 [s]"]
            else: # the new way, for some of the systems
                if system == "Daphne":
                    df["A [s]"] = (df["runtime load [ns]"] + df["runtime query [ns]"]) / G
                    df["B [s]"] = df["runtime cast [ns]"] / G
                    df["C [s]"] = df["runtime train+save [ns]"] / G
                    df["X [s]"] = 0
                if system == "MDBTF_tmptbl":
                    df["A [s]"] = df["runtime load+query [ns]"] / G
                    df["B [s]"] = (df["runtime load+query+isave [ns]"] - df["runtime load+query [ns]"]) / G + df["runtime iload [s]"] + df["runtime cast [s]"]
                    df["C [s]"] = df["runtime pyload1 [s]"] + df["runtime pyload2 [s]"] + df["runtime train+save [s]"]
                    df["X [s]"] = 0
                if system == "PDTF_direct":
                    df["A [s]"] = df["runtime load [s]"] + df["runtime query [s]"] + df["runtime pyload1 [s]"]
                    df["B [s]"] = df["runtime cast [s]"]
                    df["C [s]"] = df["runtime train+save [s]"] + df["runtime pyload2 [s]"]
                    df["X [s]"] = 0
                if system == "DDBTF_direct":
                    df["A [s]"] = df["runtime load [s]"] + df["runtime query [s]"] + df["runtime pyload1 [s]"] + df["runtime pyload2 [s]"]
                    df["B [s]"] = df["runtime cast [s]"]
                    df["C [s]"] = df["runtime train+save [s]"] + df["runtime pyload3 [s]"]
                    df["X [s]"] = 0
            
            # Discard system-specific columns.
            df = df[["system", "repIdx", "runtime [ns]", "A [s]", "B [s]", "C [s]", "X [s]"]]
            
            df["scale factor"] = sf
            df["msu"] = mktSegUpper
            df["odl"] = orderDateLower
            
            df["qrNumRows"] = queryResNumRows
            df["qrSel"] = queryResSel
            df["qrFileSize"] = queryResFileSize
            
            dfs.append(df)
    dfAll = pd.concat(dfs)
    
    colInterm = "Size of relational query result [MB]"
    dfAll["runtime [s]"] = dfAll["runtime [ns]"] / 1000000000
    dfAll[colInterm] = dfAll.apply(lambda row: "{:.0f}".format(row["qrFileSize"] / 1000000), axis=1)
    dfAll["system"] = dfAll["system"].map({
        "Daphne": "DAPHNE",
        #"MonetDB+TF (pre-loaded data)": "MonetDB+TF (pre-loaded DB)",
        #"MonetDB+TF (from scratch)": "MonetDB+TF (create new DB)",
        "MonetDB+TF (temporary table)": "MonetDB+TF",
        #"Pandas+TF (stored intermediate)": "Pandas+TF (query res via file)",
        "Pandas+TF (direct handover)": "Pandas+TF",
        #"DuckDB+TF (stored intermediate)": "DuckDB+TF (query res via file)",
        "DuckDB+TF (direct handover)": "DuckDB+TF",
    })
    dfAll["A+B [s]"] = dfAll["A [s]"] + dfAll["B [s]"]
    dfAll["A+B+C [s]"] = dfAll["A+B [s]"] + dfAll["C [s]"]
    dfAll["A+B+C+X [s]"] = dfAll["A+B+C [s]"] + dfAll["X [s]"]
    dfAll["U [s]"] = dfAll["runtime [s]"] - dfAll["A+B+C [s]"]
    
    dfAll["Runtime [s]"] = dfAll["runtime [s]"]
    
    sns.set_context("paper", 1.4)
    
    fig = plt.figure(figsize=(5, 3))
    ax = fig.add_subplot(111)
    sns.barplot(
        ax=ax,
        y="Runtime [s]", ci=None, x=colInterm, hue="system",
        data=dfAll,
        edgecolor="black", linewidth=0.25
    )
    ax.legend(
        bbox_to_anchor=(0.01, 1),
        loc="upper left",
        handlelength=1,
        labelspacing=0.25,
        handletextpad=0.4,
        borderpad=0,
        borderaxespad=0,
        frameon=False,
    )
    ax.set_ylim(top=ax.get_ylim()[1] * 1.4)
    sns.despine()
    fig.savefig(os.path.join(pathArtifacts, "p1_{}_e2e.pdf".format(queryNo)), bbox_inches="tight")
    
    fig = plt.figure(figsize=(5, 3))
    ax = fig.add_subplot(111)
    #hatches = [20*"x", 8*".", None, 8*"/", None]
    #hatches = [20*"x", None, 8*"/", None]
    hatches = [4*".", None, 4*"/", None]
    #hatches = [None, None, None, None, None]
    for yCol, hatch in zip(
        [
            "Runtime [s]",
            #"A+B+C+X [s]",
            "A+B+C [s]",
            "A+B [s]",
            "A [s]"
        ],
        hatches
    ):
        rects = sns.barplot(
            ax=ax,
            y=yCol, ci=None, x=colInterm, hue="system",
            data=dfAll,
            edgecolor="black", linewidth=0.5, hatch=hatch
        )
    ax.get_legend().remove()
    ax.legend(
        handles=[
            patches.Rectangle(
                    (0, 0), 1, 1, linewidth=0.5,
                    facecolor=fc, edgecolor="black", hatch=None
            )
            for fc in sns.color_palette()[:len(systems)]
        ] + [
            patches.Rectangle(
                    (0, 0), 1, 1, linewidth=0.5,
                    facecolor="white", edgecolor="black", hatch=hatch
            )
            for hatch in hatches
        ],
        labels=[
            "DAPHNE",
            #"MonetDB+TF (pre-loaded DB)",
            #"MonetDB+TF (create new DB)",
            "MonetDB+TF",
            #"Pandas+TF (query res via file)",
            "Pandas+TF",
            #"DuckDB+TF (query res via file)",
            "DuckDB+TF",
            
            #"(rest)",
            "start-up",
            "LM training",
            "border-crossing",
            "relational query"
        ],
        bbox_to_anchor=(0.01, 1),
        loc="upper left",
        handlelength=1,
        labelspacing=0.25,
        handletextpad=0.4,
        borderpad=0,
        borderaxespad=0,
        frameon=False,
        ncol=2
    )
    ax.set_ylim(top=ax.get_ylim()[1] * 1.4)
    ax.set_ylabel("Runtime [s]")
    sns.despine()
    fig.savefig(os.path.join(pathArtifacts, "p1_{}_e2e_stacked.pdf".format(queryNo)), bbox_inches="tight")
