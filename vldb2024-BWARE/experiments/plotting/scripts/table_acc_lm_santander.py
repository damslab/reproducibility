import os
import numpy as np


def parse(p):
    if os.path.isfile(p):
        time = []
        acc = False
        sysdstime = []
        sysCompile = []
        sysExec = []

        alg = []
        comp = []
        te = []
        auc = []
        accuracy = []

        with open(p) as f:
            for l in f:
                if "Computing the statistics..." in l:
                    stringFound = True
                # if stringFound:
                if acc:
                    acc = False
                    accuracy.append(float(l.strip()))
                    continue
                if "AUC:" in l:
                    auc.append(float(l.split(":")[1].strip()))
                if "Total elapsed time:" in l:
                    sysdstime.append(float(l.strip().split(":")[1].split("sec")[0]))
                if "Total compilation time:" in l:
                    sysCompile.append(
                        float(l.strip().split(":")[1].split("sec")[0])
                    )
                if "Total execution time:" in l:
                    sysExec.append(float(l.strip().split(":")[1].split("sec")[0]))
                if "Caused by: " in l:
                    return [-2], [-2], [-2], [-2], [-2], [-2], [-2], [-2], [-2]
                if "Accuracy:" in l:
                    acc = True
                if "seconds time elapsed" in l:
                    if "," in l:
                        l = l.replace(",", ".")
                    time.append(float(l.strip().split(" ", 1)[0]))
                if "m_lmCG   " in l:
                    alg.append(
                        float(
                            l.strip()
                            .split("m_lmCG")[1]
                            .strip()
                            .split(" ", 1)[0]
                            .replace(",", "")
                        )
                    )
                if "compress  " in l:
                    comp.append(
                        float(
                            l.strip()
                            .split("compress")[1]
                            .strip()
                            .split(" ", 1)[0]
                            .replace(",", "")
                        )
                    )
                if "transformencode  " in l:
                    te.append(
                        float(
                            l.strip()
                            .split("transformencode")[1]
                            .strip()
                            .split(" ", 1)[0]
                            .replace(",", "")
                        )
                    )

        return time, sysdstime, sysCompile, sysExec, alg, comp, te, auc, accuracy

    return [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1]


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


mkdir("./plotting/tables")
mkdir("./plotting/tables/lm/")
mkdir("./plotting/tables/lm/santander")


base = "results/e2e/santander_"

aug = ["lm", "lm_2", "lm_3", "lm_4", "lm_5", "lm_6", "lm_7", "lm_8", "lm_9", "lm_10"]


e = "/code/conf/"
aa = "b1.xml/singlenode/"
ext = ["ULA", "TAWA"]


f = "/data-santander-train.csv_code-scripts-specs-santander_"

spec = ["pass", "spec_eqh5", "spec_eqh10", "spec_eqh50", "spec_eqh100", "spec_eqh255"]


machines = ["dams-su1", "XPS-15-7590", "dams-so002"]

for m in machines:
    with open("plotting/tables/lm/santander/log_" + m + ".csv", "w") as cv:
        cv.write(
            "aug,spec,conf,Time,SysDSTime,Compile,Exec,Alg,Compress,Transform,AUC,Accuracy\n"
        )
        for ex in ext:
            for a in aug:
                for s in spec:
                    p = base + a + e + ex + aa + m + f + s + ".json.log"
                    data = parse(p)
                    cv.write(a)
                    cv.write(",")
                    cv.write(s)
                    cv.write(",")
                    cv.write(ex)
                    cv.write(",")
                    for idx, x in enumerate(data):
                        if len(x) == 0:
                            cv.write("NA")
                        else:
                            cv.write(str(sum(x) / len(x)))
                        if idx < len(data) - 1:
                            cv.write(",")
                    cv.write("\n")
