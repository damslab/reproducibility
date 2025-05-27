import os
import numpy as np
import pandas as pd
from utils.metrics import nrmse
import time
from data_loader import DataFactory
from compression.line_simplification import LineSimplification

def run_blocking_experiments():
    factory = DataFactory()
    datasets = list(factory.loaders.keys())
    blocking_results = {"dataset": [], "line_simplification": [], "error_bound": [], "cr": [], "nrmse": [], 'blocking': [], 'kappa': [], 'execution_time': [], 'threads': []}
    print('Running compression ratio experiments')
    print('----------------------------------')
    try:
        previous_results = pd.read_csv(os.path.join('results', 'solar_blocking_results.csv'))        
        for metric in blocking_results.keys():
            blocking_results[metric] = previous_results[metric].tolist()
    except:
        previous_results = pd.DataFrame()
    
    for dataset in datasets:
        line_simp = LineSimplification()
        data_loader = factory.load_data(dataset, 'data')
        y = np.squeeze(data_loader.data.values)
        nlags = data_loader.seasonality
        kappa = data_loader.aggregation
        error_bounds = line_simp.sip_error_bounds
        if kappa:
            y = y[:(y.shape[0]//kappa)*kappa]
            if dataset == 'solar4seconds':
                error_bounds = line_simp.solar_sip_error_bounds
            else:
                error_bounds = line_simp.agg_sip_error_bounds

        blocking = y.shape[0] // 2
        
        if not previous_results.empty:
            dataset_results = previous_results[previous_results['dataset'] == dataset]
            if not dataset_results.empty and dataset_results.shape[0] == len(error_bounds)*4:
                print("Skipping dataset", dataset)
                continue
            
        target = 'fgc_sip_cr'
        for error_bound in [10]:
            for blocking_constant in [3, 5, 7, 10, -1]:
                for threads in [1, 2, 4, 6, 8, 10, 12, 14, 16]:
                    running_times = []
                    
                    print("Compressing with", target, "at error bound", error_bound, "in dataset", dataset)
                    line_simp.set_target(target if threads != 1 else 'lpc_sip_cr')
                    
                    blocking = int(blocking_constant * np.log2(y.shape[0]))

                    if blocking_constant == -1:
                        blocking = y.shape[0] // 2
                    
                    for _ in range(5):
                        start = time.time()
                        comp_y = line_simp.compress(y.copy(), acf_threshold=error_bound, nlags=nlags, blocking=blocking, kappa=kappa, threads=threads)
                        end = time.time()
                        running_times.append(end-start)
                    
                    decomp_y = line_simp.decompress(comp_y)
                    blocking_results["dataset"].append(dataset)
                    blocking_results["line_simplification"].append(target)
                    blocking_results["error_bound"].append(error_bound)
                    blocking_results["nrmse"].append(np.round(nrmse(y, decomp_y), 4))
                    blocking_results["cr"].append(round(len(y)/len(comp_y), 2))
                    blocking_results["blocking"].append(blocking_constant)
                    blocking_results["kappa"].append(kappa if kappa else 0)
                    blocking_results["execution_time"].append(round(np.mean(running_times), 3))
                    blocking_results["threads"].append(threads)

                pd.DataFrame(blocking_results).to_csv(os.path.join('results', 'solar_blocking_results.csv'), index=False)

if __name__ == '__main__':
    run_blocking_experiments()