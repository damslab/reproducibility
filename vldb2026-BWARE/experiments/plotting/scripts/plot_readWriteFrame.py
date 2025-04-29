import matplotlib.pyplot as plt

import plot_util as pu




def plot(out, ax,
         x_scale=None, x_ticks=None, x_label="Block Size in # ⋅ 1000",
         y_scale=[0.5, 10], y_label="Execution Time [s]", y_tics=None, y_labels=None,
         log_x=True, log_y=True):
    if log_x:
        ax.set_xscale('log', base=2)
    if log_y:
        ax.set_yscale('log')
    pu.set_tics_x_log2(ax, 0.5, 128)

    if y_tics:
        ax.set_yticks(y_tics)
        ax.set_yticklabels(y_labels)
        plt.ylim([y_scale[0], y_scale[1]])

    else:
        pu.set_tics_y_log10(ax, y_scale[0], y_scale[1])

    if x_scale:
        plt.xlim(x_scale[0], x_scale[1])
    if x_ticks:
        ax.set_xticks(x_ticks)

    ax.yaxis.set_label_coords(-0.13, 0.81)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    plt.subplots_adjust(left=0.15, right=0.97, top=0.85,
                        bottom=0.28, wspace=0.35, hspace=0.35)
    ax.legend(ncol=2, loc="upper center", bbox_to_anchor=(0.32, 1.27),
              fontsize=7.45)
    plt.grid(True, "major", axis='both', ls='--', linewidth=0.3, alpha=0.8)
    plt.savefig(out, dpi=1600)
    plt.close()


def plot_execute(name, source=None,
                 x_scale=None, x_ticks=None, x_label="Block Size in # ⋅ 1000",
                 y_scales=[[0.5, 10], [1000000, 20000000000], [0.05, 5]], log_x=True, log_y=True):
    if source is None:
        source = name
    b = "plotting/tables/ReadWriteFrame/XPS-15-7590/singlenode-binary-"+source+".csv"
    c = "plotting/tables/ReadWriteFrame/XPS-15-7590/singlenode-compressed-"+source+".csv"
    bd = pu.make_range(pu.pars_table(b))
    cd = pu.make_range(pu.pars_table(c))


    # # End-to-End
    # _, ax = plt.subplots(1, 1, num=None, figsize=pu.fig_size,
    #                      dpi=pu.dpi, facecolor="w", edgecolor="k")
    # add_lines([bd, cd], ax)
    # plot("plotting/plots/ReadWriteFrame/XPS-15-7590/end_to_end_"+name+".pdf", ax,
    #      y_scale=y_scales[0], x_scale=x_scale, x_ticks=x_ticks, x_label=x_label,
    #      log_x=log_x, log_y=log_y)

    # # IO Plot
    _, ax = plt.subplots(1, 1, num=None, figsize=pu.fig_size,
                         dpi=pu.dpi, facecolor="w", edgecolor="k")
    pu.add_lines([bd], ax, ids=[2,  11])
    plot("plotting/plots/ReadWriteFrame/XPS-15-7590/IO_"+name+".pdf", ax,
         y_scale=y_scales[2], x_scale=x_scale, x_ticks=x_ticks, x_label=x_label,
         log_x=log_x, log_y=log_y)

    # # Disk size
    _, ax = plt.subplots(1, 1, num=None, figsize=pu.fig_size,
                         dpi=pu.dpi, facecolor="w", edgecolor="k")
    # add_lines([cd], ax, ids=[4,  6], id_names=["M", "D"], names=["Comp"])
    # add_lines([cd], ax, ids=[5], id_names=["M"], names=["UnComp"])
    pu.add_lines([bd], ax, ids=[6], id_names=["D"], names=["Binary"])
    plot("plotting/plots/ReadWriteFrame/XPS-15-7590/size" + name+".pdf", ax,
         y_scale=y_scales[1], y_label="Size [Bytes]",
         y_tics=[1, 1000, 1000000, 1000000000], y_labels=["B", "KB", "MB", "GB"],
         x_scale=x_scale, x_ticks=x_ticks, x_label=x_label,
         log_x=log_x, log_y=log_y)

