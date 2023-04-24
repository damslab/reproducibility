import os

def parse(file):

    col = {"kmeans+": 1, "PCA+": 3, "mLogReg+": 5,
           "lmCG+": 7, "lmDS+": 9, "l2svm+": 11}
    row = {"census_enc_16k": 0, "census_enc_8x_16k": 1, "census_enc_16x_16k": 2,
           "census_enc_32x_16k": 3, "census_enc_128x_16k": 4}
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
            if t != "nan":
                if r_id in row:
                    c_id = parts[1]
                    r = row[r_id]
                    if c_id in col:
                        c = col[c_id] + data[parts[2]]
                        v = float(parts[3])
                        if(v > 100):
                            matrix[r][c] = '\\numprint{' + \
                                "{0:0.0f}".format(float(parts[3])) + "}"
                        else:
                            matrix[r][c] = '\\numprint{' + \
                                "{0:0.1f}".format(float(parts[3])) + "}"

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
        if idx == 1 or idx == 4:
            s += "\\midrule\n"
    return s



machine = "dams-so001"
file = "plots/microbenchmark/table_algs_v2_"+machine+".csv"
with open("plots/tables/end_to_end_table.tex", "w") as f:
    d = parse(file)
    s = make_tex_table(d)
    f.write(s)


def parsComp(path):
    data = {}
    first_line = True
    if os.path.isfile(path):
        with open(path) as f:
            for line in f:
                if first_line:
                    first_line = False
                    continue
                split = [x.strip() for x in line.split(",")]
                ex = split[0]
                if ex not in data.keys():
                    data[ex] = []
                if "No File at" in line or "Failed Parsing" in line:
                    data[ex].append(("nan", "nan"))
                else:
                    data[ex].append((float(split[3]), float(split[7])))

    return data

with open("plots/tables/compress.tex", "w") as f:
    d = parsComp("plots/microbenchmark/table_compress.csv")
    names = [
        ("airlines", "Airline78"),
        ("amazon", "Amazon"),
        ("covtypeNew", "Covtype"),
        ("infimnist_1m", "Mnist1m"),
        ("census", "US Census"),
        ("census_enc", "US Census Enc")
    ]
    if d is not {}:
        nps = "\\numprint{"
        npe = "}"
        for n in names:
            f.write("{0:20s} ".format(n[1]))
            pairs = d[n[0]]
            for t in pairs:
                if(t[0]) == "nan":
                    f.write("& NA & NA")
                else:
                    f.write(" & {0}{1:6.2f}{2} s & {3}{4:6.2f}{5} ".format(
                        nps, t[0]/1000, npe, nps, t[1], npe))
            f.write("\\\\\n")


with open("plots/tables/compress_small.tex", "w") as f:
    d = parsComp("plots/microbenchmark/table_compress.csv")
    names = [
        ("airlines", "Airline78"),
        ("amazon", "Amazon"),
        ("covtypeNew", "Covtype"),
        ("infimnist_1m", "Mnist1m"),
        ("census", "US Census"),
        ("census_enc", "US Census Enc")
    ]
    if d is not {}:
        nps = "\\numprint{"
        npe = "}"
        for n in names:
            f.write("{0:20s} ".format(n[1]))
            pairs = d[n[0]]
            for idt, t in enumerate(pairs):
                if idt == 2 or idt >= 4:
                    continue
                if(t[0]) == "nan":
                    f.write("& NA & NA")
                else:
                    f.write(" & {0}{1:6.2f}{2} s & {3}{4:6.2f}{5} ".format(
                        nps, t[0]/1000, npe, nps, t[1], npe))
            f.write("\\\\\n")


with open("plots/tables/compress_xps.tex", "w") as f:
    d = parsComp("plots/microbenchmark/table_compress_all_xps.csv")
    names = [
        ("airlines", "Airline78"),
        ("amazon", "Amazon"),
        ("covtypeNew", "Covtype"),
        ("infimnist_1m", "Mnist1m"),
        ("census", "US Census"),
        ("census_enc", "US Census Enc")
    ]
    if d is not {}:
        nps = "\\numprint{"
        npe = "}"
        for n in names:
            f.write("{0:20s} ".format(n[1]))
            pairs = d[n[0]]
            for t in pairs:
                if(t[0]) == "nan":
                    f.write("& NA & NA")
                else:
                    f.write(" & {0}{1:6.2f}{2} s & {3}{4:6.2f}{5} ".format(
                        nps, t[0]/1000, npe, nps, t[1], npe))
            f.write("\\\\\n")


with open("plots/tables/compress_small_xps.tex", "w") as f:
    d = parsComp("plots/microbenchmark/table_compress_all_xps.csv")
    names = [
        ("airlines", "Airline78"),
        ("amazon", "Amazon"),
        ("covtypeNew", "Covtype"),
        ("infimnist_1m", "Mnist1m"),
        ("census", "US Census"),
        ("census_enc", "US Census Enc")
    ]
    if d is not {}:
        nps = "\\numprint{"
        npe = "}"
        for n in names:
            f.write("{0:20s} ".format(n[1]))
            pairs = d[n[0]]
            for idt, t in enumerate(pairs):
                if idt == 2 or idt >= 4:
                    continue
                if(t[0]) == "nan":
                    f.write("& NA & NA")
                else:
                    f.write(" & {0}{1:6.2f}{2} s & {3}{4:6.2f}{5} ".format(
                        nps, t[0]/1000, npe, nps, t[1], npe))
            f.write("\\\\\n")
