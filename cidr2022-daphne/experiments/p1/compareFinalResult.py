#!/usr/bin/env python3

import pandas as pd

import math
import sys
        
# *****************************************************************************
# Main
# *****************************************************************************

if __name__ == "__main__":
    # -------------------------------------------------------------------------
    # Argument parsing
    # -------------------------------------------------------------------------
    
    if(len(sys.argv) != 3 and len(sys.argv) != 5):
        print("Usage: python3 {} <pathFinalResultDaphne> <pathFinalResultTensorFlow> [<rowIdxs> <tolerance>]".format(sys.argv[0]))
        sys.exit(1)
        
    pathFileDaphne = sys.argv[1]
    pathFileTensorFlow = sys.argv[2]
    if len(sys.argv) == 5:
        specialRowIdxs = [int(s) for s in sys.argv[3].split(",")]
        specialTolerance = float(sys.argv[4])
    else:
        specialRowIdxs = []
        
    normalTolerance = 0.01
    
    # -------------------------------------------------------------------------
    # Result data comparison
    # -------------------------------------------------------------------------

    dfResDaphne = pd.read_csv(pathFileDaphne, sep=" ", skiprows=1, header=None)
    dfResTensorFlow = pd.read_csv(pathFileTensorFlow, header=None)

    # print(dfResDaphne[0].head())
    # print(dfResTensorFlow[0].head())

    # print("#rows: {}".format(len(dfResDaphne)))

    dfDiff = (dfResDaphne - dfResTensorFlow).abs()
    if len(dfDiff.columns) == 1:
        vDiff = dfDiff[0].values
        for i in range(len(vDiff)):
            if dfResDaphne[0].values[i] == 0:
                if vDiff[i] == 0:
                    relDiff = 0
                else:
                    relDiff = math.inf
            else:
                relDiff = vDiff[i] / dfResDaphne[0].values[i]
                
            if i in specialRowIdxs:
                ok = relDiff < specialTolerance
            else:
                ok = relDiff < normalTolerance
    else:
        maxRelDiff = (dfDiff / dfResDaphne).max().max()
        ok = maxRelDiff < normalTolerance
    
    if ok:
        print("ok")
        sys.exit(0)
    else:
        print("not ok")
        sys.exit(1)
