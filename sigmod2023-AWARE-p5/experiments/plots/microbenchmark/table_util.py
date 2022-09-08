import argparse
import os

import numpy as np


def parse(file, op, seconds=False):
    if os.path.isfile(file):
        with open(file) as f:
            if op:
                if isinstance(op, str):
                    mainString = op
                else:
                    mainString = op[0]
            else:
                mainString = "Total elapsed time:"
            time = []
            repeats = 0

            for line in f:
                if "java.lang.OutOfMemoryError" in line:
                    return [[-1], -1]
                if "Exception in thread" in line:
                    return [[-2], -2]
                if "An Error Occured" in line:
                    return [[-3], -3]
                if "----" in line:
                    continue
                if "realpath: /home/hadoop/hadoop-3.3.1:" in line:
                    continue
                if op:
                    if isinstance(op, str):
                        mainString = op
                        if "Not implemented direct tsmm colgroup" in line:
                            continue
                        if mainString in line:
                            rep = float(
                                line.split(mainString)[
                                    1].replace("\t", "")[-5:]
                            )
                            time.append(
                                float(
                                    line.split(mainString)[1]
                                    .replace("\t", "")
                                    .replace(",", "")[:-5]
                                )
                                * 1000
                                / rep
                            )
                            repeats += rep
                    elif isinstance(op, list):

                        for ido, ent in enumerate(op):
                            if ent in line:
                                if ("MATRIX" not in line and "WARN" not in line):
                                    rep = float(
                                        line.split(ent)[1].replace(
                                            "\t", "")[-5:]
                                    )
                                    v = float(line.split(ent)[
                                              1].replace("\t", "").replace(",", "")[:-5])
                                    time.append(v * 1000 / rep)
                                    # print(v)
                                    if ido == 0:
                                        repeats += rep
                        # print(time)
                else:
                    if mainString in line:
                        time.append(
                            float(line.split(mainString)[
                                  1].replace("\t", "")[:-5])
                        )
                        repeats = repeats + 1
            if isinstance(op, list):
                a = time
                time = [0] * (int)(round(len(a) / len(op)))
                for idx in range(0, len(a), len(op)):
                    for idy, v in enumerate(op):
                        index = (int)(idx / len(op))
                        if idx + idy < len(a) and index < len(time):
                            time[index] = time[index] + a[idx + idy]
                # repeats = repeats / len(op)
                # for idx in range(0, len(time)):
                #     time[idx] = time[idx] / repeats
            return [time, repeats]
    else:
        return [[float("NaN")], 0]


def parseSysML(file, op, seconds=False):
    try:
        if os.path.isfile(file):
            with open(file) as f:
                if op:
                    if isinstance(op, str):
                        mainString = op
                    else:
                        mainString = op[0]
                else:
                    mainString = "Total elapsed time:"
                time = []
                repeats = 0
                for line in f:
                    if "java.lang.OutOfMemoryError" in line:
                        return [[-1], -1]
                    if "Exception in thread" in line:
                        return [[-2], -2]
                    if "An Error Occured" in line:
                        return [[-3], -3]
                    if "----" in line:
                        continue
                    if "realpath: /home/hadoop/hadoop-3.3.1:" in line:
                        continue
                    if op:
                        line = line.replace("\t", " ")
                        if isinstance(op, str):
                            if mainString in line:
                                # print(line)
                                rep = float(line.split(mainString)
                                            [1].split("sec")[1])

                                time.append(
                                    float(
                                        line.split(mainString)[
                                            1].split("sec")[0]
                                        # .replace("\t", "")
                                        # .replace(",", "")[:-8]
                                    )
                                    * 1000 / rep
                                )
                                repeats += rep
                        elif isinstance(op, list):

                            for ido, ent in enumerate(op):
                                if ent in line:
                                    if (
                                        "MATRIX" not in line
                                        and "org.apache.sysds" not in line
                                    ):
                                        rep = float(line.split(ent)
                                                    [1].split("sec")[1])
                                        v = float(line.split(ent)[
                                                  1].split("sec")[0])
                                        time.append(v * 1000 / rep)

                                        if ido == 0:
                                            repeats += rep

                    else:
                        if mainString in line:
                            time.append(
                                float(line.split(mainString)[
                                      1].replace("\t", "")[:-5])
                            )
                            repeats = repeats + 1

                if isinstance(op, list):
                    a = time
                    time = [0] * (int)(round(len(a) / len(op)))
                    for idx in range(0, len(a), len(op)):
                        for idy, v in enumerate(op):
                            index = (int)(idx / len(op))
                            if idx + idy < len(a) and index < len(time):
                                time[index] = time[index] + a[idx + idy]

                return [time, repeats]
            return [[float("NaN")], 0]
        else:
            return [[float("NaN")], 0]
    except:
        return parse(file, op, seconds)


