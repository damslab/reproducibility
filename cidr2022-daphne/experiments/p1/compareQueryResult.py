#!/usr/bin/env python3

import pandas as pd

import sys
        
# *****************************************************************************
# Main
# *****************************************************************************

if __name__ == "__main__":
    # -------------------------------------------------------------------------
    # Argument parsing
    # -------------------------------------------------------------------------
    
    if(len(sys.argv) != 4):
        print("Usage: python3 {} <queryNo> <pathFileDaphne> <pathFileMonetDB>".format(sys.argv[0]))
        sys.exit(1)
        
    queryNo = sys.argv[1]
    pathFileDaphne = sys.argv[2]
    pathFileMonetDB = sys.argv[3]
    
    # -------------------------------------------------------------------------
    # Result data comparison
    # -------------------------------------------------------------------------

    dfResDaphne = pd.read_csv(pathFileDaphne, sep=" ", skiprows=1, header=None)
    dfResMonetDB = pd.read_csv(pathFileMonetDB, sep=",", header=None)

    if queryNo == "a":
        for df in [dfResDaphne, dfResMonetDB]:
            df.columns = [
                "C_CUSTKEY",
                "C_NAME",
                "C_ADDRESS",
                "C_NATIONKEY",
                "C_PHONE",
                "C_ACCTBAL",
                "C_MKTSEGMENT",
                "C_COMMENT",
                "SUM(O_TOTALPRICE)"
            ]
    elif queryNo == "b":
        for df in [dfResDaphne, dfResMonetDB]:
            df.columns = [
                "O_ORDERKEY",
                "O_CUSTKEY",
                "O_ORDERSTATUS",
                "O_TOTALPRICE",
                "O_ORDERDATE",
                "O_ORDERPRIORITY",
                "O_CLERK",
                "O_SHIPPRIORITY",
                "O_COMMENT",
                "SUM(L_EXTENDEDPRICE)"
            ]
    
    for df in [dfResDaphne, dfResMonetDB]:
        df.sort_values(df.columns[0], inplace=True)
        df.index = df[df.columns[0]]

    print(dfResDaphne.head())
    print(dfResMonetDB.head())

    print("#rows Daphne:  {}".format(len(dfResDaphne)))
    print("#rows MonetDB: {}".format(len(dfResMonetDB)))

    for colName in dfResDaphne.columns:
        if colName in ["SUM(O_TOTALPRICE)", "O_TOTALPRICE", "SUM(L_EXTENDEDPRICE)"]:
            colOk = ((dfResDaphne[colName] - dfResMonetDB[colName]).abs() / dfResDaphne[colName]).max() < 0.01
        else:
            colOk = all(dfResDaphne[colName] == dfResMonetDB[colName])
        print("{}:\t{}".format(colName, {False: "NOT OK", True: "ok"}[colOk]))
