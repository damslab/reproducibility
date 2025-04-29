import os

# results/wordemb/emb/dams-su1/code/conf/ULAb16.xml/singlenode/data-w2v-dblp_v14_abstracts_embedded_10000_1000.bin_data-w2v-wiki-news-300d-1M.vec_10000.embedding.bin.log


def parse(path):
    sysdstime = []
    sysCompile = []
    sysExec = []
    time = []
    replace = []
    tableExpand = []
    reshape = []
    multiply = []
    colmean = []
    if os.path.exists(path):
        with open(path) as f:
            for l in f:
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
                if "Total elapsed time:" in l:
                    # print(l, float(l.strip().split(":")[1].split("sec")[0]))
                    sysdstime.append(float(l.strip().split(":")[1].split("sec")[0]))
                if "Total compilation time:" in l:
                    sysCompile.append(float(l.strip().split(":")[1].split("sec")[0]))
                if "Total execution time:" in l:
                    sysExec.append(float(l.strip().split(":")[1].split("sec")[0]))
                if "Killed              " in l:
                    return []
                if "Exception in thread" in l:
                    return []
                if "org.apache.sysds.runtime.DMLRuntimeException" in l:
                    return []

                if " replace  " in l:
                    replace.append(float(l.split("replace")[1].strip().split(" ")[0]))

                if " uacmean  " in l:
                    colmean.append(float(l.split("uacmean")[1].strip().split(" ")[0]))
                if " ctableexpand  " in l:
                    sp = l.split("ctableexpand")[1].strip()
                    t = float(sp.split(" ")[0])
                    r = float(sp.split(" ")[-1])
                    tableExpand.append(float(t / r))
                if " rshape  " in l:
                    sp =  l.split("rshape")[1].strip().replace(",", "")
                    t = float(sp.split(" ")[0])
                    r = float(sp.split(" ")[-1])
                    reshape.append(float(t / r))
                if " ba+*  " in l:
                    sp = l.split("ba+*")[1].strip().replace(",", "")
                    t = float(sp.split(" ")[0])
                    r = float(sp.split(" ")[-1])
                    multiply.append(float(t / r))
                    

    return (
        time,
        sysdstime,
        sysCompile,
        sysExec,
        replace,
        tableExpand,
        reshape,
        multiply,
        [],
        colmean,
    )


def parseTf(path):
    time = []
    colsum = []
    embed = []
    if os.path.exists(path):
        with open(path) as f:
            for l in f:
                if "seconds time elapsed" in l:
                    if "," in l:
                        l = l.replace(",", ".")
                    time.append(float(l.strip().split(" ", 1)[0]))
                if "embed:           " in l:
                    embed.append(float(l[10:]))
                if "colsum        " in l:
                    colsum.append(float(l[10:]))

                if "OOM when allocating tensor" in l:
                    return []
                if "DefaultCPUAllocator: can't allocate memory" in l:
                    return []
    return [time, [], [], [], [], [], [], [], embed, colsum]


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


abstracts = ["1000", "3000", "10000", "30000", "100000", "300000", "1000000"]
words = ["10000", "100000", "999995"]
words = ["10000"]

machines = ["dams-su1"]
conf = ["ULAb16", "AWAb16", "tf", "torch"]

mkdir("./plotting/tables/27-wordemb-random")
this = "plotting/scripts/table_27_wordemb_random.py"
for m in machines:
    out = "plotting/tables/27-wordemb-random/" + m + ".csv"
    print("TableScript:", this, "out:", out)
    with open(out, "w") as cv:
        cv.write("conf,")
        cv.write("abstracts,")
        cv.write("words,")
        cv.write("time,")
        cv.write("sysdsTime,")
        cv.write("compile,")
        cv.write("sysdsExec,")
        cv.write("replace,")
        cv.write("tableExpand,")
        cv.write("reshape,")
        cv.write("multiply,")
        cv.write("tfEncode,")
        cv.write("colmean")
        cv.write("\n")

        basis = "results/wordemb/emb_random/" + m + "/code/conf/"
        for a in abstracts:
            for w in words:
                for c in conf:
                    if "tf" in c or "torch" in c:
                        # experiments/results/wordemb/emb/dams-su1/tf/10000_1000.log
                        path = (
                            "results/wordemb/emb/"
                            + m
                            + "/"
                            + c
                            + "/"
                            + w
                            + "_"
                            + a
                            + ".log"
                        )
                        if os.path.exists(path):
                            data = parseTf(path)
                            if len(data) > 0:
                                cv.write(c)
                                cv.write(",")
                                cv.write(a)
                                cv.write(",")
                                cv.write(w)
                                cv.write(",")
                                writeArr(cv, data)
                                cv.write("\n")
                        continue
                    path = basis + c + ".xml/singlenode/" + a + "_" + w + ".log"
                    if os.path.exists(path):
                        data = parse(path)
                        if len(data) > 0:
                            cv.write(c)
                            cv.write(",")
                            cv.write(a)
                            cv.write(",")
                            cv.write(w)
                            cv.write(",")
                            writeArr(cv, data)
                            cv.write("\n")
                    # else:
                    #     print("missing: " + path)
