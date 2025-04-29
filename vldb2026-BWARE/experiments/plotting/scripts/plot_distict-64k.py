
import plot_readWrite

plot_readWrite.plot_execute(
    "Distinct", source="Distinct-64k",
    x_label="# Distinct values",
    x_scale=[1, 65536],
    x_ticks=[1, 4, 16, 64, 256, 1024, 4096, 16384, 65536],
    y_scales=[[0.3, 40], [1000, 30000000000], [0.03, 15], ],
    log_x=True)
