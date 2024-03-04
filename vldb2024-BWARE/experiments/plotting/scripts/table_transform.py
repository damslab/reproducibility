
import table_readWrite
import traceback
import table_util
import os

from math import nan


def parseExisting(file):
    writeTime = []
    diskSize = []
    totalTime = []
    compEncodeSize = []
    compEncodeSparseSize = []
    compEncodeDenseSize = []
    compEncodeRatio = []
    compFactoryDense = []
    compFactoryOriginal = []
    compFactoryComp = []
    compFactoryRatio = []
    with open(file) as f:
        for l in f:
            if "SYSTEMDS_STANDALONE_OPTS" in l:
                pass
            elif "with opts:" in l:
                pass
            elif "java -Xmx" in l:
                pass
            elif " DMLRuntimeException --" in l:
                return None
            elif "java.io.IOException" in l:
                return None
            elif "Cache times (ACQr/m, RLS, EXP):" in l:
                writeTime.append(
                    float(l[33:].split("/")[3].split(" ")[0]))
            elif file[10:-10] in l and ".data" in l and "Performance counter stats for" not in l and "DMLRuntimeException" not in l:
                diskSize.append(int(l.split("\t")[0]) * 1024)
            elif "Total elapsed time:	" in l:
                totalTime.append(float(l[20:].split("sec.")[0]))
            elif "encode.CompressedEncode: Compressed transform encode size:         " in l:
                compEncodeSize.append(float(l[90:].strip()))
            elif "encode.CompressedEncode: Uncompressed transform encode Sparse size: " in l:
                compEncodeSparseSize.append(float(l[91:].strip()))
            elif "encode.CompressedEncode: Uncompressed transform encode Dense size: " in l:
                compEncodeDenseSize.append(float(l[90:].strip()))
            elif "encode.CompressedEncode: Compression ratio:  " in l:
                compEncodeRatio.append(float(l[71:].strip()))
            elif "compress.CompressedMatrixBlockFactory: --dense size:       " in l:
                compFactoryDense.append(float(l[84:].strip()))
            elif "compress.CompressedMatrixBlockFactory: --original size:    " in l:
                compFactoryOriginal.append(float(l[84:].strip()))
            elif "compress.CompressedMatrixBlockFactory: --compressed size:  " in l:
                compFactoryComp.append(float(l[84:].strip()))
            elif "compress.CompressedMatrixBlockFactory: --compression ratio:" in l:
                compFactoryRatio.append(float(l[84:].strip()))

    if len(compEncodeRatio) > 0:
        return [writeTime, diskSize, totalTime, compEncodeRatio, compEncodeSize, compEncodeSparseSize, compEncodeDenseSize, compFactoryRatio, compFactoryComp, compFactoryOriginal, compFactoryDense]
    elif len(compFactoryRatio) > 0:
        return [writeTime, diskSize, totalTime, compEncodeRatio, compEncodeSize, compEncodeSparseSize, compEncodeDenseSize, compFactoryRatio, compFactoryComp, compFactoryOriginal, compFactoryDense]
    else:
        return [writeTime, diskSize, totalTime, [nan], [nan], [nan], [nan], [nan], [nan], [nan], [nan]]


def parseTransform(file):

    try:
        if os.path.isfile(file):
            return parseExisting(file)
        else:
            # print("Missing file: " + file)
            return None
    except Exception as e:
        print("Failed parsing: " + file)
        raise e


file_types = [""]


criteo_specs = ["criteo_spec1", "criteo_spec2",
                "criteo_fe1", "criteo_fe2", "criteo_fe3", "criteo_fe4", "criteo_fe5", "criteo_fe6", ]

machines = ["XPS-15-7590", "dams-su1"]
data_files = ["day_0_1000", "day_0_10000",
              "day_0_100000", "day_0_1000000", "cup98val", "adult"]
# data_files = ["day_0_1000", "day_0_10000"]
specs = [criteo_specs, criteo_specs,
         criteo_specs, criteo_specs,
         ["kdd_spec1"], ["adult_spec2"]]
mo = "singlenode"
blockSizes = ["16"]
formats = ["binary", "compressed"]
configs = ["ULA", "CLA", "TCLA"]
csv_base = u"{c:9}, {fs:16}, {bs:9}, {td}\n"
csv_header = u"{c:9}, {fs:16}, {bs:9}, {tdh}"


transformBase = u"results/Transform/{ma}/{c}-{fs}/B{bs}-{mo}-{file}-{spec}.log"
for ma in machines:
    for idx, file in enumerate(data_files):
        for spec in specs[idx]:
            tablePath = u"plotting/tables/Transform/{ma}-{mo}-{file}-{spec}.csv"
            with open(tablePath.format(ma=ma, mo=mo, file=file, spec=spec), "w") as w:
                w.write(csv_header.format(c="Conf", fs="Format", bs="BlockSz",
                                          tdh=table_readWrite.format_header(
                                              ["WriteTime", "DiskSize", "totalTime", "compRatio", "compSize", "SparseSize", "DenseSize"])))
                for c in configs:
                    for fs in formats:
                        for bs in blockSizes:
                            path = transformBase.format(
                                ma=ma, c=c, fs=fs, bs=bs, mo=mo, file=file, spec=spec)
                            data = parseTransform(path)
                            if data == None:
                                continue
                            data = table_util.stats_list(data)

                            if (data):
                                td = table_readWrite.format_write(
                                    data, len(data))
                                w.write(csv_base.format(
                                    c=c, fs=fs, bs=bs, td=td))
                            else:
                                print("Something wrong with: " + path)
