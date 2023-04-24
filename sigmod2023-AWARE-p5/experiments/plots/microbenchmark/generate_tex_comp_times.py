import os

import argparse


def flo(f):
    return '\\numprint{' + "{0:0.2f}".format(f) + "}"


def inte(f):
    return '\\numprint{' + "{0:0.0f}".format(f) + "}"


def parse(file):

    col = {"cla-sysml-singlenode-sysml": 1,
           "clab16-singlenode": 3, "claWorkloadb16-singlenode": 5}

    row = {"airlines": 0,
           "amazon": 1,
           "covtypeNew": 2,
           "infimnist_1m": 3,
           "census": 4,
           "census_enc": 5,
           }

    # data = {"ulab16-hybrid": 0, "claWorkloadb16-hybrid": 1}
    matrix = [["" for i in range(7)] for j in range(len(row))]

    matrix[0][0] = 'Airline78      '
    matrix[1][0] = 'Amazon         '
    matrix[2][0] = 'Covtype        '
    matrix[3][0] = 'Mnist1m        '
    matrix[4][0] = 'US Census      '
    matrix[5][0] = 'US Census Enc  '

    with open(file) as f:
        firstLine = True
        l = ""
        for line in f:
            if firstLine:
                firstLine = False
                continue

            parts = [x.strip() for x in line.split(",")]
            r_id = parts[0]
            # t = parts[3]
            c_id = parts[1]

            if r_id in row and c_id in col and len(parts) > 4:
                r = row[r_id]
                c = col[c_id]
                comp = float(parts[3]) / 1000
                matrix[r][c] = flo(comp) + " sec"
                ratio = float(parts[7])
                matrix[r][c+1] = flo(ratio)
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

for machine in machinesList:
    file = "plots/microbenchmark/tab/table_compress_"+machine+".csv"
    with open("plots/tables/compress_"+machine+".tex", "w") as f:
        f.write('\\begin{tabular}{r|rr|rr|rr}\n')
        f.write('\\toprule\n')

        f.write(
            '\\textbf{Dataset} & \\multicolumn{2} {c|}{\\textbf{CLA}} & \\multicolumn{2}{c|}{\\textbf{\\name-Mem}} & \\multicolumn{2}{c}{\\textbf{\\name}} \\\\\n')
        f.write('& \\multicolumn{1} {c}{time}                                     & \\multicolumn{1} {c|}{ratio}             & \\multicolumn{1} {c}{time}          & \\multicolumn{1} {c|}{ratio} & \\multicolumn{1} {c}{time} & \\multicolumn{1} {c}{ratio} \\\\\n')

        f.write('\\midrule\n')
        d = parse(file)



        # d[1][1] = "Hello"
        # d[1][2] = d[1][3]
        # d[1][3] = d[1][4]
        d[1][1] =  "\\multicolumn{2} {c|}{\\numprint{ 37.6} \\textit{hours Crash}  } "

        d[1][5] =  " \\numprint{  3.77} sec "
        d[1][6] =  " \\textit{Abort} "

        s = make_tex_table(d)

        # s = s.replace("Amazon          &\t &\t &\t &\t &\t &\t ","""Amazon & \\multicolumn{2} {c|}{\\numprint{ 37.6} \\textit{hours Crash}  } & \\numprint{  8.60} sec & \\numprint{  1.67} & \\numprint{  4.11} sec & \\textit{Abort} """)
        
        f.write(s)
        f.write('\\bottomrule\n')
        f.write('\\end{tabular}\n')
