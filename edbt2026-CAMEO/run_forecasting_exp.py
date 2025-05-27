import os
import numpy as np
import pandas as pd
from data_loader import DataFactory
from compression.sp_compressor import SimPiece
from compression.model_compressor import ModelCompressor
from experiments.forecasting.pedestrian.run_model import compress_and_forecast
from compression.line_simplification import LineSimplification


if __name__ == '__main__':
    factory = DataFactory()
    datasets = list(factory.loaders.keys())
    
    for forecasting_model in ['stlf', 'arima']:    
        for compressor in ['ped_mae_cameo', 'ped_rmse_cameo', 'ped_cheb_cameo']:    
            for error_bound in LineSimplification.name_map_coef[compressor]:
                print(f"Running {compressor} with error bound {error_bound}")
                compress_and_forecast(forecasting_model, compressor, error_bound)
        
        for target in ['pmc', 'swing', 'sp', 'swab']:
            print("Compressing with", target, "at error bound", error_bound, "in pedestrian", flush=True)

            if target in ['pmc', 'swing']:
                for error_bound in ModelCompressor.name_map_coef[target]:    
                   compress_and_forecast(forecasting_model, target, error_bound) 
            elif target == 'sp':
                for error_bound in SimPiece.name_map_coef[target]:
                    compress_and_forecast(forecasting_model, target, error_bound)    
            else:
                for error_bound in [0.01, 0.05, 0.1, 0.2]:
                    compress_and_forecast(forecasting_model, target, error_bound)