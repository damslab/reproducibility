import os
import subprocess
import numpy as np
import pandas as pd
from data_loader import DataFactory

def auto_corr(x, max_lag):
    return np.asarray([np.corrcoef(x[:-lag], x[lag:])[0, 1] for lag in range(1, max_lag+1)])

def extract_agg(x, m):
    if m:
        new_size = x.shape[0] // m
        a = x[:new_size * m].reshape(new_size, m)
        return np.nanmean(a, axis=1)

    return x


def run_exp():
    factory = DataFactory()
    datasets = list(factory.loaders.keys())
    results = {'dataset': [], 'error_bound': [], 'bit_rate': [], 'acf_error': []}

    for dataset in datasets:
        data_loader = factory.load_data(dataset, 'data')
        nlags = data_loader.seasonality
        kappa = data_loader.aggregation
        ts = np.squeeze(data_loader.data.values)
        size = ts.shape[0]
        raw_acf = auto_corr(ts, nlags)
        if kappa:
            agg_ts = extract_agg(ts ,kappa)
            raw_acf = auto_corr(agg_ts, nlags)
        
        with open(f'data/sz_compressed/{dataset}.dat', 'wb') as f:
            f.write(ts.tobytes())
        
        for per in np.linspace(0.0, 0.001, 2):
            error_bound = (ts.max() - ts.min())*per
            
            subprocess.run(["sz3", "-d", "-i", f'data/sz_compressed/{dataset}.dat', "-z", f"data/sz_compressed/{dataset}.sz", 
                            "-o", f"data/sz_compressed/{dataset}.out", "-1", str(size), '-M',  'ABS', str(error_bound)]) 
            
            size_in_bytes = os.path.getsize(f'data/sz_compressed/{dataset}.sz')
            size_in_bits = size_in_bytes * 8        


            with open(f'data/sz_compressed/{dataset}.out', 'rb') as f:
                buffer = f.read()
                decompressed_data = np.frombuffer(buffer, np.float64)    

            
            if kappa:
                decompressed_data = extract_agg(decompressed_data, kappa)

            acf_error = np.mean(np.abs(auto_corr(decompressed_data, nlags) - raw_acf))

            results['dataset'].append(dataset)
            results['error_bound'].append(per)
            results['bit_rate'].append(np.round(size_in_bits/size, 2))
            results['acf_error'].append(np.round(acf_error, 6))
        
        pd.DataFrame(results).to_csv('reproducibility/results/sz_results.csv', index=False)
        
        
    
