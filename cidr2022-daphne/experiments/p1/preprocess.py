#!/usr/bin/env python3

import pandas as pd

import os
import sys

# *****************************************************************************
# Utilities
# *****************************************************************************

def getDict(col):
    return {val: idx for idx, val in enumerate(sorted(col.unique()))}

def dictEncode(col):
    d = getDict(col)
    return col.map(d), d
    
#def writeFileAndMetaData(df, filename):
#    df.to_csv(filename, sep=",", header=False)
#    with open(filename + ".meta", "w") as f):
#        f.write(",".join([len(df), len(df.columns), ]))
        
# *****************************************************************************
# Main
# *****************************************************************************

if __name__ == "__main__":
    # -------------------------------------------------------------------------
    # Parse arguments
    # -------------------------------------------------------------------------
    
    if(len(sys.argv) != 3):
        print("Usage: python3 {} <pathData> <queryNo>".format(sys.argv[0]))
        sys.exit(1)
        
    pathData = sys.argv[1]
    queryNo = sys.argv[2]

    # -------------------------------------------------------------------------
    # Preprocess CUSTOMER table
    # -------------------------------------------------------------------------
    
    dfC = pd.read_csv(os.path.join(pathData, "customer.tbl"), sep="|", usecols=range(8), header=None)
    #dfC = dfC.head()
    dfC.columns = [
        "C_CUSTKEY",
        "C_NAME",
        "C_ADDRESS",
        "C_NATIONKEY",
        "C_PHONE",
        "C_ACCTBAL",
        "C_MKTSEGMENT",
        "C_COMMENT"
    ]

    #print(dfC)

    for colName in ["C_NAME", "C_ADDRESS", "C_PHONE"]:
        dfC[colName], _ = dictEncode(dfC[colName])
    for colName in ["C_COMMENT"]:
        # Real dictionary encoding is unnecessary and too expensive here.
        dfC[colName] = range(len(dfC))
        
    dfC["C_MKTSEGMENT"], dictMktSegment = dictEncode(dfC["C_MKTSEGMENT"])
    
    print("Code for C_MKTSEGMENT == 'AUTOMOBILE': {}".format(dictMktSegment["AUTOMOBILE"]))
    for colName in ["C_NATIONKEY", "C_MKTSEGMENT"]:
        print("{} is between {} and {} ({} distinct values)".format(
                colName,
                dfC[colName].min(),
                dfC[colName].max(),
                len(dfC[colName].unique())
        ))

    #print(dfC)

    dfC.to_csv(os.path.join(pathData, "customer.csv"), sep=",", header=False, index=False)
    with open(os.path.join(pathData, "customer.csv.meta"), "w") as f:
        f.write(",".join([
            str(len(dfC)), str(len(dfC.columns)), str(0),
            "si64", "si64", "si64", "si64", "si64", "f64", "si64", "si64",
            *dfC.columns
        ]))
    
    # -------------------------------------------------------------------------
    # Preprocess ORDERS table
    # -------------------------------------------------------------------------
    
    dfO = pd.read_csv(os.path.join(pathData, "orders.tbl"), sep="|", usecols=range(9), header=None)
    #dfO = dfO.head()
    dfO.columns = [
        "O_ORDERKEY",
        "O_CUSTKEY",
        "O_ORDERSTATUS",
        "O_TOTALPRICE",
        "O_ORDERDATE",
        "O_ORDERPRIORITY",
        "O_CLERK",
        "O_SHIPPRIORITY",
        "O_COMMENT"
    ]

    #print(dfO)

    for colName in ["O_ORDERSTATUS", "O_ORDERPRIORITY", "O_CLERK"]:
        dfO[colName], _ = dictEncode(dfO[colName])
    for colName in ["O_ORDERDATE"]:
        dfO[colName] = dfO[colName].apply(lambda val: val.replace("-", ""))
    for colName in ["O_COMMENT"]:
        # Real dictionary encoding is unnecessary and too expensive here.
        dfO[colName] = range(len(dfO))
    
    
    print("O_ORDERDATE is between {} and {}".format(dfO["O_ORDERDATE"].min(), dfO["O_ORDERDATE"].max()))
    for colName in ["O_ORDERSTATUS", "O_ORDERPRIORITY", "O_CLERK"]:
        print("{} is between {} and {} ({} distinct values)".format(
                colName,
                dfO[colName].min(),
                dfO[colName].max(),
                len(dfO[colName].unique())
        ))

    #print(dfO)

    dfO.to_csv(os.path.join(pathData, "orders.csv"), sep=",", header=False, index=False)
    with open(os.path.join(pathData, "orders.csv.meta"), "w") as f:
        f.write(",".join([
            str(len(dfO)), str(len(dfO.columns)), str(0),
            "si64", "si64", "si64", "f64", "si64", "si64", "si64", "si64", "si64",
            *dfO.columns
        ]))
    
    # -------------------------------------------------------------------------
    # Preprocess LINEITEM table
    # -------------------------------------------------------------------------
    
    if queryNo == "b":
        # Even at scale factor 10, pandas gets problems with loading the data on my
        # machine (out of memory), so we do it differently here.
        
        dfL = pd.read_csv(os.path.join(pathData, "lineitem.tbl"), sep="|", usecols=[8, 9, 13, 14], header=None)
        
        dfL.columns = [
            "L_RETURNFLAG",
            "L_LINESTATUS",
            "L_SHIPINSTRUCT",
            "L_SHIPMODE"
        ]
        
        dictReturnFlag   = getDict(dfL["L_RETURNFLAG"])
        dictLineStatus   = getDict(dfL["L_LINESTATUS"])
        dictShipInstruct = getDict(dfL["L_SHIPINSTRUCT"])
        dictShipMode     = getDict(dfL["L_SHIPMODE"])
            
        with open(os.path.join(pathData, "lineitem.tbl"), "r") as inCsv:
            with open(os.path.join(pathData, "lineitem.csv"), "w") as outCsv:
                for idx, line in enumerate(inCsv):
                    parts = line.split("|")
                    outCsv.write(",".join(parts[0:8]))
                    outCsv.write(",")
                    outCsv.write(str(dictReturnFlag[parts[8]]))
                    outCsv.write(",")
                    outCsv.write(str(dictLineStatus[parts[9]]))
                    outCsv.write(",")
                    outCsv.write(",".join(parts[10:13]).replace("-", ""))
                    outCsv.write(",")
                    outCsv.write(str(dictShipInstruct[parts[13]]))
                    outCsv.write(",")
                    outCsv.write(str(dictShipMode[parts[14]]))
                    outCsv.write(",")
                    outCsv.write(str(idx))
                    outCsv.write("\n")

        with open(os.path.join(pathData, "lineitem.csv.meta"), "w") as f:
            f.write(",".join([
                str(len(dfL)), str(16), str(0),
                "si64", "si64", "si64", "si64", "si64", "f64", "f64", "f64", "si64", "si64", "si64", "si64", "si64", "si64", "si64", "si64",
                "L_ORDERKEY",
                "L_PARTKEY",
                "L_SUPPKEY",
                "L_LINENUMBER",
                "L_QUANTITY",
                "L_EXTENDEDPRICE",
                "L_DISCOUNT",
                "L_TAX",
                "L_RETURNFLAG",
                "L_LINESTATUS",
                "L_SHIPDATE",
                "L_COMMITDATE",
                "L_RECEIPTDATE",
                "L_SHIPINSTRUCT",
                "L_SHIPMODE",
                "L_COMMENT"
            ]))
