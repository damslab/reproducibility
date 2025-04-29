

import table_readWrite
import traceback
import table_util


def make_blocks_table(fs, ma, mo, t):
    blocks = [0.5, 1, 2, 4, 8, 16, 32, 64, 128]
    writeBase = u"results/WriteFrame/{ma}/ULA-{fs}/B{bs}-{mo}-{t}-Write.log"
    readBase = u"results/ReadFrame/{ma}/ULA-{fs}/B{bs}-{mo}-{t}-Read.log"
    write_data = []
    read_data = []
    try:
        for bs in blocks:
            write_data.append(table_readWrite.parse_write(
                writeBase.format(t=t, ma=ma, mo=mo, fs=fs, bs=bs)))
            read_data.append(table_readWrite.parse_read(
                readBase.format(t=t, ma=ma, mo=mo, fs=fs, bs=bs)))
        # print(write_data)
        # print(read_data)
        write_stats = table_util.stats(write_data)
        read_stats = table_util.stats(read_data)
        # print(write_stats[0])
        # castTime = []
        # detectSchema = []
        # applySchema = []
        # print(read_stats)
        if write_stats and read_stats:
            csv_base = u"{bs:13.1f}, {wd}, {rd}\n"
            with open(u"plotting/tables/ReadWriteFrame/{ma}/{mo}-{fs}-{t}.csv".format(t=t, ma=ma, mo=mo, fs=fs), "w") as w:
                w.write("blockSize (k), Total Write      , Write Time       ," +
                        " Rand Time        , Compress Mem Size, Normal Mem Size  ," +
                        " Disk Size        ,  Castdtf time    ,detect schema time," +
                        " apply schema time,  Total Read      , Read Time        ," +
                        " Plus Time        , Sum Time         , rightIndex       , toString\n")
                for idx, v in enumerate(blocks):
                    wd = table_readWrite.format_write(
                        write_stats[idx], len(write_stats))
                    rd = table_readWrite.format_read(
                        read_stats[idx], len(read_stats))
                    w.write(csv_base.format(bs=v, wd=wd, rd=rd))
        # else:
            # raise Exception("failed parsing")
            # print(u"Failed Parsing: {0} {1} {2} {3} {4} {5}".format(
                # fs, ma, mo, t, write_stats is None, read_stats is None))
    except Exception as e:
        print("Failed parsing: \n{}\n{}".format(writeBase.format(
            t=t, ma=ma, mo=mo, fs=fs, bs=bs), readBase.format(t=t, ma=ma, mo=mo, fs=fs, bs=bs)))
        raise e


def make_sparsity_table(fs, ma, mo, size):
    writeBase = u"results/WriteFrame/{ma}/ULA-{fs}/B{bs}-{mo}-Sparse{s}-{size}-Binary-Write.log"
    readBase = u"results/ReadFrame/{ma}/ULA-{fs}/B{bs}-{mo}-Sparse{s}-{size}-Binary-Read.log"

    sparsities = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    write_data = [] 
    read_data = []
    for s in sparsities: 
        write_data.append(table_readWrite.parse_write(writeBase.format(ma=ma, fs=fs, bs=16, mo=mo, s=s, size=size)))
        read_data.append(table_readWrite.parse_read(readBase.format(ma=ma, fs=fs, bs=16, mo=mo, s=s, size=size)))

    write_stats = table_util.stats(write_data)
    read_stats = table_util.stats(read_data)
    
    if write_stats and read_stats:
        csv_base = u"{bs:13.1f}, {wd}, {rd}\n"
        with open(u"plotting/tables/ReadWriteFrame/{ma}/{mo}-{fs}-Sparsities-{size}.csv".format(size=size, ma=ma, mo=mo, fs=fs), "w") as w:
            w.write("blockSize (k), Total Write      , Write Time       ," +
                    " Rand Time        , Compress Mem Size, Normal Mem Size  ," +
                    " Disk Size        ,  Castdtf time    ,detect schema time," +
                    " apply schema time,  Total Read      , Read Time        ," +
                    " Plus Time        , Sum Time         , rightIndex       , toString\n")
            for idx, v in enumerate(sparsities):
                wd = table_readWrite.format_write(
                    write_stats[idx], len(write_stats))
                rd = table_readWrite.format_read(
                    read_stats[idx], len(read_stats))
                w.write(csv_base.format(bs=v, wd=wd, rd=rd))

file_types = ["binary"]
ma = "XPS-15-7590"
mo = "singlenode"
targets = ["Sparse0.5-64k-Binary"]


for fs in file_types:
    try:
        for t in targets:
            make_blocks_table(fs, ma, mo, t)

        make_sparsity_table(fs, ma, mo, "64k")
        # make_sparsity_table(fs, ma, mo, "256k")
        # make_distinct_table(fs, ma, mo, "64k")
    except Exception as e:
        traceback.print_exc()
        print(str(e))
