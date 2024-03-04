import matplotlib
import numpy as np
import matplotlib.transforms
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import os
import warnings
import math

warnings.filterwarnings("ignore")


mpl.rcParams["font.family"] = "serif"
plt.rcParams.update({"hatch.color": "#0a0a0a00"})
plt.rcParams.update({"hatch.linewidth": 1.2})


fig_size = (3.33, 1)

fig_sizeh = (3.33 / 2, 1)
dpi = 80


def pars_table(path):
    data = []
    first_line = True
    if os.path.isfile(path):
        with open(path) as f:
            for line in f:
                if first_line:
                    first_line = False
                    continue
                data.append([x.strip() for x in line.split(",")])
    return data


def make_range_single(data):
    if "+-" in data:
        return [float(x) for x in data.split("+-")]
    else:
        return [float(data), 0.0]


def make_range(data):
    return [[make_range_single(y) for y in x] for x in data]


def add_line(
    ax, steps, values, uncertainty, label, linestyle, marker="o", markersize=3
):
    ax.plot(
        steps,
        values,
        label=label,
        linestyle=linestyle,
        linewidth=0.5,
        marker=marker,
        markersize=markersize,
    )

    ax.fill_between(
        steps, values - uncertainty * 2, values + uncertainty * 2, alpha=0.3
    )


def plot_line_data(ax, blocks, data, id, label, linestyle, marker):
    write_total = np.array([x[id][0] for x in data])
    write_var = np.array([x[id][1] for x in data])
    if np.isnan(write_total).all():
        return
    add_line(ax, blocks, write_total, write_var, label, linestyle, marker)


def add_lines(
    data,
    ax,
    names=["Binary", "Comp"],
    ids=[1, 7],
    id_names=["W", "R"],
    line=["dashed"],
    markers=["o", "v", "s", "x", "*"],
):
    block_sizes = [x[0][0] for x in data[0]]
    for idx, d in enumerate(data):
        for idy, ix in enumerate(ids):
            plot_line_data(
                ax,
                block_sizes,
                d,
                ix,
                "{1}-{0}".format(names[idx], id_names[idy]),
                line[0],
                markers[len(data) * idx + idy],
            )


def set_tics_x_log2(ax, abs_min, abs_max):
    x_ticks = []
    s = 2 ** math.ceil(math.log2(abs_min))
    while s <= abs_max:
        x_ticks.append(s)
        s = s * 2
    ax.set_xlim([abs_min, abs_max])
    if x_ticks is not []:
        ax.set_xticks(x_ticks)


def set_tics_x_log10(ax, abs_min, abs_max):
    set_tics_x_log10(ax, abs_min, abs_max)


def set_tics_x_log10(ax, abs_min, abs_max, lim=4):
    x_ticks = []
    if abs_min == 0:
        abs_min = 1
    s = 10 ** math.ceil(math.log10(abs_min))
    while s <= abs_max:
        x_ticks.append(s)
        s = s * 10
    if len(x_ticks) > lim:
        x_ticks = [x_ticks[x] for x in range(0, len(x_ticks), 2)]
    ax.set_xlim([abs_min, abs_max])

    if x_ticks is not []:
        ax.set_xticks(x_ticks)
    return x_ticks


def set_tics_x(ax, abs_min, abs_max, lim=4, include0 = False):
    s = math.ceil(abs_max)

    if s == 0:
        xticks = []
    elif s == 1:
        xticks = [0, s]
    else:
        step = math.floor((s - abs_min) / lim)
        if step == 0:
            step = 1
        if include0:
            xticks = list(range(abs_min , s + 1 , step))
        else: 
            xticks = list(range(abs_min + step, s + 1, step))

    ax.set_xlim([abs_min, s])
    if xticks is not []:
        ax.set_xticks(xticks)

    if s == 1:
        ax.set_xticks([0.25, 0.5, 0.75, 1.0])
        ax.set_xticklabels(["", "", "", "1"])
    elif s == 2:
        ax.set_xticks([0.5, 1, 1.5, 2.0])
        ax.set_xticklabels(["", "1", "", "2"])
    return xticks



def set_tics_y(ax, abs_min, abs_max, lim=4):
    s = math.ceil(abs_max)

    if s <= 4:
        yticks = [1,2,3,4]
        ax.set_ylim([abs_min, s])
        ax.set_yticks([1,2,3,4])
        ax.set_yticklabels(["1", "2", "3", "4"])
        mx = s
    else:
        step = math.ceil((s - abs_min) / lim)
        if step == 0:
            step = 1
        yticks = list(range(abs_min + step, step*lim + 1, step))
        mx = max(s,step*lim)
        if yticks is not []:
            ax.set_yticks(yticks)

        ax.set_ylim([abs_min, mx])

    return yticks



def set_tics_y_float(ax, abs_min, abs_max, lim=4):
    s = math.ceil(abs_max)

    if s == 0:
        yticks = []
    elif s == 1:
        yticks = [0, s]
    else:
        step = (s - abs_min) / lim
        if step == 0:
            step = 1
        yticks = []
        for i in range(lim):
            yticks.append( abs_min + step * i)
        # yticks = list(range(abs_min + step, s + 1, step))

    ax.set_ylim([abs_min, s])
    if yticks is not []:
        ax.set_yticks(yticks)

    if s == 1:
        ax.set_yticks([0.25, 0.5, 0.75, 1.0])
        ax.set_yticklabels(["", "", "", "1"])
    elif s == 2:
        ax.set_yticks([0.5, 1, 1.5, 2.0])
        ax.set_yticklabels(["", "1", "", "2"])
    return yticks


def set_tics_y_log10(ax, abs_min, abs_max, lim= 8):
    try:
        # if(abs_min < 0):
        #     abs_min = 1
        yticks = []
        s = 10 ** math.ceil(math.log10(abs_min))
        while s <= abs_max:
            yticks.append(s)
            s = s * 10
        if len(yticks) > lim:
            yticks = [yticks[x] for x in range(0, len(yticks), 2)]

        ax.set_ylim([abs_min, abs_max])
        if yticks is not []:
            ax.set_yticks(yticks)
        return yticks
    except Exception as e:
        print(abs_min, "   ", abs_max)

        raise e
    
