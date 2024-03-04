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
    ratio = []

    teSize = []
    compRatio = []
    sparseSize = []
    denseSize = []
    normal_compressionTime =[]


    emptyReturn = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
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
                    if time[-1] > 1000:  # Timeout
                        return emptyReturn

                if "Cache times (ACQr/m, RLS, EXP):" in l:
                    readTime.append(float(l.strip()[31:].split("/")[0]))
                if "Total elapsed time:" in l:
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
                if "CLA Compression Phases :" in l:
                    # CLA Compression Phases :	0.096/1.108/0.034/0.132/0.001/0.000
                    parts = np.sum([float(x) for x in l.split(":")[1].strip().split("/")])
                    normal_compressionTime.append(parts)
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
                    return emptyReturn
                if "Exception in thread" in l:
                    return emptyReturn
                if "org.apache.sysds.runtime.DMLRuntimeException" in l:
                    return emptyReturn

    if len(sysdstime) == 0:
        return emptyReturn
    return (
        stringSize,
        schemaSize,
        ratio,
        orgDiskSize,
        diskSchemaSize,
        time,
        sysdstime,
        sysCompile,
        sysExec,
        readTime,
        transformEncode,
        teSize,
        normal_compressionTime,
        compRatio,
        sparseSize,
        denseSize,
    )


# results/ReadRealFrame/XPS-15-7590/FM--adult-cf.log
data = ["adult", "cat", "kdd", "salaries", "santander", "home", "criteo", "crypto"]
machines = ["XPS-15-7590", "dams-su1"]
lossy = ["l0","l0.6", "l1", "l2", "l3", "l5", "l10", "l20", "l40", "l80", "l160", "l320", "l640", "l1280", "l2560"]


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


mkdir("./plotting/tables/te")

for m in machines:
    with open("plotting/tables/te/" + m + "_lossy.csv", "w") as cv:
        cv.write("name,lossy,")
        cv.write(
            "StringSize,SchemaSize,SchemaRatio,OrgDiskSize,FMDiskSize,FMTime,FMSysDSTime,FMCompile,FMExec,FMRead,FMTE,FMSize,"
        )
        cv.write(
            "CFCMCDDiskSize,CFCMCDTime,CFCMCDSysDSTime,CFCMCDCompile,CFCMCDExec,CFCMCDRead,CFCMCDTE,CFCMCDSize,CFCMCDCompTime,CFCMCDCompSize,CFCMCDSparseSize,CFCMCDDenseSize,"
        )
        cv.write(
            "CFMCMCDDiskSize,CFMCMCDTime,CFMCMCDSysDSTime,CFMCMCDCompile,CFMCMCDExec,CFMCMCDRead,CFMCMCDTE,CFMCMCDSize,CFMCMCDCompTime,CFMCMCDCompSize,CFMCMCDSparseSize,CFMCMCDDenseSize"
        )
       
        cv.write("\n")

        for d in data:
            for l in lossy:
                a =parse("results/TE_lossy/" + m + "/E-" + d + "-FM-"+l+".log")[:-4]
                if len(a[0]) > 0:
                   cv.write(d)
                   cv.write(",")
                   cv.write(l)
                   cv.write(",")
                   writeArr(cv, a)
                   cv.write(",")
                   writeArr(cv, parse("results/TE_lossy/" + m + "/E-" + d + "-CFCMCD-"+l+".log")[4:])
                   cv.write(",")
                   writeArr(cv, parse("results/TE_lossy/" + m + "/E-" + d + "-CFMCMCD-"+l+".log")[4:])
                   cv.write("\n")
