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
    row = {
        "census_enc_16k": 0,
        "census_enc_8x_16k": 1,
        "census_enc_16x_16k": 2,
        "census_enc_32x_16k": 3,
        "census_enc_128x_16k": 4}
    data = {"ulab16-hybrid": 0, "claWorkloadb16-hybrid": 1}

    matrix = [["" for i in range(len(col) * 2 + 1)] for j in range(len(row))]

    matrix[0][0] = "1x"
    matrix[1][0] = "8x"
    matrix[2][0] = "16x"
    matrix[3][0] = "32x"
    matrix[4][0] = "128x"

    with open(file) as f:
        firstLine = True
        l = ""
        for line in f:
            if firstLine:
                firstLine = False
                continue

            parts = [x.strip() for x in line.split(",")]
            r_id = parts[0]
            t = parts[3]
            c_id = parts[1]
            if t != "nan" and r_id in row and c_id in col and parts[2] in data:

                r = row[r_id]

                c = col[c_id] + data[parts[2]]
                v = float(parts[3])
                # if (v > 100):
                matrix[r][c] = flo(v)
                # else:
                    # matrix[r][c] = inte(v)

                if len(parts) == 9:
                    matrix[r][c] = "\\dist" + matrix[r][c]
                comp = float(parts[6])
                if comp > 0 and comp - float(parts[5]) > 0:
                    matrix[r][c] = "("+inte(comp -
                                            float(parts[5]))+") " + matrix[r][c]
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

for machine in machinesList:
    # try:
    file = "plots/microbenchmark/tab/table_algs_v2_"+machine+".csv"
    # print(d)
    with open("plots/tables/scaleup_"+machine+".tex", "w") as f:

        f.write('\\begin{tabular}{r|rr|rr|rr}\n')
        f.write('\\toprule\n')
        f.write('\\headendtoendone\n')
        f.write('\\midrule\n')
        f.write('\\subhead\n')
        f.write('\\midrule\n')

        d = parse(file)
        s = make_tex_table(d)
        f.write(s)

        f.write('\\midrule\n')
        f.write('\\midrule\n')
        f.write('\\headendtoendtwo\n')
        f.write('\\midrule\n')
        f.write('\\subhead\n')
        f.write('\\midrule\n')

        d = parse(file, col={"lmCG+": 1, "lmDS+": 3, "l2svm+": 5})
        s = make_tex_table(d)
        f.write(s)

        f.write('\\bottomrule\n')
        f.write('\\end{tabular}\n')

    # except:
    # continue
