from pathlib import Path
import os

import matplotlib.pyplot as plt

import plot_util as pu
import math
import numpy as np
import table_util as tb

def key_1(rows, cols, sp, uniq, threads, id):
    return (int(rows) * int(cols) * 8, int(threads))


def order_1(rows, cols, sp, uniq, threads, id):
    return rows + "_" + cols + "_" + sp + "_" + uniq + "_" + threads + "_" + str(id)


def take_1(data):
    ret = {}
    for k in data:
        ret[k] = data[k][1]
    return ret


def filter_1(data):
    if(len(data) == 8):
        return float(data[5]) == 12 and float(data[4]) != 1
    else:
        return False


def filter_2(data):
    if(len(data) == 8):
        return float(data[5]) == 12 and float(data[4]) == 1
    else:
        return False



def splitV(v):
    try:
        data = v.split(",")
        time = data[0].split("+-")
        inSize = data[1].split("+-")
        outSize = data[2].split("+-")
        time[1] = time[1][:-2]
        inSize[1] = inSize[1][:-6]
        outSize[1] = outSize[1][:-6]
        time = [float(x.strip()) for x in time]
        inSize = [float(x.strip()) for x in inSize]
        outSize = [float(x.strip()) for x in outSize]
        return time, inSize, outSize
    except Exception as e:
        print(e)
        print(v)
        exit(-1)


def parse(path):
    data = {}
    with open(path) as f:
        for l in f:
            if "Profiling started\n" in l:
                continue
            elif len(l) < 30:
                continue
            elif "(" in l:
                continue
                # elif "Performance counter " in l:
                # return data
            elif " Serialize  Repetitions:" in l:
                continue
            elif "Performance counter stats" in l:
                return data
            # Everything else:
            kv = l.split(",", 1)
            if len(kv) > 1:
                k = kv[0].strip()
                v = kv[1].strip()
                data[k] = splitV(v)
    return data


def parse_params(path):
    p = str(path)
    f = p.split("/")[-1]
    return f[4:-4].split("-")


def use_key(props, key):
    if len(props) == 6:
        return key(
            rows=props[0],
            cols=props[1],
            sp=props[3],
            uniq=props[2],
            threads=props[4],
            id=-1,
        )
    else:
        return key(
            rows=props[0],
            cols=props[1],
            sp=props[3],
            uniq=props[2],
            threads=props[4],
            id=props[5],
        )


def fix(d):
    ret = {}
    for k in d:
        a = d[k]
        for aa in a:
            for key in aa[1]:
                full_key = str(k) + "_" + key
                if k in ret.keys():
                    ret[k].append([key, aa[1][key]])
                else:
                    ret[k] = [[key, aa[1][key]]]

    for k in ret:
        ret[k] = [[a[0], a[1][0], a[1][1]] for a in ret[k]]

    return ret


def parse_all(machine, t=take_1, k=key_1, o=order_1, f=filter_1):
    path_list = Path("results/performance/" + machine).glob("Serial/**/*.log")
    ret1 = {}
    for p in path_list:
        props = parse_params(p)
        if f(props):
            d = parse(p)
            if d == None:
                continue
            key = use_key(props, k)
            ord = use_key(props, o)
            if key in ret1.keys():
                ret1[use_key(props, k)].append([ord, t(d)])
            else:
                ret1[use_key(props, k)] = [[ord, t(d)]]

    ret = fix(ret1)
    return ret

def parse_dd(machine):
    p = "results/diskSpeed/"+machine+"-diskspeed.log"
    if os.path.isfile(p):
        ret = []
        with open(p) as f:
            for l in f:
                if len(l) < 30:
                    # new entry
                    ret.append([])

                else:
                    speed = l.split("copied,")[1].split("s,")[1].strip()

                    ret[-1].append(parseSpeed(speed))
        
        # print(ret)
        ret = [tb.st(x) for x in ret]

        return ret;

    else:
        return []

def parseSpeed(st):
    if "MB" in st:
        return float(st.split(" ")[0])* 1024*1024
    elif "GB" in st:
        return float(st.split(" ")[0])* 1024*1024*1024
    elif "KB" in st:
        return float(st.split(" ")[0])* 1024
    else:
        return float(st)



def plot(d, machine, par=48, name="plt"):

    filter = {
        f"StandardDisk {par}":"ULA", 
        f"Compress StandardIO {par}":"CLA",
        f"Update&Apply Standard IO {par}":"U&A"}
    
    plotA(d, machine, filter=filter, par = par, name = name)

def plotR(d, machine,par, name):

    filter = {
        f"StandardRead {par}":"ULA", 
        f"StandardCompressedRead {par}":"CLA"}
    
    plotA(d, machine, filter=filter, par = par, name = name)

