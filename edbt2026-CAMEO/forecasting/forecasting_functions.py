from forecasting.models.sarima import do_auto_arima_on, do_arima_on
import os
import numpy as np
from scipy import stats
import pandas as pd
from sklearn.preprocessing import StandardScaler
from data_loader import TSFReader
os.environ['R_HOME'] = '/home/cmcuza/anaconda3/envs/torch_env/lib/R'
import rpy2.robjects as robjects

time_map = {'hourly': 'h', 'half_hourly': '30T'}


def standardize(ts):
    shift_value = abs(min(ts)) + 1
    tts, boxcox_lambda = stats.boxcox(ts + shift_value)
    scaler = StandardScaler()
    dtts = scaler.fit_transform(tts[:, np.newaxis]).squeeze()
    return dtts, shift_value, scaler, boxcox_lambda


def get_arima_forecasting(data_name, file_path, file_name, load_raw_model_hyper=False):
    robjects.r.assign("load_raw_model_hyper", load_raw_model_hyper)
    r_code = f"""
    BASE_DIR <- "."
    source(file.path(BASE_DIR, "forecasting", "fixed_horizon_functions.R", fsep = "/"))
    do_fixed_horizon_local_forecasting("{data_name}", "{file_path}", "arima", "{file_name}", 
    "series_name", "start_timestamp", load_raw_model_hyper)"""

    robjects.r(r_code)


def get_dhr_arima_forecasting(data_name, file_path, file_name, load_raw_model_hyper=False):
    robjects.r.assign("load_raw_model_hyper", load_raw_model_hyper)
    r_code = f"""
    BASE_DIR <- "."
    source(file.path(BASE_DIR, "forecasting", "fixed_horizon_functions.R", fsep = "/"))
    do_fixed_horizon_local_forecasting("{data_name}", "{file_path}", "dhr_arima", "{file_name}", 
    "series_name", "start_timestamp", load_raw_model_hyper)"""

    robjects.r(r_code)


def get_sarima_forecasting(data_name, file_path, file_name):
    BASE_DIR = '.'
    reader = TSFReader()
    full_file_path_and_name = os.path.join(file_path, file_name)
    split_string = file_path.split("/")[2:]

    results_folder_exec = os.path.join(BASE_DIR, "results", "fixed_horizon_execution_times")
    results_folder_error = os.path.join(BASE_DIR, "results", "fixed_horizon_errors")
    results_folder_forecasts = os.path.join(BASE_DIR, "results", "fixed_horizon_forecasts")
    results_folder_model_hyper = os.path.join(BASE_DIR, "results", "fixed_horizon_model_hyper", "raw")

    for subfolder in split_string:
        if not subfolder or subfolder == 'compressed':
            continue
        results_folder_exec = os.path.join(results_folder_exec, subfolder)
        results_folder_error = os.path.join(results_folder_error, subfolder)
        results_folder_forecasts = os.path.join(results_folder_forecasts, subfolder)

    os.makedirs(results_folder_exec, exist_ok=True)
    os.makedirs(results_folder_error, exist_ok=True)
    os.makedirs(results_folder_forecasts, exist_ok=True)
    os.makedirs(results_folder_model_hyper, exist_ok=True)

    file_path_ = os.path.join(results_folder_forecasts, f"{data_name}_sarima.txt")
    if os.path.exists(file_path_):
        os.remove(file_path_)

    forecasting_results_file_ = open(file_path_, 'w')

    print(f"Started loading {data_name}")

    loaded_data, freq, fh, mv, ce = reader.convert_tsf_to_dataframe(full_file_path_and_name)

    lookback = fh

    h_file = os.path.join(results_folder_model_hyper, f'sarima_{data_name}_hyperparameters.csv')

    all_hyperparameters = pd.DataFrame()

    if split_string[0] != 'raw':
        assert os.path.exists(h_file)
        all_hyperparameters = pd.read_csv(h_file)

    for index, row in loaded_data.iterrows():
        ts = np.asarray(row.series_value)[:-fh].copy()
        if split_string[0] == 'raw':
            prediction, order = do_auto_arima_on(ts, lookback)
        else:
            order = all_hyperparameters.loc[index]['order'].values
            prediction = do_arima_on(ts, order, lookback)
            pd.concat([all_hyperparameters, pd.DataFrame({'index': index, 'order': [order]})])

        if data_name == "pedestrian":
            prediction = np.round(prediction)

        forecast_str = f'T{index+1},' + ','.join([str(p) for p in prediction]) + '\n'
        forecasting_results_file_.write(forecast_str)
        forecasting_results_file_.flush()

    forecasting_results_file_.close()
    if split_string[0] == 'raw':
        all_hyperparameters.set_index('index', inplace=True)
        all_hyperparameters.to_csv(h_file)
        file_path = file_path.strip('./')

    r_code = f"""
                BASE_DIR = "."
                source(file.path(BASE_DIR, "forecasting", "fixed_horizon_functions.R", fsep = "/"))
                only_forecasting_metrics("{data_name}", "{file_path}", "sarima", "{file_name}")
            """

    robjects.r(r_code)


