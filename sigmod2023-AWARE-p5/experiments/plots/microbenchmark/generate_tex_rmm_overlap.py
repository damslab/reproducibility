import os

import argparse


def flo3(f):
    return '\\numprint{' + "{0:0.3f}".format(f) + "}"


def flo1(f):
    return '\\numprint{' + "{0:0.1f}".format(f) + "}"


def flo2(f):
    return '\\numprint{' + "{0:0.2f}".format(f) + "}"


def inte(f):
    return '\\numprint{' + "{0:0.0f}".format(f) + "}"


def parse(file):

    row = {
        "ula-sysmlb16-singlenode-sysml": 0,
        "cla-sysmlb16-singlenode-sysml": 1,
           "ulab16-singlenode": 2, 
           "claWorkloadb16NoOL-singlenode":3,
           "clab16-singlenode":4,
           "claWorkloadb16-singlenode": 5}

    # row = {"airlines": 0,
    #        "amazon": 1,
    #        "covtypeNew": 2,
    #        "infimnist_1m": 3,
    #        "census": 4,
    #        "census_enc": 5,
    #        }

    # data = {"ulab16-hybrid": 0, "claWorkloadb16-hybrid": 1}
    matrix = [["" for _ in range(5)] for _ in range(6)]

    matrix[0][0] = 'SystemML - ULA          '
    matrix[1][0] = 'SystemML - CLA'
    matrix[2][0] = 'SystemDS - ULA          '
    matrix[3][0] = '\\name-No OL  '
    matrix[4][0] = '\\name-Mem  '
    matrix[5][0] = '\\name        '

    with open(file) as f:
        firstLine = True
        l = ""
        for line in f:
            if firstLine:
                firstLine = False
                continue

            parts = [x.strip() for x in line.split(",")]
            r_id = parts[2]
            # t = parts[3]
            # c_id = parts[1]

            if r_id in row and len(parts) > 4:
                r = row[r_id]
                # c = col[c_id]
                multtime = float(parts[3])
                rep = float(parts[4])
                repExtra = rep / 11
                if repExtra > 1:
                    rep = rep / repExtra
                io = float(parts[5])
                comp = float(parts[6]) - io
                total = float(parts[7])

                matrix[r][1] = flo2(io) + " sec"
                if comp <= 0:
                    matrix[r][2] = "---"
                else:
                    matrix[r][2] = flo2(comp) + " sec"
                matrix[r][3] = flo2(multtime * rep / 1000) + " sec"
                matrix[r][4] = flo2(total) + " sec"
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


header = """\\begin{tabular}{r|r|r|r|r}
\\toprule
            & \\textbf{I/O}      & \\textbf{Comp}       & \\textbf{RMM}         & \\textbf{Total}       \\\\
\\midrule
"""

footer = """\\bottomrule
\\end{tabular}
"""

for machine in machinesList:
    file = "plots/microbenchmark/tab/table_512_seqmmr+_"+machine+".csv"
    with open("plots/tables/overlap_sequence_"+machine+".tex", "w") as f:
        f.write(header)
        d = parse(file)
        s = make_tex_table(d)
        f.write(s)
        f.write(footer)

        # f.write('\\bottomrule\n')
        # f.write('\\end{tabular}\n')
