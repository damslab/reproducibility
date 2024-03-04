
import plot_readWrite

plot_readWrite.plot_execute("Sparsities-64k",
             x_label="Sparsity in %",
             x_scale=[-0.01, 1.01], x_ticks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
             y_scales=[[0.3, 10], [1, 30000000000], [0.003, 15], ],
             log_x=False)
plot_readWrite.plot_execute("Sparsities-to-0.1-64k", source="Sparsities-64k",
             x_label="Sparsity in %",
             x_scale=[-0.001, .101], x_ticks=[0.0, 0.02, 0.04, 0.06, 0.08, .1],
             y_scales=[[0.3, 10], [1000, 30000000000], [0.003, 15], ],
             log_x=False)
plot_readWrite.plot_execute("Sparsities-to-0.9-64k", source="Sparsities-64k",
             x_label="Sparsity in %",
             x_scale=[0.899, 1.001], x_ticks=[0.9, 0.92, 0.94, 0.96, 0.98, 1.0],
             y_scales=[[0.3, 10], [1000, 30000000000], [0.003, 15], ],
             log_x=False)
