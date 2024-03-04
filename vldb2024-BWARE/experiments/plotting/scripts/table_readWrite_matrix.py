

import traceback
import table_util
import table_readWrite


def make_blocks_table(fs, ma, mo, t):
    blocks = [0.5, 1, 2, 4, 8, 16, 32, 64, 128]
    writeBase = u"results/Write/{ma}/ULA-{fs}/B{bs}-{mo}-{t}-Write.log"
    readBase = u"results/Read/{ma}/ULA-{fs}/B{bs}-{mo}-{t}-Read.log"
    write_data = []
    read_data = []
    try:
        for bs in blocks:
            write_data.append(table_readWrite.parse_write(
                writeBase.format(t=t, ma=ma, mo=mo, fs=fs, bs=bs)))
            read_data.append(table_readWrite.parse_read(
                readBase.format(t=t, ma=ma, mo=mo, fs=fs, bs=bs)))

        write_stats = table_util.stats(write_data)
        read_stats = table_util.stats(read_data)
        if write_stats and read_stats:
            csv_base = u"{bs:13.1f}, {wd}, {rd}\n"
            with open(u"plotting/tables/ReadWrite/{ma}/{mo}-{fs}-{t}.csv".format(t=t, ma=ma, mo=mo, fs=fs), "w") as w:
                w.write("blockSize (k), Total Write      , Write Time       , Rand Time        , Compress Mem Size, Normal Mem Size  , Disk Size        , Total Read       , Read Time        , Plus Time        , Sum Time\n")
                for idx, v in enumerate(blocks):
                    wd = table_readWrite.format_write(write_stats[idx])
                    rd = table_readWrite.format_read(read_stats[idx])
                    w.write(csv_base.format(bs=v, wd=wd, rd=rd))
        else:

            print(u"Failed Parsing: {0} {1} {2} {3} {4} {5}".format(
                fs, ma, mo, t, write_stats is None, read_stats is None))
    except Exception as e:
        print("Failed parsing: \n{}\n{}".format(writeBase.format(
            t=t, ma=ma, mo=mo, fs=fs, bs=bs), readBase.format(t=t, ma=ma, mo=mo, fs=fs, bs=bs)))
        raise e


def make_sparsity_table(fs, ma, mo, size):
    writeBase = u"results/Write/{ma}/ULA-{fs}/B{bs}-{mo}-Sparse{s}-{size}-Binary-Write.log"
    readBase = u"results/Read/{ma}/ULA-{fs}/B{bs}-{mo}-Sparse{s}-{size}-Binary-Read.log"
    # sparsities = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    sparsities = [0.0,  # Empty
                  0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09,  # Small Edge
                  0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,  # Intermediate
                  0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99,  # Large Edge
                  1.0  # Constant
                  ]
    write_data = []
    read_data = []
    for s in sparsities:
        write_data.append(table_readWrite.parse_write(
            writeBase.format(ma=ma, fs=fs, bs=16, mo=mo, s=s, size=size)))
        read_data.append(table_readWrite.parse_read(
            readBase.format(ma=ma, fs=fs, bs=16, mo=mo, s=s, size=size)))

    write_stats = table_util.stats(write_data)
    read_stats = table_util.stats(read_data)

    if write_stats and read_stats:
        csv_base = u"{s:13.3f}, {wd}, {rd}\n"
        with open(u"plotting/tables/ReadWrite/{ma}/{mo}-{fs}-Sparsities-{size}.csv".format(ma=ma, mo=mo, fs=fs, size=size), "w") as w:
            w.write("Sparsity       , Total Write      , Write Time       , Rand Time        , Compress Mem Size, Normal Mem Size  , Disk Size        , Total Read       , Read Time        , Plus Time        , Sum Time\n")
            for idx, v in enumerate(sparsities):
                wd = table_readWrite.format_write(write_stats[idx])
                rd = table_readWrite.format_read(read_stats[idx])
                w.write(csv_base.format(s=v, wd=wd, rd=rd))
    else:
        print(u"Failed Parsing: {0} {1} {2} {3} {4} ".format(
            fs, ma, mo,  write_stats is None, read_stats is None))


def make_distinct_table(fs, ma, mo, size):
    writeBase = u"results/Write/{ma}/ULA-{fs}/B{bs}-{mo}-Sparse1.0-{size}-Distinct{s}-Write.log"
    readBase = u"results/Read/{ma}/ULA-{fs}/B{bs}-{mo}-Sparse1.0-{size}-Distinct{s}-Read.log"
    # sparsities = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    distinct = [1,2,3,4,5,6,7,8,9,10,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536]
    write_data = []
    read_data = []
    for s in distinct:
        write_data.append(table_readWrite.parse_write(
            writeBase.format(ma=ma, fs=fs, bs=16, mo=mo, s=s, size=size)))
        read_data.append(table_readWrite.parse_read(
            readBase.format(ma=ma, fs=fs, bs=16, mo=mo, s=s, size=size)))

    write_stats = table_util.stats(write_data)
    read_stats = table_util.stats(read_data)

    if write_stats and read_stats:
        csv_base = u"{s:9d}, {wd}, {rd}\n"
        with open(u"plotting/tables/ReadWrite/{ma}/{mo}-{fs}-Distinct-{size}.csv".format(ma=ma, mo=mo, fs=fs, size=size), "w") as w:
            w.write("Distinct , Total Write      , Write Time       , Rand Time        , Compress Mem Size, Normal Mem Size  , Disk Size        , Total Read       , Read Time        , Plus Time        , Sum Time\n")
            for idx, v in enumerate(distinct):
                wd = table_readWrite.format_write(write_stats[idx])
                rd = table_readWrite.format_read(read_stats[idx])
                w.write(csv_base.format(s=v, wd=wd, rd=rd))
    else:
        print(u"Failed Parsing: {0} {1} {2} {3} {4} ".format(
            fs, ma, mo,  write_stats is None, read_stats is None))


file_types = ["compressed", "binary"]
machines = ["XPS-15-7590", "dams-su1"]
mo = "singlenode"
targets = ["Sparse0.5-64k-Binary",
           "Sparse0.5-256k-Binary", "Sparse1.0-64k-Ternary"]
for fs in file_types:
    for ma in machines:
       try:
           for t in targets:
               make_blocks_table(fs, ma, mo, t)

           make_sparsity_table(fs, ma, mo, "64k")
           make_sparsity_table(fs, ma, mo, "256k")
           make_distinct_table(fs, ma, mo, "64k")
       except Exception as e:
           traceback.print_exc()
           print(str(e))
