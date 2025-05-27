import os
import numpy as np
import pandas as pd
from utils.metrics import nrmse
from data_loader import DataFactory
from compression.line_simplification import LineSimplification

def run_ls_cr_experiments():
    factory = DataFactory()
    datasets = list(factory.loaders.keys())
    cr_nrmse_results = {"dataset": [], "line_simplification": [], "error_bound": [], "cr": [], "nrmse": []}
    print('Running compression ratio experiments')
    print('----------------------------------')
    try:
        previous_results = pd.read_csv(os.path.join('results', 'fixed_cr_nrmse_results.csv'))        
        for metric in cr_nrmse_results.keys():
            cr_nrmse_results[metric] = previous_results[metric].tolist()
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
        
        for error_bound in error_bounds:
            for target in ['tp', 'pip', 'vw', 'sip']:
                print("Compressing with", target, "at error bound", error_bound, "in dataset", dataset)
                line_simp.set_target(target)
                comp_y = line_simp.compress(y.copy(), error_bound, nlags, blocking, kappa)
                decomp_y = line_simp.decompress(comp_y)
                cr_nrmse_results["dataset"].append(dataset)
                cr_nrmse_results["line_simplification"].append(target)
                cr_nrmse_results["error_bound"].append(error_bound)
                cr_nrmse_results["nrmse"].append(np.round(nrmse(y, decomp_y), 4))
                cr_nrmse_results["cr"].append(round(len(y)/len(comp_y), 2))

            pd.DataFrame(cr_nrmse_results).to_csv(os.path.join('results', 'line_simplification_results.csv'), index=False)

if __name__ == '__main__':
    run_ls_cr_experiments()