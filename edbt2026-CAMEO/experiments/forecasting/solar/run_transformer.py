import zipfile
from os.path import join as path_join
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from darts.models import TransformerModel
from darts import TimeSeries
from compression.line_simplification import LineSimplification
from statsmodels.tools.eval_measures import rmse
import torch


class Solar4Seconds():
    file_name = 'solar_4_seconds_dataset.zip'
    freq = '4s'
    name = 'solar4seconds'
    aggregation = 120
    forecasting_horizon = 24
    fs = 2. / 3600.

    def __init__(self):
        self.data = pd.DataFrame()

    def load(self, file_path):
        with zipfile.ZipFile(path_join(file_path, self.file_name)) as _zip:
            for filename in _zip.namelist():
                with _zip.open(filename) as f:
                    for i, line in enumerate(f):
                        if i == 15:
                            line = str(line)
                            _, timestamp, points = line.split(':')
                            points = points.split(',')
                            points[-1] = points[-1][:-5]
                            self.data['y'] = np.asarray(points, dtype=float)
                            ts = pd.date_range(start=pd.to_datetime(timestamp), freq=self.freq, periods=len(self.data))
                            self.data.set_index(ts, inplace=True)

        self.data = self.data.resample('30min').mean()
        print(self.data.shape)

    def prepare_for_parquet(self):
        self.data.reset_index(inplace=True)
        self.data.rename({'index': 'datetime'}, axis=1, inplace=True)


torch.set_float32_matmul_precision('medium')
torch.manual_seed(0)
np.random.seed(0)

def msmape(forecasts, test_set):
    forecasts = forecasts[np.newaxis, :]
    test_set = test_set[np.newaxis, :]
    epsilon = 0.1
    comparator = np.full(test_set.shape, 0.5 + epsilon)
    sum_val = np.maximum(comparator, (np.abs(forecasts) + np.abs(test_set) + epsilon))
    smape = 2 * np.abs(forecasts - test_set) / sum_val
    msmape_per_series = np.nanmean(smape, axis=1)
    return msmape_per_series


def get_harmonics(dti, freq='h'):
    harmonics = pd.DataFrame({'date': dti})
    harmonics['date'] = pd.PeriodIndex(harmonics['date'], freq=freq)
    harmonics.set_index('date', inplace=True)
    harmonics.sort_index(inplace=True)

    harmonics[f'sin-1har'] = np.sin(2 * np.pi * (harmonics.index.hour * 60 + harmonics.index.minute) / (24 * 60))
    harmonics[f'cos-1har'] = np.cos(2 * np.pi * (harmonics.index.hour * 60 + harmonics.index.minute) / (24 * 60))

    return harmonics


