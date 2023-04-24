import argparse
import os

import numpy as np


def parseAWARE(path, op):

    orgCost = []
    estCost = []
    actCost = []
    comp = []
    total = []

    repeats = 0

    if os.path.isfile(path):
        with open(path) as f:
            for line in f:
                if "DEBUG compress.CompressedMatrixBlockFactory: --original cost:    " in line:
                    orgCost.append(float(line[83:]))
                elif "DEBUG compress.CompressedMatrixBlockFactory: --cocode cost:   " in line:
                    estCost.append(float(line[83:]))
                elif "DEBUG compress.CompressedMatrixBlockFactory: --actual cost:    " in line:
                    actCost.append(float(line[83:]))
                elif " compress     " in line:
                    comp.append(float(line[15:26]))
                elif isinstance(op, str) and op in line:
                    total.append(float(line[15:26]))
                elif isinstance(op, list):
                    for ido, ent in enumerate(op):
                        if ent in line and "MATRIX" not in line and "org.apache.sysds" not in line:
                            v = float(line.split(ent)[
                                              1].replace("\t", "").replace(",", "")[:-6])
                            total.append(v)
                            if ido == 0:
                                repeats += 1
        if isinstance(op, list):
            total = [sum(total) / repeats]
        return orgCost, estCost, actCost, comp, total
    return None


def parseBase(path, op):
    total = []
    repeats = 0
    if os.path.isfile(path):
        with open(path) as f:
            for line in f:
                if isinstance(op, str) and op in line:
                    total.append(float(line[15:26]))
                elif isinstance(op, list):
                    for ido, ent in enumerate(op):
                        if ent in line and "MATRIX" not in line and "org.apache.sysds" not in line:
                            v = float(line.split(ent)[
                                              1].replace("\t", "").replace(",", "")[:-6])
                            total.append(v)
                            if ido == 0:
                                repeats += 1
        if isinstance(op, list) and repeats != 0 :
            
            total = [sum(total) / repeats]
            
        return total
    return -1


def lts(d):
    return np.format_float_scientific(sum(d) / len(d), unique=False, exp_digits=2, precision=2)


def numPrintFormat(d):
    d = np.average(d)

    return "\\numprint{" + "{0:0.2f}".format(d) + "}"


basePath = "results/{e1}/{e2}/census_enc/{m}/{t}-singlenode.log"

exp = [
    ["UA", "sum", "SUM", "  uak+   "],
    ["UA", "sum+", "SUM Dense", "  uak+   "],
    ["Sc", "plus", "Plus", "  +     "],
    ["MM", "mmr-256", "RMM-256", "  ba+*    "],
    ["MM", "mml-256", "LMM-256", "  ba+*    "],
    ["UA", "tsmm", "TSMM", "  tsmm     "],
    ["UA", "scaleshift", "ScaleShift", [" uacmean ", " uacsqk+ ", " - ", " / "]],
    ["MM", "euclidean-256", "Euclidean-256", [" ba+*", " * ", " + ", " uarmin"]]
]

tec = ["ulab16Copy", "claWorkloadb16Copy"]

parser = argparse.ArgumentParser()
parser.add_argument("-x", "--machines", nargs="+", required=False)
args = parser.parse_args()
machinesList = args.machines


outStringBase = "{e3} & {orgCost}  & {actTime} sec & {estCost}  & {actCost} & {comp} sec  & {compTime} sec \\\\\n"


header = """\\begin{tabular}{r|rr|rrrr}
\\toprule
               & \\multicolumn{2} {c|}{\\textbf{ULA}} & \\multicolumn{4} {c}{\\textbf{\\name}}                                                                                                                  \\\\
Op $\\cdot$ 100 & \\multicolumn{1}{c}{TOPS}           & \\multicolumn{1}{c|}{Time}           & \\multicolumn{1}{c}{Est. TOPS} & \\multicolumn{1}{c}{TOPS} & \\multicolumn{1}{c}{Comp} & \\multicolumn{1}{c}{Time} \\\\
\\midrule
"""
footer = """\\bottomrule
\\end{tabular}"""

for m in machinesList:
    with open("plots/tables/tops_"+m+".tex", "w") as f:
        f.write(header)
        for e in exp:
            dAWARE = parseAWARE(basePath.format(
                e1=e[0], e2=e[1], t=tec[1], m=m), e[3])
            dULA = parseBase(basePath.format(
                e1=e[0], e2=e[1], t=tec[0], m=m), e[3])
           
            if dAWARE:

                s = outStringBase.format(e3=e[2],
                                         orgCost=lts(dAWARE[0]),
                                         actTime=numPrintFormat(dULA),
                                         estCost=lts(dAWARE[1]),
                                         actCost=lts(dAWARE[2]),
                                         comp=numPrintFormat(dAWARE[3]),
                                         compTime=numPrintFormat(dAWARE[4]))
                f.write(s)

        f.write(footer)