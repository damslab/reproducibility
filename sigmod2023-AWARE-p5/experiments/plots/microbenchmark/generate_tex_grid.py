import os

import argparse


def flo(f):
    return '\\numprint{' + "{0:0.1f}".format(f) + "}"


def inte(f):
    return '\\numprint{' + "{0:0.0f}".format(f) + "}"


def parse(file, col={"kmeans+": 1, "PCA+": 3, "mLogReg+": 5}):
    # col = {"lmCG+" :1, "LmDS+" : 3 , "l2svm+" : 5}
    # col = {"kmeans+": 1, "PCA+": 3, "mLogReg+": 5,
    #        "lmCG+": 7, "lmDS+": 9, "l2svm+": 11}
    # "census_enc_16k": 0,
    # row = {
    #     "census_enc_8x_16k": 0,
    #     "census_enc_16x_16k": 1,
    #     "census_enc_32x_16k": 2,
    #     "census_enc_128x_16k": 3}

    # row ={

    #     "train_census_enc    ,l2svmml             ,ula-sysml-hybrid-spark  ":0,
    #     "train_census_enc    ,l2svmml             ,cla-sysml-hybrid-spark  ":1,
    #     "census_enc_16k      ,l2svmml             ,ulab16-hybrid           ":2,
    #     "census_enc_16k      ,l2svmml             ,clab16-hybrid           ":3,
    #     "census_enc_16k      ,l2svmml             ,claWorkloadb16-hybrid   ":4

    # }
    # row128 = {

    #     "train_census_enc_128x,l2svmml             ,ula-sysml-hybrid-spark ":0,
    #     "train_census_enc_128x,l2svmml             ,cla-sysml-hybrid-spark ":1,
    #     "census_enc_128x_16k ,l2svmml             ,ulab16-hybrid           ":2,
    #     "census_enc_128x_16k ,l2svmml             ,clab16-hybrid           ":3,
    #     "census_enc_128x_16k ,l2svmml             ,claWorkloadb16-hybrid   ":4
    # }

    col = {
     "ulab16-hybrid": 0,
     "clab16-hybrid": 1,
     "claWorkloadb16-hybrid": 2
    }


    # data = {"ulab16-hybrid": 0, "claWorkloadb16-hybrid": 1}

    matrix = [["" for i in range(3)] for j in range(1)]

    # matrix[0][0] = "1x"
    # matrix[0][0] = "SysML - ULA"
    # matrix[1][0] = "SysML - CLA"
    # matrix[2][0] = "ULA"
    # matrix[3][0] = "\\name-Mem"
    # matrix[4][0] = "\\name"

    with open(file) as f:
        # firstLine = True
        # l = ""
        for line in f:
            parts = [x.strip() for x in line.split(",")]
            if parts[2] in col:
                # print(parts)
                
                c_id = col[parts[2]] 
                # r_id = row[line[:rowlen]] 
                matrix[0][c_id] = flo(float(parts[3])) + " sec"
    #             if(float(parts[6]) < 0.1):
    #                 matrix[r_id][2] = "---"
    #             else:
    #                 matrix[r_id][2] =flo( float(parts[6])) + " sec"
    #             matrix[r_id][3] = flo(float(parts[3]) - float(parts[5]) - float(parts[6])) + " sec"
    #             matrix[r_id][4] = flo(float(parts[3])) + " sec"


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


header ="""\\begin{tabular}{c|c|c}
\\toprule
\\textbf{ULA}       & \\textbf{\\name-Mem} & \\textbf{\\name}       \\\\
\\midrule
"""

footer ="""\\bottomrule
\\end{tabular}
"""

for machine in machinesList:

    # try:
    file = "plots/microbenchmark/tab/table_grid_"+machine+".csv"
    
    # print(d)
    with open("plots/tables/grid_"+machine+".tex", "w") as f:

        f.write(header)

        d = parse(file)
        # print(d)
        s = make_tex_table(d)
        f.write(s)
        f.write(footer)

