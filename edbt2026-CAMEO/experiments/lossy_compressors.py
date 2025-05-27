import os
import numpy as np
import pandas as pd
from utils.metrics import nrmse
from data_loader import DataFactory
from compression.model_compressor import ModelCompressor
from compression.line_simplification import LineSimplification
from compression.sp_compressor import SimPiece


def auto_corr(x, max_lag):
    return np.asarray([np.corrcoef(x[:-lag], x[lag:])[0, 1] for lag in range(1, max_lag+1)])

def extract_agg(x, m):
    if m:
        new_size = x.shape[0] // m
        a = x[:new_size * m].reshape(new_size, m)
        return np.nanmean(a, axis=1)

    return x


def run_lc_cr_experiments():
    factory = DataFactory()
    datasets = list(factory.loaders.keys())
    cr_nrmse_results = {"dataset": [], "lossy_compression": [], "error_bound": [], "cr": [], "nrmse": [], "acf_error": []}

    
    for dataset in datasets:
        data_loader = factory.load_data(dataset, 'data')
        uncompressed = np.squeeze(data_loader.data.values)
        nlags = data_loader.seasonality
        kappa = data_loader.aggregation
        raw_acf = auto_corr(uncompressed, nlags)
        
        if kappa:
            uncompressed = uncompressed[:(uncompressed.shape[0]//kappa)*kappa]
            agg_ts = extract_agg(uncompressed, kappa)       
            raw_acf = auto_corr(agg_ts, nlags)     
        
        for error_bound in ModelCompressor.coefficients:
            for target in ['pmc', 'swing', 'sp', 'swab']:
                print("Compressing with", target, "at error bound", error_bound, "in dataset", dataset, flush=True)

                if target in ['pmc', 'swing']:
                    compressor = ModelCompressor(uncompressed, dataset)
                    compressed = compressor.compress(target, error_bound)
                    decompressed_data = np.squeeze(compressor.decompress(target, error_bound))
                elif target == 'sp':
                    error_bound = (np.max(uncompressed)-np.min(uncompressed))*error_bound/100
                    compressed = SimPiece().compress(uncompressed, error_bound)
                    decompressed_data = SimPiece().decompress(compressed)
                else:
                    error_bound = (np.max(uncompressed)-np.min(uncompressed))*error_bound/100
                    line_simp = LineSimplification()
                    line_simp.set_target(target)
                    compressed = line_simp.compress(uncompressed.copy(), error_bound)
                    decompressed_data = line_simp.decompress(compressed)

                            
                cr_nrmse_results["dataset"].append(dataset)
                cr_nrmse_results["lossy_compression"].append(target)
                cr_nrmse_results["error_bound"].append(round(error_bound, 2))
                cr_nrmse_results["nrmse"].append(np.round(nrmse(uncompressed, decompressed_data), 4))
                if target == 'pmc':
                    cr_nrmse_results["cr"].append(round(len(uncompressed)/(compressed.shape[0]), 2))
                elif target == 'swing':
                    cr_nrmse_results["cr"].append(round(len(uncompressed)/(compressed.shape[0]*2), 2))
                elif target == 'swab':
                    cr_nrmse_results["cr"].append(round(len(uncompressed)/(compressed.shape[0]), 2))
                elif target == 'sp':
                    cr_nrmse_results["cr"].append(round(len(uncompressed)*8/(compressed.shape[0]), 2))
                
                if kappa:
                    decompressed_data = extract_agg(decompressed_data, kappa)

                acf_error = np.mean(np.abs(auto_corr(decompressed_data, nlags) - raw_acf))
                cr_nrmse_results["acf_error"].append(np.round(acf_error, 4))


            pd.DataFrame(cr_nrmse_results).to_csv(os.path.join('results', 'lossy_compression_results.csv'), index=False)
            


if __name__ == '__main__':
    run_lc_cr_experiments