def parseComp(file):
    if os.path.isfile(file):
        with open(file) as f:
            op = " compress  "
            phases = [[], [], [], [], []]
            readingFromDisk = []
            time = []
            repeats = 0
            full_reps = 0
            ratio = 0

            for line in f:
                if op in line:
                    rep = int(line.split(op)[1].replace("\t", "")[-5:])
                    time.append(
                        float(line.split(op)[1].replace(
                            "\t", "")[:-5]) * 1000 / rep
                    )
                    repeats += rep
                elif "--compression phase " in line:
                    phaseId = int(line[83:85])
                    phases[phaseId].append(float(line[97:]))

                elif "Cache times " in line:
                    full_reps += 1
                    readingFromDisk.append(
                        float(line[31:].split("/")[0]) * 1000)
                elif "--compression ratio" in line:
                    ratio += float(line[84:])

            try:
                if len(phases) > 0:
                    avgPhases = []
                    for p in phases:
                        avgPhases.append(round(sum(p) / len(p), 2))
                    avgPhases = str(avgPhases).replace(",", ":")
                else:
                    avgPhases = ""
                if len(time) > 0:
                    timeAvg = np.average(time)
                else:
                    timeAvg = -1

                if len(readingFromDisk) > 0:
                    avgDisk = np.average(readingFromDisk)
                else:
                    avgDisk = -1
                avgcompress = timeAvg - avgDisk

                avgRatio = ratio / repeats
                return ", ".join(
                    [
                        "{0:10.2f}".format(avgcompress),
                        "{0:5}".format(repeats),
                        "{0:6.0f}".format(avgDisk),
                        "{0:10.2f}".format(timeAvg),
                        "{0:5.2f}".format(avgRatio),
                        avgPhases,
                    ]
                )
            except:
                return "Failed Parsing"
    else:
        return "No File at : " + file


def parseSysMLComp(file):
    try:
        if os.path.isfile(file):
            with open(file) as f:
                op = "\tcompress "
                phases = [[], [], [], []]
                readingFromDisk = []
                time = []
                repeats = 0
                full_reps = 0
                ratio = 0

                for line in f:
                    if op in line:
                        rep = int(line.split("sec")[1])
                        time.append(
                            float(line.split(op)[1].split(
                                "sec")[0]) * 1000 / rep
                        )
                        repeats += rep
                    elif "DEBUG compress.CompressedMatrixBlock: --compression phase " in line:
                        phaseId = int(line[76]) - 1
                        phases[phaseId].append(float(line[78:-1]))

                    elif "Cache times " in line:
                        full_reps += 1
                        readingFromDisk.append(
                            float(line[31:].split("/")[0]) * 1000)
                    elif "EBUG compress.CompressedMatrixBlock: --compression ratio:" in line:
                        ratio += float(line.split("--compression ratio:")[1])

                try:
                    if len(phases) > 0:
                        avgPhases = []
                        for p in phases:
                            avgPhases.append(round(sum(p) / len(p), 2))
                        avgPhases = str(avgPhases).replace(",", ":")
                    else:
                        avgPhases = ""
                    if len(time) > 0:
                        timeAvg = np.average(time)
                    else:
                        timeAvg = -1

                    if len(readingFromDisk) > 0:
                        avgDisk = np.average(readingFromDisk)
                    else:
                        avgDisk = -1
                    avgcompress = timeAvg - avgDisk

                    avgRatio = ratio / repeats
                    return ", ".join(
                        [
                            "{0:10.2f}".format(avgcompress),
                            "{0:5}".format(repeats),
                            "{0:6.0f}".format(avgDisk),
                            "{0:10.2f}".format(timeAvg),
                            "{0:5.2f}".format(avgRatio),
                            avgPhases,
                        ]
                    )
                except:
                    return "Failed Parsing"
        else:
            return "No File at : " + file
    except:
        return parseSysMLv2(file)


