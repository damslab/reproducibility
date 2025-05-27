import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from darts.models import BlockRNNModel
import numpy as np
from darts import TimeSeries
from compression.line_simplification import LineSimplification
from statsmodels.tools.eval_measures import rmse
import torch


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


def main():
    file_path = 'data/mintemp.csv'
    data = pd.read_csv(file_path, index_col='Date', parse_dates=True).sort_index()
    data.Temp = data.Temp.astype(float)
    date_range = pd.date_range(start=data.index.min(), end=data.index.max(), freq='D')
    data = data.reindex(date_range)
    data = data.interpolate()

    before_target = data[:'1989-12-31']
    after_target = data['1990-01-01':]

    # Concatenate the segments in the correct order
    concatenated_data = pd.concat([before_target, before_target, before_target,
                                   before_target, before_target, before_target,
                                   before_target, before_target, before_target,
                                   before_target, before_target, before_target,
                                   before_target, before_target, before_target,
                                   before_target, before_target, before_target,
                                   before_target, before_target, before_target,
                                   before_target, before_target, before_target,
                                   before_target, before_target, before_target,
                                   before_target, before_target, before_target,
                                   before_target, before_target, before_target,
                                   before_target, before_target, before_target,
                                   after_target])
    concatenated_data.index = pd.date_range(start='1900-01-01', freq='D', periods=concatenated_data.shape[0])
    concatenated_data = concatenated_data.resample('7D').mean()
    ts = concatenated_data.values
    scaler = StandardScaler()
    X = np.squeeze(scaler.fit_transform(ts))

    acf_preservation = 54
    lookback = acf_preservation*5
    dropout = 0.0
    n_rnn_layers = 1
    hidden_fc_sizes = 64
    hidden_dim = 64
    n_epochs = 10
    x_train = X[:-lookback]
    x_test = X[-lookback:]
    x_test = scaler.inverse_transform(x_test[:, np.newaxis]).squeeze()

    model = BlockRNNModel(input_chunk_length=lookback, output_chunk_length=lookback,
                          hidden_dim=hidden_dim, n_epochs=n_epochs,
                          #hidden_fc_sizes=[hidden_fc_sizes, hidden_fc_sizes//2],
                          n_rnn_layers=n_rnn_layers, dropout=dropout, model='LSTM')
    x_train_time_series = TimeSeries.from_values(x_train)
    model.fit(x_train_time_series)
    forecast = model.predict(lookback)
    forecast = np.squeeze(forecast.values())
    forecast = scaler.inverse_transform(forecast[:, np.newaxis]).squeeze()
    rmse_raw_results = rmse(forecast, x_test)
    msmape_raw_results = msmape(forecast, x_test)
    print("RMSE", rmse_raw_results)
    print("MSMAPE", msmape_raw_results)
    
    pmc_rmse_results = [rmse_raw_results]
    pmc_msmape_results = [msmape_raw_results[0]]
    pmc_cr = [1.]

    for error in [0.4, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0, 2.5, 2.55, 2.6]:
        compressor = LineSimplification()
        compressor.set_target('pmc')
        compressed_data = compressor.compress(pts=x_train.copy(), acf_threshold=error, blocking=x_train.shape[0]//2, nlags=acf_preservation)
        print(f"Compression Ratio {error}", 2*((x_train.shape[0]*8)/len(compressed_data)), flush=True)
        pmc_cr.append(2*((x_train.shape[0]*8)/len(compressed_data)))
        decompressed_data = np.asarray(compressor.decompress(compressed_data))

        model = BlockRNNModel(input_chunk_length=lookback, output_chunk_length=lookback,
                              hidden_dim=hidden_dim, n_epochs=n_epochs,
                              n_rnn_layers=n_rnn_layers, dropout=dropout, model='LSTM')

        decompressed_time_series = TimeSeries.from_values(decompressed_data)
        model.fit(decompressed_time_series)
        forecast = model.predict(lookback)
        forecast = np.squeeze(forecast.values())
        forecast = scaler.inverse_transform(forecast[:, np.newaxis]).squeeze()

        print("RMSE", rmse(forecast, x_test))
        print("mSMAPE", msmape(forecast, x_test), flush=True)
        pmc_rmse_results.append(rmse(forecast, x_test))
        pmc_msmape_results.append(msmape(forecast, x_test)[0])

    acf_rmse_results = [rmse_raw_results]
    acf_msmape_results = [msmape_raw_results[0]]
    acf_cr = [1.]
    acf_acf_errors = [0.001, 0.005, 0.02, 0.07, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55]
    for error in acf_acf_errors:
        compressor = LineSimplification()
        compressor.set_target('sip')
        compressed_data = compressor.compress(pts=x_train.copy(), acf_threshold=error, blocking=x_train.shape[0]//2, nlags=acf_preservation)
        print("SIP Compression Ratio", x_train.shape[0]/compressed_data.shape[0], flush=True)
        acf_cr.append(x_train.shape[0]/compressed_data.shape[0])
        decompressed_data = np.interp(np.arange(x_train.shape[0]), compressed_data[:, 0], compressed_data[:, 1])


        model = BlockRNNModel(input_chunk_length=lookback, output_chunk_length=lookback,
                              hidden_dim=hidden_dim, n_epochs=n_epochs,
                              n_rnn_layers=n_rnn_layers, dropout=dropout, model='LSTM')

        decompressed_time_series = TimeSeries.from_values(decompressed_data)
        model.fit(decompressed_time_series)
        forecast = model.predict(lookback)
        forecast = np.squeeze(forecast.values())
        forecast = scaler.inverse_transform(forecast[:, np.newaxis]).squeeze()
        print()
        print("RMSE", rmse(forecast, x_test))
        print("MSMAPE", msmape(forecast, x_test))
        print()
        acf_rmse_results.append(rmse(forecast, x_test))
        acf_msmape_results.append(msmape(forecast, x_test)[0])

    area_rmse_results = [rmse_raw_results]
    area_msmape_results = [msmape_raw_results[0]]
    area_cr = [1.]
    area_acf_errors = [0.01, 0.02, 0.03, 0.05, 0.07, 0.1, 0.2, 0.5, 0.7, 0.75, 0.77]
    for error in area_acf_errors:
        compressor = LineSimplification()
        compressor.set_target('vw')
        compressed_data = compressor.compress(pts=x_train.copy(), acf_threshold=error, blocking=x_train.shape[0]//2, nlags=acf_preservation)
        print("VW Compression Ratio", x_train.shape[0]/compressed_data.shape[0], flush=True)
        area_cr.append(x_train.shape[0]/compressed_data.shape[0])
        decompressed_data = np.interp(np.arange(x_train.shape[0]), compressed_data[:, 0], compressed_data[:, 1])

        model = BlockRNNModel(input_chunk_length=lookback, output_chunk_length=lookback,
                              hidden_dim=hidden_dim, n_epochs=n_epochs,
                              #hidden_fc_sizes=[hidden_fc_sizes, hidden_fc_sizes // 2],
                              n_rnn_layers=n_rnn_layers, dropout=dropout, model='LSTM')
        decompressed_time_series = TimeSeries.from_values(decompressed_data)
        model.fit(decompressed_time_series)
        forecast = model.predict(lookback)
        forecast = np.squeeze(forecast.values())
        forecast = scaler.inverse_transform(forecast[:, np.newaxis]).squeeze()
        # Calculate MSE
        print()
        print("RMSE", rmse(forecast, x_test))
        print("MSMAPE", msmape(forecast, x_test)[0])
        print()
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
    
    os.makedirs('results/min_temp/', exist_ok=True)

    area_results.to_csv('results/min_temp/lstm_mintemp_area_results.csv')
    acf_results.to_csv('results/min_temp/lstm_mintemp_acf_results.csv')
    pmc_results.to_csv('results/min_temp/lstm_mintemp_pmc_results.csv')
    
    print('Experiments completed')


if __name__ == '__main__':
    main()
