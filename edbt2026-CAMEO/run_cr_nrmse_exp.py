from experiments import line_simplificators
from experiments import blocking
from experiments import lossy_compressors

line_simplificators.run_ls_cr_experiments()
lossy_compressors.run_lc_cr_experiments()
blocking.run_blocking_experiments()

