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

    compTime = []

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
                            [], []
                        )

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
                if "compress.CompressedMatrixBlockFactory: --compression phase" in l:
                    cl = l.split("--compression phase")[1]
                
                    phaseId = int(cl.strip().split(" ", 1)[0].strip())
                    if(phaseId == 0):
                        compTime.append(float(cl.split(":")[1]) / 1000)
                    else:
                        compTime[-1] += float(cl.split(":")[1])  / 1000

                    # if("RCFCMCD" in file ):
                    #     print(compTime)
                   
                if "Killed              " in l:
                    return [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
                if "Exception in thread" in l:
                    return [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
                if "org.apache.sysds.runtime.DMLRuntimeException" in l:
                    return [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

    if len(sysdstime) == 0:
        return [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
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
        compRatio,
        sparseSize,
        denseSize,
        compTime
    )


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


mkdir("./plotting/tables/te")

for m in machines:
    out = "plotting/tables/te/" + m + ".csv"
    print("tableScript:", "plotting/scripts/table_transform_encode_real_new.py", "out:" , out)
    with open(out, "w") as cv:
        cv.write("name,")
        cv.write(
            "StringSize,SchemaSize,SchemaRatio,OrgDiskSize,FMDiskSize,FMTime,FMSysDSTime,FMCompile,FMExec,FMRead,FMTE,FMSize,"
        )
        cv.write(
            "FMCDDiskSize,FMCDTime,FMCDSysDSTime,FMCDCompile,FMCDExec,FMCDRead,FMCDTE,FMCDSize,FMCDCompSize,FMCDSparseSize,FMCDDenseSize,FMCDCompTime,"
        )
        cv.write(
            "FCMCDDiskSize,FCMCDTime,FCMCDSysDSTime,FCMCDCompile,FCMCDExec,FCMCDRead,FCMCDTE,FCMCDSize,FCMCDCompSize,"
        )
        cv.write(
            "CFCMDDiskSize,CFCMDTime,CFCMDSysDSTime,CFCMDCompile,CFCMDExec,CFCMDRead,CFCMDTE,CFCMDSize,CFCMDCompSize,CFCMDSparseSize,CFCMDDenseSize,"
        )
        cv.write(
            "CFCMCDDiskSize,CFCMCDTime,CFCMCDSysDSTime,CFCMCDCompile,CFCMCDExec,CFCMCDRead,CFCMCDTE,CFCMCDSize,CFCMCDCompSize,CFCMCDSparseSize,CFCMCDDenseSize,"
        )
        cv.write(
            "RFCMCDDiskSize,RFCMCDTime,RFCMCDSysDSTime,RFCMCDCompile,RFCMCDExec,RFCMCDRead,RFCMCDTE,RFCMCDSize,RFCMCDCompSize,RFCMCDSparseSize,RFCMCDDenseSize,"
        )
        cv.write(
            "RCFCMCDDiskSize,RCFCMCDTime,RCFCMCDSysDSTime,RCFCMCDCompile,RCFCMCDExec,RCFCMCDRead,RCFCMCDTE,RCFCMCDSize,RCFCMCDCompSize,RCFCMCDSparseSize,RCFCMCDDenseSize,RCFCMCDCompTime,"
        )
        cv.write(
            "RCFMCDDiskSize,RCFMCDTime,RCFMCDSysDSTime,RCFMCDCompile,RCFMCDExec,RCFMCDRead,RCFMCDTE,RCFMCDSize,"
        )
        cv.write(
            "FMSDiskSize,FMSTime,FMSSysDSTime,FMSCompile,FMSExec,FMSRead,FMSTE,FMSSize,"
        )
        # cv.write("OrgDiskSnappy,OrgSnappyTime,OrgSnappySysDSTime,OrgSnappyCompile,OrgSnappyExec,")
        # cv.write("OrgDiskZstd,OrgZstdTime,OrgZstdSysDSTime,OrgZstdCompile,OrgZstdExec,")
        # cv.write("CompSize,CompRatio,CompDisk,CompTime,CompSysDSTime,CompCompile,CompExec,")
        # cv.write("CompDiskSnappy,CompSnappyTime,CompSnappySysDSTime,CompSnappyCompile,CompSnappyExec,")
        # cv.write("CompDiskZstd,CompZstdTime,CompZstdSysDSTime,CompZstdCompile,CompZstdExec,")
        # cv.write("CompDetectRatio\n")
        cv.write("\n")

        for d in data:
            cv.write(d)
            cv.write(",")
            writeArr(cv, parse("results/TE/" + m + "/FM--" + d + "-FM.log")[:-4])
            cv.write(",")
            writeArr(cv, parse("results/TE/" + m + "/FM--" + d + "-FMCD.log")[4:])
            cv.write(",")
            writeArr(cv, parse("results/TE/" + m + "/FM--" + d + "-FCMCD.log")[4:-3])
            cv.write(",")
            writeArr(cv, parse("results/TE/" + m + "/FM--" + d + "-CFCMD.log")[4:-1])
            cv.write(",")
            writeArr(cv, parse("results/TE/" + m + "/FM--" + d + "-CFCMCD.log")[4:-1])
            cv.write(",")
            p_data = parse("results/TE/" + m + "/FM--" + d + "-RFCMCD.log")[4:-1]
            writeArr(cv,p_data)
            cv.write(",")
            writeArr(cv, parse("results/TE/" + m + "/FM--" + d + "-RCFCMCD.log")[4:])
            cv.write(",")
            writeArr(cv, parse("results/TE/" + m + "/FM--" + d + "-RCFMCD.log")[4:-4])
            cv.write(",")
            # experiments/results/TE_lossy/dams-su1/E-adult-FM-l0-S.log
            writeArr(cv, parse("results/TE_lossy/" + m + "/E-" + d + "-FM-l0-S.log")[4:-4])
            cv.write("\n")
