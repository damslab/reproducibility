import copy
from data_loader import TSFReader
from forecasting.forecasting_functions import get_forecasting
from compression.factory import *

def run_forecasting_on(new_tsf, forecasting_model, forecast_horizon, compressor, error_bound):
    r = TSFReader()
    cr = list()
    compressed_list = list()
    for index, row in new_tsf.iterrows():
        print("Compressing time series", index)
        compressor_class = CompressorFactory.get_compressor(compressor)
        ts = np.asarray(row.series_value)[:-forecast_horizon].copy()
        try:
            x = compressor_class.compress(ts, error_bound, forecast_horizon)
        except IndexError as e:
            raise e

        cr.append(ts.shape[0] / x.shape[0])
        decomp_ts = compressor_class.decompress(x)

        if type(decomp_ts) is list:
            new_tsf.at[index, 'series_value'] = np.array(decomp_ts)
        else:
            new_tsf.at[index, 'series_value'] = decomp_ts

        compressed_list.append(x)

    print("Mean CR", np.mean(cr))
    # CompressorFactory.save_data(compressed_list, compressor, 'pedestrian', error_bound)
    r.convert_dataframe_to_tsf(os.path.join(compressor, f'num_coef_{error_bound}'), 'pedestrian_counts_dataset.tsf', new_tsf)
    get_forecasting('pedestrian', f'data/compressed/{compressor}/num_coef_{error_bound}', 'pedestrian', forecasting_model, False)


def compress_and_forecast(forecasting_model, compressor, error_bound):
    r = TSFReader()
    loaded_data, frequency, forecast_horizon, contain_missing_values, contain_equal_length = r.read_raw_tsf('pedestrian_counts_dataset.tsf')

    new_tsf = loaded_data.copy(deep=True)
    new_tsf['series_value'] = new_tsf['series_value'].apply(lambda x: copy.deepcopy(x))

    run_forecasting_on(new_tsf, forecasting_model, forecast_horizon, compressor, error_bound)

