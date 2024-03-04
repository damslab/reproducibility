
import math
import os
from math import nan


def parse_write(file):

    totalTime = []
    writeTime = []
    randTime = []
    compressSize = []
    uncompressedSize = []
    diskSize = []
    castTime = []
    detectSchema = []
    applySchema = []

    try:
        if os.path.isfile(file):
            with open(file) as f:
                for l in f:
                    if "SYSTEMDS_STANDALONE_OPTS" in l:
                        pass
                    elif "with opts:" in l:
                        pass
                    elif "java -Xmx" in l:
                        pass
                    elif "Cache times (ACQr/m, RLS, EXP):" in l:
                        writeTime.append(
                            float(l[33:].split("/")[3].split(" ")[0]))
                    elif "DEBUG compress.CompressedMatrixBlockFactory: --compressed size: " in l:
                        compressSize.append(int(l[85:]))
                    elif "DEBUG compress.CompressedMatrixBlockFactory: --original size:" in l:
                        uncompressedSize.append(int(l[85:]))
                    elif file[10:-10] in l and "Performance counter stats for" not in l:
                        diskSize.append(int(l.split("\t")[0]) * 1024)
                    elif "Total elapsed time:	" in l:
                        totalTime.append(float(l[20:].split("sec.")[0]))
                    elif "  rand        " in l:
                        randTime.append(
                            float(l.split("rand")[1].strip().split(" ")[0]))
                    elif "  castdtf     " in l:
                        castTime.append(
                            float(l.split("castdtf")[1].strip().split(" ")[0]))
                    elif " detectSchema  " in l:
                        detectSchema.append(float(l.split("detectSchema")[1].strip().split(" ")[0]))
                    elif " applySchema  " in l:
                        applySchema.append(float(l.split("applySchema")[1].strip().split(" ")[0]))

            if compressSize == []:
                compressSize = [nan, nan]
            if uncompressedSize == []:
                uncompressedSize = [nan, nan]
            if castTime == []:
                castTime = [nan,nan]
            if detectSchema == []:
                detectSchema = [nan, nan]
            if applySchema == []:
                applySchema = [nan,nan]
            return totalTime, writeTime, randTime, compressSize, uncompressedSize, diskSize, castTime, detectSchema, applySchema
        else:
            print("Missing file: " + file)
            return None
    except Exception as e:
        print("Failed parsing: " + file)
        raise e


def parse_read(file):

    totalTime = []
    readTimes = []
    plusTime = []
    sumTime = []
    rightIndex = []
    toString = []

    if os.path.isfile(file):
        with open(file) as f:
            for l in f:
                if "Cache times (ACQr/m, RLS, EXP):" in l:
                    readTimes.append(float(l[32:].split("/")[0]))
                elif "  +           " in l:
                    plusTime.append(
                        float(l.split("+")[1].strip().split(" ")[0]))
                elif " uak+        " in l:
                    sumTime.append(
                        float(l.split("uak+")[1].strip().split(" ")[0]))
                elif "Total elapsed time:	" in l:
                    totalTime.append(float(l[20:].split("sec.")[0]))
                elif " rightIndex  " in l:
                    rightIndex.append(float(l.split("rightIndex")[1].strip().split(" ")[0]))
                elif " toString  " in l:
                    toString.append(float(l.split("toString")[1].strip().split(" ")[0]))

        return totalTime, readTimes, plusTime, sumTime, rightIndex, toString
    else:
        print("Missing file: " + file)
        return None



def format_tuple(data):
    if math.isnan(data[0]) or math.isinf(data[0]):
        return u"{0:17.3f}".format(data[0])
    elif data[1] == 0 or data[0] == int(data[0]):
        if  data[0] == int(data[0]):
            return u"{0:17d}".format(int(data[0]))
        return u"{0:17.3f}".format(data[0])
    else:
        return u"{0:10.3f}+-{1:5.3f}".format(data[0], data[1])


def format_write(data, len = 6):
    return ", ".join([format_tuple(d) for d in data[:len]])


def format_header(data):
    return ", ".join([u"{0:17s}".format(d) for d in data]) + "\n"

def format_read(data, len = 4):
    return ", ".join([format_tuple(d) for d in data[:len]])