def get_stlf_arima_forecasting(data_name, file_path, file_name):
    r_code = f"""
    BASE_DIR <- "."
    source(file.path(BASE_DIR, "forecasting", "fixed_horizon_functions.R", fsep = "/"))
    do_fixed_horizon_local_forecasting("{data_name}", "{file_path}", "stlf_arima", "{file_name}")"""

    robjects.r(r_code)


def get_ets_forecasting(data_name, file_path, file_name):
    r_code = f"""
    BASE_DIR <- "."
    source(file.path(BASE_DIR, "forecasting", "fixed_horizon_functions.R", fsep = "/"))
    do_fixed_horizon_local_forecasting("{data_name}", "{file_path}", "ets", "{file_name}")"""

    robjects.r(r_code)


def get_theta_forecasting(data_name, file_path, file_name):
    r_code = f"""
    BASE_DIR <- "."
    source(file.path(BASE_DIR, "forecasting", "fixed_horizon_functions.R", fsep = "/"))
    do_fixed_horizon_local_forecasting("{data_name}", "{file_path}", "theta", "{file_name}")"""

    robjects.r(r_code)


def get_tbats_forecasting(data_name, file_path, file_name):
    r_code = f"""
    BASE_DIR <- "."
    source(file.path(BASE_DIR, "forecasting", "fixed_horizon_functions.R", fsep = "/"))
    do_fixed_horizon_local_forecasting("{data_name}", "{file_path}", "tbats", "{file_name}")"""

    robjects.r(r_code)


def get_stlf_forecasting(data_name, file_path, file_name):
    print("Correct STLF")
    r_code = f"""
    BASE_DIR <- "."
    source(file.path(BASE_DIR, "forecasting", "fixed_horizon_functions.R", fsep = "/"))
    do_fixed_horizon_local_forecasting("{data_name}", "{file_path}", "stlf", "{file_name}")"""

    robjects.r(r_code)



def get_forecasting(data_name, file_path, file_name, forecasting_model, load_raw_model_hyper=False):
    if forecasting_model == 'arima':
        get_arima_forecasting(data_name, file_path, file_name, load_raw_model_hyper)
    elif forecasting_model == 'stlf':
        get_stlf_forecasting(data_name, file_path, file_name)
    elif forecasting_model == 'stlf_arima':
        get_stlf_arima_forecasting(data_name, file_path, file_name)
    else:
        raise ValueError(f'Forecasting model {forecasting_model} is not defined')


def process_data_item_forecasting(data_item):
    data_name, forecasting_model, file_name = data_item
    print(f'Doing {data_name}')
    if forecasting_model == 'arima':
        get_arima_forecasting(data_name, './data/raw', file_name)
    elif forecasting_model == 'sarima':
        get_sarima_forecasting(data_name, './data/raw', file_name)
    elif forecasting_model == 'dhr_arima':
        get_dhr_arima_forecasting(data_name, './data/raw', file_name)
    elif forecasting_model == 'stlf_arima':
        get_stlf_arima_forecasting(data_name, './data/raw', file_name)
    elif forecasting_model == 'theta':
        get_theta_forecasting(data_name, './data/raw', file_name)
    elif forecasting_model == 'tbats':
        get_tbats_forecasting(data_name, './data/raw', file_name)
    elif forecasting_model == 'stlf':
        get_stlf_forecasting(data_name, './data/raw', file_name)
    else:
        raise ValueError(f'Forecasting model {forecasting_model} is not defined')