def main():
    loader = Solar4Seconds()
    loader.load('data/')
    ts = loader.data.values
    scaler = StandardScaler()
    X = np.squeeze(scaler.fit_transform(ts))

    lookback = 336

    x_train = X[:-lookback]
    x_test = X[-lookback:]
    x_test = scaler.inverse_transform(x_test[:, np.newaxis]).squeeze()

    model = TransformerModel(
                    input_chunk_length=lookback,
                    output_chunk_length=lookback,
                    batch_size=32,
                    n_epochs=10,
                    model_name="solar_transformer",
                    nr_epochs_val_period=2,
                    d_model=16,
                    nhead=8,
                    num_encoder_layers=2,
                    num_decoder_layers=2,
                    dim_feedforward=128,
                    dropout=0.1,
                    activation="relu",
                    random_state=42,
                    save_checkpoints=True,
                    force_reset=True,
    )

    x_train_time_series = TimeSeries.from_values(x_train)
    model.fit(x_train_time_series)
    forecast = model.predict(lookback)
    forecast = np.squeeze(forecast.values())
    forecast = scaler.inverse_transform(forecast[:, np.newaxis]).squeeze()
    rmse_raw_results = rmse(forecast, x_test)
    msmape_raw_results = msmape(forecast, x_test)
    print()
    print("RMSE", rmse_raw_results)
    print("MSMAPE", msmape_raw_results)
    print()


    pmc_rmse_results = [rmse_raw_results]
    pmc_msmape_results = [msmape_raw_results[0]]
    pmc_cr = [1.]

    for error in [0.2, 0.5, 1.0, 1.5, 1.7, 1.8, 1.83, 1.84, 1.845]:
        compressor = LineSimplification()
        compressor.set_target('pmc')
        compressed_data = compressor.compress(pts=x_train.copy(), acf_threshold=error, blocking=x_train.shape[0]//2, nlags=48)
        print(f"Compression Ratio {error}", 2*((x_train.shape[0]*8)/len(compressed_data)), flush=True)
        pmc_cr.append(2*((x_train.shape[0]*8)/len(compressed_data)))
        decompressed_data = np.asarray(compressor.decompress(compressed_data))

        model = TransformerModel(
                    input_chunk_length=lookback,
                    output_chunk_length=lookback,
                    batch_size=32,
                    n_epochs=10,
                    model_name="solar_pmc_trans%f"%error,
                    nr_epochs_val_period=2,
                    d_model=16,
                    nhead=8,
                    num_encoder_layers=2,
                    num_decoder_layers=2,
                    dim_feedforward=128,
                    dropout=0.1,
                    activation="relu",
                    random_state=42,
                    save_checkpoints=True,
                    force_reset=True,
        )


        decompressed_time_series = TimeSeries.from_values(decompressed_data)
        model.fit(decompressed_time_series)
        forecast = model.predict(lookback)
        forecast = np.squeeze(forecast.values())
        forecast = scaler.inverse_transform(forecast[:, np.newaxis]).squeeze()
        print("RMSE", rmse(forecast, x_test))
        print("MSMAPE", msmape(forecast, x_test), flush=True)
        pmc_rmse_results.append(rmse(forecast, x_test))
        pmc_msmape_results.append(msmape(forecast, x_test)[0])

    acf_rmse_results = [rmse_raw_results]
    acf_msmape_results = [msmape_raw_results[0]]
    acf_cr = [1.]

    for error in [0.001, 0.08, 0.1, 0.2, 0.3, 0.5, 0.6, 0.63]:
        compressor = LineSimplification()
        compressor.set_target('sip')
        compressed_data = compressor.compress(pts=x_train.copy(), acf_threshold=error, blocking=x_train.shape[0]//2, nlags=48)
        print("Compression Ratio", x_train.shape[0]/compressed_data.shape[0], flush=True)
        acf_cr.append(x_train.shape[0]/compressed_data.shape[0])
        decompressed_data = np.interp(np.arange(x_train.shape[0]), compressed_data[:, 0], compressed_data[:, 1])

        model = TransformerModel(
                    input_chunk_length=lookback,
                    output_chunk_length=lookback,
                    batch_size=32,
                    n_epochs=10,
                    model_name="solar_sip_trans%f"%error,
                    nr_epochs_val_period=2,
                    d_model=16,
                    nhead=8,
                    num_encoder_layers=2,
                    num_decoder_layers=2,
                    dim_feedforward=128,
                    dropout=0.1,
                    activation="relu",
                    random_state=42,
                    save_checkpoints=True,
                    force_reset=True,
        )
        decompressed_time_series = TimeSeries.from_values(decompressed_data)
        model.fit(decompressed_time_series)
        forecast = model.predict(lookback)
        forecast = np.squeeze(forecast.values())
        forecast = scaler.inverse_transform(forecast[:, np.newaxis]).squeeze()
        
        print("RMSE", rmse(forecast, x_test))
        print("MSMAPE", msmape(forecast, x_test), flush=True)
        acf_rmse_results.append(rmse(forecast, x_test))
        acf_msmape_results.append(msmape(forecast, x_test)[0])

    area_rmse_results = [rmse_raw_results]
    area_msmape_results = [msmape_raw_results[0]]
    area_cr = [1.]
    
    for error in [0.01, 0.02, 0.05, 0.1, 0.3, 0.4, 0.5, 0.6, 0.65, 0.7]:
        compressor = LineSimplification()
        compressor.set_target('vw')
        compressed_data = compressor.compress(pts=x_train.copy(), acf_threshold=error, blocking=x_train.shape[0]//2, nlags=48)
        print("Compression Ratio", x_train.shape[0]/compressed_data.shape[0], flush=True)
        area_cr.append(x_train.shape[0]/compressed_data.shape[0])
        decompressed_data = np.interp(np.arange(x_train.shape[0]), compressed_data[:, 0], compressed_data[:, 1])

        model = TransformerModel(
                    input_chunk_length=lookback,
                    output_chunk_length=lookback,
                    batch_size=32,
                    n_epochs=10,
                    model_name="solar_vw_trans%f"%error,
                    nr_epochs_val_period=2,
                    d_model=16,
                    nhead=8,
                    num_encoder_layers=2,
                    num_decoder_layers=2,
                    dim_feedforward=128,
                    dropout=0.1,
                    activation="relu",
                    random_state=42,
                    save_checkpoints=True,
                    force_reset=True,
        )

        decompressed_time_series = TimeSeries.from_values(decompressed_data)
        model.fit(decompressed_time_series)
        forecast = model.predict(lookback)
        forecast = np.squeeze(forecast.values())
        forecast = scaler.inverse_transform(forecast[:, np.newaxis]).squeeze()
        # Calculate MSE
        print("RMSE", rmse(forecast, x_test))
        print("MSMAPE", msmape(forecast, x_test)[0], flush=True)
        
        area_rmse_results.append(rmse(forecast, x_test))
        area_msmape_results.append(msmape(forecast, x_test)[0])

    
    area_results = pd.DataFrame({'area_cr': area_cr,
                                 'area_rmse_results': area_rmse_results,
                                 'area_msmape_results': area_msmape_results}).set_index('area_cr')
    acf_results = pd.DataFrame({'acf_cr': acf_cr,
                                'acf_rmse_results': acf_rmse_results,
                                'acf_msmape_results': acf_msmape_results}).set_index('acf_cr')
    pmc_results = pd.DataFrame({'pmc_cr': pmc_cr,
                                 'pmc_rmse_results': pmc_rmse_results,
                                 'pmc_msmape_results': pmc_msmape_results}).set_index('pmc_cr')

    
    pmc_results.to_csv('results/solar/transformer_solar_pmc_results.csv')
    area_results.to_csv('results/solar/transformer_solar_area_results.csv')
    acf_results.to_csv('results/solar/transformer_solar_acf_results.csv')
    
    print('Experiments completed')


if __name__ == '__main__':
    main()
