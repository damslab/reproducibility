
import os
from math import nan
import table_readWrite
import table_util
from multiprocessing import Process


def parse_read(path):
    pass


def parse_write(file):
    try:
        totalTime = []
        writeTime = []
        compressSize = []
        uncompressedSize = []
        diskSize = []
        mse = []
        rmse = []
        nrmse = []
        mae = []
        mape = []
        smape = []
        msmape = []
        sdd = []
        skwd = []
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
                    elif "                Mean Square Error:" in l:
                        mse.append(float(l[35:]))
                    elif "           Root Mean Square Error:" in l:
                        rmse.append(float(l[35:]))
                    elif "Normalized Root Mean Square Error:" in l:
                        nrmse.append(float(l[35:]))
                    elif "              Mean Absolute Error:" in l:
                        mae.append(float(l[35:]))
                    elif "   Mean Absolute percentage Error:" in l:
                        mape.append(float(l[35:]))
                    elif "symmetric Mean Absolute per Error:" in l:
                        smape.append(float(l[35:]))
                    elif "          modified symmetric MAPE:" in l:
                        msmape.append(float(l[35:]))
                    elif "    Standard Deviation Difference:" in l:
                        sdd.append(float(l[35:]))
                    elif "                  Skew Difference:" in l:
                        skwd.append(float(l[35:]))
            if compressSize == []:
                compressSize = [nan, nan]
            if uncompressedSize == []:
                uncompressedSize = [nan, nan]

            return totalTime, writeTime, compressSize, uncompressedSize, diskSize, \
                mse, rmse, nrmse, mae, mape, smape, msmape, sdd, skwd

        else:
            # print("Missing: " + file);
            return None
    except Exception as e:
        print(e)
        print(file)
        return None


def getColumnNamesWrite():
    return ["Lossy", "BlkSize","TotalTime", "WriteTime", "CompSize", "UncSize", "DiskSize", "MSE",
        "RMSE", "NRMSE", "MAE", "MAPE", "SMAPE", "MSMAPE", "SDD", "SKWD"]



def a(m, d, f, b, l, w, pre=""):
    
    pathWrite = base.format(
        r="Write", m=m, d=d, f=f, b=b, l=l)
    write_data = table_util.stats_list(parse_write(pathWrite))
    pathRead = base.format(
        r="Read", m=m, d=d, f=f, b=b, l=l)
    read_data = table_util.stats_list(parse_read(pathRead))

    if write_data != None:
        wd = table_readWrite.format_write(
            write_data, len=len(write_data))
        w.write(csv_base.format(l=pre + l, b=b, wd=wd, rd=None))


def construct(out_base, header, blockSizes, lossy, d , m):
    out = out_base.format(m=m, d=d)
    with open(out, "w") as w:

        w.write(header)
        for b in blockSizes:
            a(m, d, "binary", b, "original", w, "bin-")
        for l in lossy:
            for b in blockSizes:
                a(m, d, "compressed", b, l,w)


if __name__ == "__main__":

    lossy = ["original", "replace",
             "q10", "q9", "q8", "q7", "q6", "q5", "q4", "q3", "q2", "q1",
             "qi10", "qi9", "qi8", "qi7", "qi6", "qi5", "qi4", "qi3", "qi2", "qi1",
             "qti10", "qti9", "qti8", "qti7", "qti6", "qti5", "qti4", "qti3", "qti2", "qti1",
             "qt10", "qt9", "qt8", "qt7", "qt6", "qt5", "qt4", "qt3", "qt2", "qt1"]
    machines = ["dams-su1", "XPS-15-7590"]
    blockSizes = ["0.5", "1", "8", "16"]

    # Example:
    base = "results/{r}-UCR/{m}/ULA-{f}-{d}/B{b}-singlenode-{l}.log"
    datasets = os.listdir("data/UCRTime/UCRArchive_2018")
    datasets.sort()
    out_base = "plotting/tables/UCRTime/{m}/{d}.csv"
    csv_base = u"{l:17}, {b:17}, {wd}, {rd}\n"

    colNames = getColumnNamesWrite()
    header = table_readWrite.format_header(colNames)

    processes = []
    for m in machines:
        table_util.make_sure_path_exists(
            "plotting/tables/UCRTime/{m}".format(m=m))
        for d in datasets:
            p = Process(target=construct, args=(out_base, header, blockSizes, lossy, d, m))
            p.start()
            processes.append( p)

    for process in processes:
        process.join()
    