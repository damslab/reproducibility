import numpy as np
import os


def parsePython(file):
    readTime = []
    endTime = []
    progTime = []
    if os.path.exists(file):
        with open(file) as f:
            for l in f:
                if "readTime:" in l: 
                    readTime.append(float(l.split(":")[1].strip().split(" ")[0]))
                elif "endTime:" in l: 
                    endTime.append(float(l.split(":")[1].strip().split(" ")[0]))
                elif "seconds time elapsed" in l:
                    progTime.append(float(l.strip().split(" ")[0]))

    return progTime, readTime, endTime
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
                    if time[-1] > 3000:  # Timeout
                        return (
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
                    transformEncode.append(float(l[21:32].strip()))
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
                    return [], [], [], 
                if "Exception in thread" in l:
                    return [], [], [], 
                if "org.apache.sysds.runtime.DMLRuntimeException" in l:
                    return [], [], [], 

    if len(sysdstime) == 0:
        return [], [], [], 
    return (
        # stringSize,
        # schemaSize,
        # orgDiskSize,
        # diskSchemaSize,
        time,
        # sysdstime,
        # sysCompile,
        # sysExec,
        readTime,
        transformEncode,
        # detectSchema,
        # applySchema,
        # ratio,
        # teSize,
        # compRatio,
        # sparseSize,
        # denseSize,
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


# data = [
#     "adult",
#     "cat",
#     "kdd",
#     "salaries",
#     "santander",
#     "home",
#     "criteo",
#     "crypto",
# ]
# datareg = ["kdd", "crypto", "salaries"]
# databin = ["adult", "cat", "santander", "home", "criteo"]
machines = ["XPS-15-7590", "dams-su1"]
# machines = ["dams-su1"]

# confs = ("ULAb16", "TAWAb16")

# lossy = (
#     "full",
#     "l10",
# )

mkdir("./plotting/tables/25-others")
# inputFileType = (".bin", ".cla")

baseAlg = ["comp", "def", "pd", "pl", "sk", "tf", "tra"]


data = ["100000", "1000000","10000000", "100000000"]
this = "plotting/scripts/table_25_others.py"

# experiments/results/algorithms/dams-su1

# experiments/results/otherSystems/dams-su1/comp/criteo_full-criteo-day_0_1000000.tsv-TAWAb16.log

for m in machines:
    out = "plotting/tables/25-others/" + m + ".csv"
    print("TableScript:", this, "out:", out)
    with open(out, "w") as cv:
        ## Header
        cv.write("name,")
        cv.write("alg,")
        cv.write("Time,ReadTime,TE")
        cv.write("\n")

        ## Data:
        basis =  "results/otherSystems/" + m 
        for d in data:
            for alg in baseAlg:
                baseAlgPath = basis + "/" + alg + "/criteo_full-criteo-day_0_"
                path = baseAlgPath + d + ".tsv.log"

                if os.path.exists(path):
                    a = parsePython(path)
                    if len(a[0]) > 0:
                        cv.write(d)
                        cv.write(",")
                        cv.write(alg)
                        cv.write(",")
                        writeArr(cv, a)
                        cv.write("\n")

                path = baseAlgPath + d + ".tsv-TAWAb16.log"

                if os.path.exists(path):
                    a = parse(path)
                    if len(a[0]) > 0:
                        cv.write(d)
                        cv.write(",")
                        cv.write(alg + "TAWAb16")
                        cv.write(",")
                        writeArr(cv, a)
                        cv.write("\n")


                path = baseAlgPath + d + ".tsv-ULAb16.log"

                if os.path.exists(path):
                    a = parse(path)
                    if len(a[0]) > 0:
                        cv.write(d)
                        cv.write(",")
                        cv.write(alg + "ULAb16")
                        cv.write(",")
                        
                        writeArr(cv, a)
                        cv.write("\n")
