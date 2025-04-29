import numpy as np
import os


def parseCompress(file):
    ucSize = []
    cSize = []
    ratio = []
    diskCompressed = []
    orgDiskSize = []
    sysdstime = []
    sysCompile = []
    sysExec = []
    time = []

    readTime = []
    writeTime = []
    if os.path.exists(file):
        with open(file) as f:
            for l in f:
                if "\tdata/" in l:
                    if ".mtd" in l:
                        continue
                    elif ".dict" in l:
                        diskCompressed[-1] += int(l.split("\t")[0]) * 1024
                    elif ".tmp" in l:
                        diskCompressed.append(int(l.split("\t")[0]) * 1024)
                    else:
                        orgDiskSize.append(int(l.split("\t")[0]) * 1024)
                if "seconds time elapsed" in l:
                    if "," in l:
                        l = l.replace(",", ".")
                    time.append(float(l.strip().split(" ", 1)[0]))

                if "Cache times (ACQr/m, RLS, EXP):" in l:
                    readTime.append(float(l.strip()[31:].split("/")[0]))
                    writeTime.append(float(l.strip()[31:].split("/")[3].split(" ")[0]))
                if "Total elapsed time:" in l:
                    sysdstime.append(float(l.strip().split(":")[1].split("sec")[0]))
                if "Total compilation time:" in l:
                    sysCompile.append(float(l.strip().split(":")[1].split("sec")[0]))
                if "Total execution time:" in l:
                    sysExec.append(float(l.strip().split(":")[1].split("sec")[0]))
                if "compress.CompressedFrameBlockFactory: Uncompressed Size:" in l:
                    ucSize.append(int(l.split(":")[-1].strip()))
                elif "compress.CompressedFrameBlockFactory: compressed Size: " in l:
                    cSize.append(int(l.split(":")[-1].strip()))
                elif "compress.CompressedFrameBlockFactory: ratio:          " in l:
                    ratio.append(float(l.split(":")[-1].strip()))

    return (
        ucSize,
        cSize,
        ratio,
        diskCompressed,
        time,
        sysdstime,
        sysCompile,
        sysExec,
        readTime,
        writeTime,
    )


def parseDetect(file):
    stringSize = []
    schemaSize = []
    diskSchemaSize = []
    orgDiskSize = []

    sysdstime = []
    sysCompile = []
    sysExec = []
    time = []

    readTime = []
    writeTime = []

    ratio = []
    if os.path.exists(file):
        with open(file) as f:
            for l in f:
                if "\tdata/" in l:
                    if ".mtd" in l:
                        continue
                    elif ".tmp" in l:
                        diskSchemaSize.append(int(l.split("\t")[0]) * 1024)
                    else:
                        orgDiskSize.append(int(l.split("\t")[0]) * 1024)
                if "seconds time elapsed" in l:
                    if "," in l:
                        l = l.replace(",", ".")
                    time.append(float(l.strip().split(" ", 1)[0]))
                if "Cache times (ACQr/m, RLS, EXP):" in l:
                    readTime.append(float(l.strip()[31:].split("/")[0]))
                    writeTime.append(float(l.strip()[31:].split("/")[3].split(" ")[0]))
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
        writeTime,
    )


def parseReadCompressed(file):
    readtime = []
    totaltime = []
    if os.path.exists(file):
        with open(file) as f:
            for l in f:
                if "Cache times (ACQr/m, RLS, EXP):" in l:
                    readtime.append(float(l[32:37]))
                if "Total elapsed time:		" in l:
                    totaltime.append(float(l.split(":")[1].split("sec")[0].strip()))
    return readtime, totaltime


# results/ReadRealFrame/XPS-15-7590/FM--adult-cf.log
data = ["adult", "cat", "criteo", "crypto", "kdd", "salaries", "santander", "home"]
machines = ["XPS-15-7590", "dams-su1"]


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


mkdir("./plotting/tables/comp")

for m in machines:
    with open("plotting/tables/comp/" + m + ".csv", "w") as cv:
        cv.write("name,")
        cv.write(
            "StringSize,SchemaSize,SchemaRatio,OrgDiskSize,SchemaDiskSize,DetectSchemaTime,DetectSchemaSysDSTime,DetectSchemaCompile,DetectSchemaExec,DetectSchemaRead,DetectSchemaWrite,"
        )
        cv.write(
            "OrgDiskSnappy,OrgSnappyTime,OrgSnappySysDSTime,OrgSnappyCompile,OrgSnappyExec,OrgSnappyRead,OrgSnappyWrite,"
        )
        cv.write(
            "OrgDiskZstd,OrgZstdTime,OrgZstdSysDSTime,OrgZstdCompile,OrgZstdExec,OrgZstdRead,OrgZstdWrite,"
        )
        cv.write(
            "CompSize,CompRatio,CompDisk,CompTime,CompSysDSTime,CompCompile,CompExec,CompRead,CompWrite,"
        )
        cv.write(
            "CompDiskSnappy,CompSnappyTime,CompSnappySysDSTime,CompSnappyCompile,CompSnappyExec,CompSnappyRead,CompSnappyWrite,"
        )
        cv.write(
            "CompDiskZstd,CompZstdTime,CompZstdSysDSTime,CompZstdCompile,CompZstdExec,CompZStdRead,CompZStdWrite,"
        )
        cv.write("CompDetectRatio\n")

        for d in data:
            cv.write(d)
            cv.write(",")
            p = "results/ReadRealFrame/" + m + "/FM--" + d + "-uf.log"
            det = parseDetect(p)
            writeArr(cv, det)
            cv.write(",")
            p = "results/ReadRealFrame/" + m + "/FM--" + d + "-uf-SNAPPY.log"
            writeArr(cv, parseCompress(p)[3:])
            cv.write(",")
            p = "results/ReadRealFrame/" + m + "/FM--" + d + "-uf-ZStd.log"
            writeArr(cv, parseCompress(p)[3:])
            cv.write(",")
            p = "results/ReadRealFrame/" + m + "/FM--" + d + "-cf.log"
            com = parseCompress(p)[1:]
            writeArr(cv, com)
            # cv.write(",")
            # p = "results/ReadRealFrame/" + m + "/FM--" + d + "-rc.log"
            # writeArr(cv, parseReadCompressed(p))
            cv.write(",")
            p = "results/ReadRealFrame/" + m + "/FM--" + d + "-cf-SNAPPY.log"
            writeArr(cv, parseCompress(p)[3:])
            cv.write(",")
            p = "results/ReadRealFrame/" + m + "/FM--" + d + "-cf-ZStd.log"
            writeArr(cv, parseCompress(p)[3:])
            cv.write(",")
            writeDetCom(cv, det, com)
            cv.write("\n")
            # print(d)