def plotA(d, machine, filter,par=48, name="plt"):
    if len(d) == 0:
        return

    plt.rc('xtick', labelsize=8)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=8) 
    _, ax = plt.subplots(
        1, 1, num=None, figsize=pu.fig_size, dpi=pu.dpi, facecolor="w", edgecolor="k"
    )

    ax.set_xscale("log", base=10)
    # x = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
   
    # y_labels = ["B/s", "$10$", "$10^(2)$", "KiB/s", "$10^4$", "$10^5$",
    #             "MiB/s", "$10^7$", "$10^8$", "GiB/s", "$10^[10]$", "$10^11$", "TiB/s"]
    ymin = None
    ymax = None
    x_tics = []
    x = []
    markers=["o", "v", "s", "x", "*", "^", "<", "p"]
    markid = 0
    for k in filter:
        # if k in filter.keys():
            x = np.array([a[0] for a in d[k]])
            y = np.array([a[1] for a in d[k]])
            err = []
            for a in d[k]:
                if a[1] - a[2] < 0:
                    err.append(a[1] * 0.2)
                else:
                    err.append(a[2])


            err = np.array(err);
          
            
            # plt.bar()
            pu.add_line(ax, x, y, err, filter[k], "dashed", markers[markid], markersize=3)
            markid += 1
            # pu.add_line(ax, x, y, err, k, "dashed", "o", markersize=1)

            if ymin == None:
                ymin = min(y)
                ymax = max(y)
            else:
                ymin = min(min(y), ymin)
                ymax = max(max(y), ymax)
            if len(x) > len(x_tics):
                x_tics = x


   
    # dd = parse_dd(machine)
    # if len(dd) > 0:
    #     xm = x[:len(dd)]
    #     y = np.array([x[0] for x in dd])
    #     err = np.array([x[1] for x in dd])

    #     pu.add_line(ax, xm, y, err, "dd", "dashed", "o", markersize=1)
    # if "so" in machine:
    #     bandwidth = 200 * 1024 * 1024 * 1024
    # elif machine == "XPS-15-7590":
    #     bandwidth = 21333 * 1024 * 1024 * 2
    # ax.axhline(bandwidth, 0, max(x_tics), label="MemBandWidth", linewidth=0.5)

    # ymax = max(bandwidth, ymax)

    ax.set_ylabel("# Bytes / sec")
    ax.set_xlabel("# Bytes Input")
    ax.xaxis.set_label_coords(0.5, -0.22)
    ax.yaxis.set_label_coords(-0.17, 0.61)
    
    if len(x) < 10:
        ax.set_xticks(x)
        ax.set_xticklabels(["80K", "", "8M", "", "800M", "", "80G"][:len(x)])
    ax.set_yscale("log")
    pu.set_tics_y_log10(ax, ymin/6, ymax*4)
    # ax.set_yticks(y_tics[7:])
    ax.set_ylim([ymin / 6, ymax * 4])

    ax.set_xmargin(0.01)
 
    plt.subplots_adjust(
        left=0.19, right=0.94, top=0.91, bottom=0.27, wspace=0.35, hspace=0.35
    )
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.13), fontsize=6.5)
    plt.grid(True, "major", axis="both", ls="--", linewidth=0.4, alpha=0.8)
    plt.savefig("plotting/plots/Performance/" + machine + "/" + name + ".pdf", dpi=1600)

    plt.close()


def reverse(data):
    ret = {}
    for k in data:
        for v in data[k]:
            key = v[0] +" "+ str(k[1])
            if key in ret.keys():
                ret[key].append([k[0], v[1], v[2]])
                ret[key].sort()
            else:
                ret[key] = [[k[0], v[1], v[2]]]

    return ret


if __name__ == "__main__":
    for m in ["dams-su1","dams-so002", "dams-so009", "dams-so011"]:
        try:

            d = parse_all(m, f=filter_1)
            d = reverse(d)
            if m == "dams-su1":
                plot(d, m, 128,"SerialParallel")
                plotR(d, m, 128, "ReadParallel")
            else:
                plot(d, m, 48,"SerialParallel")
                plotR(d, m, 48, "ReadParallel")

            d = parse_all(m, f=filter_2)
            d = reverse(d)
            plot(d, m, 1,"SerialSingle")
            plotR(d, m, 1, "ReadSingle")



            # d = parse_all(m, f=filter_3)
        except Exception as e:
            print(e)
    # plot(parse_all(m, f=filter_800MB100), m, "800MB100%")
    # m = "XPS-15-7590"
    # plot(parse_all(m, f=filter_2), m, "12MB1%")
    # plot(parse_all(m, f=filter_800MB100), m, "800MB100%")
    # plot(parse_all(m, f=filter_1sparsity), m, "1%Sparsity")
    # plot(parse_all(m, f=filter_38sparsity), m, "38%Sparsity")
    # plot(parse_all(m, f=filter_noSparse), m, "Dense")
