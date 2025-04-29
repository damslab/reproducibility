import numpy as np
import os


def parse(file):
    stringSize = []
    schemaSize = []
    diskSchemaSize = []
    orgDiskSize = []

    sysdstime = []
    sysCompile = []
    sysExec = []
    time = []

    readTime = []
    transformEncode = []
    applySchema = []
    detectSchema = []
    ratio = []

    teSize = []
    compRatio = []
    sparseSize = []
    denseSize = []

    tmptmp = False
    if os.path.exists(file):
        with open(file) as f:
            for l in f:
                if "\tdata/" in l:
                    if ".tmp.tmp" in l:
                        tmptmp = True
                    if ".mtd" in l:
                        continue
                    elif (tmptmp and ".tmp.tmp" in l) or (not tmptmp and ".tmp" in l):
                        diskSchemaSize.append(int(l.split("\t")[0]) * 1024)
                    else:
                        orgDiskSize.append(int(l.split("\t")[0]) * 1024)
                if "seconds time elapsed" in l:
                    if "," in l:
                        l = l.replace(",", ".")
                    time.append(float(l.strip().split(" ", 1)[0]))
                    if time[-1] > 100000:  # Timeout
                        return (
                            [],
                            [],
                            [],
                            [],
                            [],
                            [-1],
                            [-1],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                        )

                if "Cache times (ACQr/m, RLS, EXP):" in l:
                    readTime.append(float(l.strip()[31:].split("/")[0]))
                if "Total elapsed time:" in l:
                    # print(l, float(l.strip().split(":")[1].split("sec")[0]))
                    sysdstime.append(float(l.strip().split(":")[1].split("sec")[0]))
                if "Total compilation time:" in l:
                    sysCompile.append(float(l.strip().split(":")[1].split("sec")[0]))
                if "Total execution time:" in l:
                    sysExec.append(float(l.strip().split(":")[1].split("sec")[0]))
                if "DEBUG lib.FrameLibApplySchema: Schema Apply Input Size:" in l:
                    stringSize.append(int(l[74:].strip()))
                if "DEBUG lib.FrameLibApplySchema:             Output Size:" in l:
                    schemaSize.append(int(l[74:].strip()))
                if "DEBUG lib.FrameLibApplySchema:             Ratio      :" in l:
                    ratio.append(float(l[74:].strip()))
                if " transformencode  " in l:
                    transformEncode.append(float(l[22:32].strip()))
                if "  applySchema   " in l:
                    applySchema.append(
                        float(l.split("applySchema")[1].strip().split(" ")[0])
                    )
                if "  detectSchema  " in l:
                    detectSchema.append(
                        float(l.split("detectSchema")[1].strip().split(" ")[0])
                    )
                if (
                    "DEBUG encode.MultiColumnEncoder: Transform Encode output mem size: "
                    in l
                ):
                    teSize.append(float(l[85:].strip()))
                if (
                    "DEBUG encode.CompressedEncode: Compressed transform encode size:  "
                    in l
                ):
                    teSize.append(float(l[85:].strip()))
                if "compress.CompressedMatrixBlockFactory: --compressed size:" in l:
                    compRatio.append(float(l[84:].strip()))
                if "DEBUG compress.CompressedMatrixBlockFactory: --sparse size:" in l:
                    sparseSize.append(float(l[80:].strip()))
                if "DEBUG compress.CompressedMatrixBlockFactory: --dense size:" in l:
                    denseSize.append(float(l[80:].strip()))
                if "Killed              " in l:
                    return [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
                if "Exception in thread" in l:
                    return [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
                if "org.apache.sysds.runtime.DMLRuntimeException" in l:
                    return [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

    if len(sysdstime) == 0:
        return [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
    return (
        # stringSize,
        # schemaSize,
        # orgDiskSize,
        # diskSchemaSize,
        time,
        sysdstime,
        sysCompile,
        sysExec,
        readTime,
        transformEncode,
        detectSchema,
        applySchema,
        ratio,
        teSize,
        compRatio,
        sparseSize,
        denseSize,
    )


def writeDetCom(cv, detect, compress):
    if len(detect[1]) == 0 or len(compress[0]) == 0:
        writeArr(cv, [[]])
        return
    sizeDetect = sum(detect[1]) / len(detect[1])
    sizeCompress = sum(compress[0]) / len(compress[0])

    c = sizeDetect / sizeCompress
    writeArr(cv, [[c]])


def writeArr(cv, data):
    for idx, x in enumerate(data):
        if len(x) == 0:
            cv.write("NA")
        else:
            cv.write(str(sum(x) / len(x)))
        if idx < len(data) - 1:
            cv.write(",")


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


data = [
    "adult",
    "cat",
    "kdd",
    "salaries",
    "santander",
    "home",
    "criteo-day_0_10000000",
    "crypto",
]
datareg = ["kdd", "crypto", "salaries"]
databin = ["adult", "cat", "santander", "home", "criteo"]
machines = ["XPS-15-7590", "dams-su1"]

confs = ("ULAb16", "TAWAb16")
# confs = ("ULAb16", "TAWAb16")

lossy = (
    "full",
    "l1",
    "l2",
    "l3",
    "l5",
    "l10",
    "l20",
    "l40",
    "l80",
    "l160",
    "l320",
    "l640",
    "l1280",
    "l2560",
)
# l1 l2 l3 l5 l10 l20 l40 l80 l160 l320 l640 l1280 l2560

mkdir("./plotting/tables/21-scaling")
inputFileType = (".bin", ".cla")


# results/lossy_alg/dams-su1/regress_lm/code/conf/TAWAb16.xml/singlenode/data-crypto-train.csv_code-scripts-specs-crypto_l1.json.log02-04-24-12:51:21 AM.log

for m in machines:
    baseRegression = "results/lossy_scaling/" + m + "/regress_lm/code/conf/"
    baseClassification = "results/lossy_scaling/" + m + "/binary_lm_1/code/conf/"
    baseClassification2 = "results/lossy_scaling/" + m + "/binary_lm_last/code/conf/"
    out = "plotting/tables/21-scaling/" + m + ".csv"
    print("TableScript:", "plotting/scripts/table_21_scaling.py", "out:", out)
    with open(out, "w") as cv:
        cv.write("name,")
        cv.write("Conf,lossy,FileType,")
        cv.write("FullName,")
        cv.write(
            "Time,SysDSTime,Compile,Exec,Read,TE,DetectSchema,ApplySchema,Ratio,TESize,CompRatio,SparseSize,DenseSize"
        )

        cv.write("\n")
        for d in datareg:
            dd = d
            if "kdd" in d:
                ddd = "kdd98-cup98lrn"
            else:
                ddd = d + "-train"

            for c in confs:

                for ft in inputFileType:
                    if ft == ".bin" and c != "ULAb16":
                        continue
                    if ft == ".cla" and c != "TAWAb16":
                        continue
                    for l in lossy:
                        path = (
                            baseRegression
                            + c
                            + ".xml/singlenode/data-"
                            + ddd
                            + ".csv"
                            + ft
                            + "_code-scripts-specs-"
                            + dd
                            + "_"
                            + l
                            + ".json.log"
                        )
                        # if "kdd" in path:
                        #     print(path)
                        # print(path)
                        if os.path.exists(path):
                            # print(path)

                            a = parse(path)
                            if len(a[0]) > 0:
                                cv.write(d)
                                cv.write(",")
                                cv.write(c)
                                cv.write(",")
                                cv.write(l)
                                cv.write(",")
                                if ft == "":
                                    cv.write("str")
                                else:
                                    cv.write(ft[1:])
                                cv.write(",")
                                writeArr(cv, a)
                                cv.write("\n")
                            # else:
                            #     print("Failed: " + path)
                        # else:
                        # print("Not exists:" + path)

        for d in databin:
            dd = d
            if "adult" in d:
                ddd = "adult-adult.csv"
            elif "criteo" in d:
                ddd = "criteo-day_0_10000000.tsv"
            else:
                ddd = d + "-train.csv"

            if "cat" in dd:
                dd = "catindat"
            for ddd in [
                "criteo-day_0_1000.tsv",
                "criteo-day_0_10000.tsv",
                "criteo-day_0_100000.tsv",
                "criteo-day_0_1000000.tsv",
                "criteo-day_0_10000000.tsv",
                "criteo-day_0_100000000.tsv",
                "criteo-day_0.tsv",
            ]:
                for c in confs:
                    for ft in inputFileType:
                        if ft == ".bin" and c != "ULAb16":
                            continue
                        if ft == ".cla" and c != "TAWAb16":
                            continue
                        for l in lossy:
                            path = (
                                baseClassification
                                + c
                                + ".xml/singlenode/data-"
                                + ddd
                                + ft
                                + "_code-scripts-specs-"
                                + dd
                                + "_"
                                + l
                                + ".json.log"
                            )
                            if (
                                not os.path.exists(path)
                                or "-cat-" in path
                                or "-adult-" in path
                            ):
                                path = (
                                    baseClassification2
                                    + c
                                    + ".xml/singlenode/data-"
                                    + ddd
                                    + ft
                                    + "_code-scripts-specs-"
                                    + dd
                                    + "_full.json.log"
                                )

                            if os.path.exists(path):

                                a = parse(path)
                                if len(a[0]) > 0:
                                    cv.write(d)
                                    cv.write(",")
                                    cv.write(c)
                                    cv.write(",")
                                    cv.write(l)
                                    cv.write(",")
                                    if ft == "":
                                        cv.write("str")
                                    else:
                                        cv.write(ft[1:])
                                    cv.write(",")
                                    cv.write(ddd)
                                    cv.write(",")
                                    writeArr(cv, a)
                                    cv.write("\n")
                                else:
                                    print("Failed: " + path)
                            # else:
                            # print(path)
