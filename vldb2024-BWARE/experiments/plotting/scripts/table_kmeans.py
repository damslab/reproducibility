import os
import numpy as np


def parse(p):
    if os.path.isfile(p):
        # print(p)
        #   skipp = 10
        time = []

        sysdstime = []
        sysCompile = []
        sysExec = []

        alg = []
        comp = []
        te = []

        with open(p) as f:
            for l in f:
                #  if "SystemDS Statistics" in l:
                #      skipp = skipp + 20
                #  if skipp > 0:
                #      skipp = skipp - 1
                #      continue
                if "DEBUG" in l:
                    continue
                if "seconds time elapsed" in l:
                    if "," in l:
                        l = l.replace(",", ".")
                    time.append(float(l.strip().split(" ", 1)[0]))
                #  if "END DML run" in l:
                #    break
                if "m_kmeans   " in l:
                    alg.append(
                        float(
                            l.strip()
                            .split("m_kmeans")[1]
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
                if "Total elapsed time:" in l:
                    sysdstime.append(float(l.strip().split(":")[1].split("sec")[0]))
                if "Total compilation time:" in l:
                    sysCompile.append(float(l.strip().split(":")[1].split("sec")[0]))
                if "Total execution time:" in l:
                    sysExec.append(float(l.strip().split(":")[1].split("sec")[0]))
                if "Caused by: " in l:
                    return [-2], [-2], [-2], [-2], [-2], [-2], [-2]

            #  print(l)
        return time, sysdstime, sysCompile, sysExec, alg, comp, te
    return [-1], [-1], [-1], [-1], [-1], [-1], [-1]


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


base = "results/e2e/criteo_kmeans/code/conf/"
types = ["TAWAb1", "ULAb1", "TCLAb1", "TULAb1"]
sizes = [
    "1000",
    "10000",
    "100000",
    "300000",
    "1000000",
    "3000000",
    "10000000",
    "30000000",
    "100000000",
    "",
]
data = "data-criteo-day_0_"
machines = ["dams-su1", "XPS-15-7590"]

mkdir("./plotting/tables")
mkdir("./plotting/tables/kmeans/")
mkdir("./plotting/tables/kmeans/criteo")

for m in machines:
    with open("plotting/tables/kmeans/criteo/log_" + m + ".csv", "w") as cv:
        cv.write(
            "Type,Size,Time,SysDSTime,Compile,Exec,Alg,Compress,Transform\n"
        )
        for t in types:
            #   ts = base + t + ".xml/singlenode/dams-su1/data-criteo-day_0_"
            ts = base + t + ".xml/singlenode/" + m + "/data-criteo-day_0_"
            for s in sizes:
                tss = ts + s + ".tsv_code-scripts-specs-criteo_full.json.log"
                data = parse(tss)
                cv.write(t)
                cv.write(",")
                if len(s) == 0:
                    cv.write("195841983")
                else:
                    cv.write(s)
                cv.write(",")
                for idx, x in enumerate(data):
                    if len(x) == 0:
                        cv.write("NA")
                    else:
                        cv.write(str(sum(x) / len(x)))
                    if idx < len(data) - 1:
                        cv.write(",")
                cv.write("\n")