def parseSysMLv2(file):
    if os.path.isfile(file):
        with open(file) as f:
            op = " compress "
            phases = [[], [], [], [], []]
            readingFromDisk = []
            time = []
            repeats = 0
            full_reps = 0
            ratio = 0

            for line in f:
                if op in line:
                    rep = int(line.split(op)[1].replace("\t", "")[-5:])
                    time.append(
                        float(line.split(op)[1].replace(
                            "\t", "")[:-5]) * 1000 / rep
                    )
                    repeats += rep
                elif "DEBUG compress.CompressedMatrixBlock: --compression phase " in line:
                    phaseId = int(line[76]) - 1
                    phases[phaseId].append(float(line[78:-1]))

                elif "Cache times " in line:
                    full_reps += 1
                    readingFromDisk.append(
                        float(line[31:].split("/")[0]) * 1000)
                elif "--compression ratio: " in line:
                    ratio += float(line.split("--compression ratio:")[1])

            try:
                if len(phases) > 0:
                    avgPhases = []
                    for p in phases:
                        avgPhases.append(round(sum(p) / len(p), 2))
                    avgPhases = str(avgPhases).replace(",", ":")
                else:
                    avgPhases = ""
                if len(time) > 0:
                    timeAvg = np.average(time)
                else:
                    timeAvg = -1

                if len(readingFromDisk) > 0:
                    avgDisk = np.average(readingFromDisk)
                else:
                    avgDisk = -1
                avgcompress = timeAvg - avgDisk

                avgRatio = ratio / repeats

                return ", ".join(
                    [
                        "{0:10.2f}".format(avgcompress),
                        "{0:5}".format(repeats),
                        "{0:6.0f}".format(avgDisk),
                        "{0:10.2f}".format(timeAvg),
                        "{0:5.2f}".format(avgRatio),
                        avgPhases,
                    ]
                )
            except:
                return "Failed Parsing"
    else:
        return "No File at : " + file


def appendOut(f, path, op, name, techniques, machines, dataSet, sysmlTechniques=[], includeULA=True, seconds=False):

    for comp in sysmlTechniques:
        resString = ""
        if not includeULA and comp == "ula":
            continue
        for machine in machines:
            fullPath = path + machine + "/" + comp + ".log"
            data = parseSysML(fullPath, op, seconds)
            times = np.average(data[0]) if (len(data[0]) > 0) else float("NaN")
            reps = data[1]
            resString = resString + "{0:20.2f},{1:5.0f},".format(times, reps)
        f.write("{0:20},{1:20},{2:35},{3}\n".format(
            dataSet, name, comp, resString))
    for comp in techniques:
        resString = ""
        if not includeULA and comp == "ula":
            continue
        for machine in machines:
            fullPath = path + machine + "/" + comp + ".log"
            data = parse(fullPath, op, seconds)
            times = np.average(data[0]) if (len(data[0]) > 0) else float("NaN")
            reps = data[1]
            resString = resString + "{0:20.2f},{1:5.0f},".format(times, reps)
        f.write("{0:20},{1:20},{2:35},{3}\n".format(
            dataSet, name, comp, resString))


def appendOutComp(f, path, op, name, machines, techniques, dataSet, sysmlTechniques=[]):
    for comp in sysmlTechniques:
        for machine in machines:
            fullPath = path + machine + "/" + comp + ".log"
            data = parseSysMLComp(fullPath)

            f.write(
                "{0:15},{1:33},{2:15},{3}\n".format(
                    dataSet, comp, machine, str(data))
            )
    for comp in techniques:
        for machine in machines:
            fullPath = path + machine + "/" + comp + ".log"
            data = parseComp(fullPath)

            f.write(
                "{0:15},{1:33},{2:15},{3}\n".format(
                    dataSet, comp, machine, str(data))
            )
