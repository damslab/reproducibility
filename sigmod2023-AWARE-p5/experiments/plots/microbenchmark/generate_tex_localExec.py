import os

import argparse


def flo(f):
    return '\\numprint{' + "{0:0.1f}".format(f) + "}"


def inte(f):
    return '\\numprint{' + "{0:0.0f}".format(f) + "}"


def parse(file):

    col = {"kmeans+": 1, "PCA+": 3, "mLogReg+": 5,
           "lmCG+": 7, "lmDS+": 9, "l2svm+": 11}

    col = {"ulab16-hybrid": 1, "clab16-hybrid": 3, "claWorkloadb16-hybrid": 5}

    row = {"kmeans+": 0,
           "PCA+": 1,
           "mLogReg+": 2,
           "lmCG+": 3,
           "lmDS+": 4,
           "l2svm+": 5}

    # data = {"ulab16-hybrid": 0, "claWorkloadb16-hybrid": 1}
    matrix = [["" for i in range(6)] for j in range(len(row))]

    matrix[0][0] = '\\textbf{K-Means}'
    matrix[1][0] = '\\textbf{PCA}    '
    matrix[2][0] = '\\textbf{MLogReg}'
    matrix[3][0] = '\\textbf{lmCG}   '
    matrix[4][0] = '\\textbf{lmDS}   '
    matrix[5][0] = '\\textbf{L2SVM}  '

    with open(file) as f:
        firstLine = True
        l = ""
        for line in f:
            if firstLine:
                firstLine = False
                continue

            parts = [x.strip() for x in line.split(",")]
            r_id = parts[1]
            t = parts[3]
            c_id = parts[2]
            if t != "nan" and r_id in row and c_id in col and "census_enc_16k" in parts[0]:
                r = row[r_id]
                c = col[c_id]
                v = float(parts[3])
                if (v > 10):
                    matrix[r][c] = flo(v) + " sec"
                else:
                    matrix[r][c] = inte(v) + " sec"
                comp = float(parts[6])
                if (comp > 0):
                    matrix[r][c-1] = flo(comp - float(parts[5])) + " sec"
                # if(float(parts[5]) != 0):
                #     matrix[r][c] = "()"  +matrix[r][c]

    return matrix


def make_tex_table(data):
    s = ""
    idx = 0
    for x in data:
        for y in x:
            s += y + " &\t"
        # if more than 4 no comma.
        # \num{v}
        s = s[:-2] + " \\\\\n"
        idx += 1
    return s


parser = argparse.ArgumentParser()
parser.add_argument("-x", "--machines", nargs="+", required=False)
args = parser.parse_args()
machinesList = args.machines


header="""\\begin{tabular}{r|r|rr|rr}
\\toprule
                 & \\textbf{ULA}        & \\multicolumn{2}{c|}{\\textbf{\\name-Mem}} & \\multicolumn{2}{c}{\\textbf{\\name}}                                             \\\\
                 & Time                & Comp                                    & Time                               & Comp                & Time                \\\\
\\midrule
"""

footer="""\\bottomrule
\\end{tabular}
"""
for machine in machinesList:
    file = "plots/microbenchmark/tab/table_algs_local_"+machine+".csv"
    with open("plots/tables/local_end_"+machine+".tex", "w") as f:
        f.write(header)
        d = parse(file)
        s = make_tex_table(d)
        f.write(s)
        f.write(footer)
