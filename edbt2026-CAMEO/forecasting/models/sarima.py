from pmdarima.arima import auto_arima
import pandas as pd
import numpy as np
from pmdarima.arima import ARIMA


def get_harmonics(dti, freq='h'):
    harmonics = pd.DataFrame({'date': dti})
    harmonics['date'] = pd.PeriodIndex(harmonics['date'], freq=freq)
    harmonics.set_index('date', inplace=True)
    harmonics.sort_index(inplace=True)

    harmonics[f'sin-1har'] = np.sin(2 * np.pi * (harmonics.index.hour * 60 + harmonics.index.minute) / (24 * 60))
    # harmonics[f'sin-2har'] = np.sin(2 * np.pi * (harmonics.index.day * 60 * 24 + harmonics.index.hour * 60 + harmonics.index.minute) / (7 * 24 * 60))
    harmonics[f'cos-1har'] = np.cos(2 * np.pi * (harmonics.index.hour * 60 + harmonics.index.minute) / (24 * 60))
    # harmonics[f'cos-2har'] = np.cos(2 * np.pi * (harmonics.index.day * 60 * 24 + harmonics.index.hour * 60 + harmonics.index.minute) / (7 * 24 * 60))

    return harmonics


def do_auto_arima_on(ts, lookahead):
    # scaler = StandardScaler()
    # x_train = np.squeeze(scaler.fit_transform(ts[:, np.newaxis]))
    freq = 'h'
    train_dti = pd.date_range(start="2009-05-01", periods=ts.shape[0], freq=freq)

    print(f'Getting Harmonic')
    train_exog = get_harmonics(train_dti, freq=freq)

    auto_model = auto_arima(ts,
                       X=train_exog,
                       start_p=1,
                       max_p=5,
                       max_q=5,
                       start_q=1,
                       trace=True,
                       n_jobs=25,
                       seasonal=False,
                       error_action='warn',
                       supress_warnings=True,
                       stepwise=False,
                       n_fits=50,
                       random_state=42)

    print(auto_model.summary())

    test_dti = pd.date_range(start=train_dti[-1], periods=lookahead+1, freq=freq)
    harmonics = get_harmonics(test_dti[1:], freq=freq)
    # predictions = model.predict(lookahead, X=harmonics.values)
    # real_pred = scaler.inverse_transform(predictions[:, np.newaxis]).squeeze()
    arima_model = ARIMA(order=auto_model.order)
    arima_model.fit(ts, X=train_exog)
    predictions = arima_model.predict(lookahead, X=harmonics.values)

    return predictions, auto_model.order


def do_arima_on(ts, order, lookahead):
    # scaler = StandardScaler()
    # x_train = np.squeeze(scaler.fit_transform(ts[:, np.newaxis]))
    freq = 'h'
    train_dti = pd.date_range(start="2009-05-01", periods=ts.shape[0], freq=freq)

    print(f'Getting Harmonic')
    train_exog = get_harmonics(train_dti, freq=freq)

    model = ARIMA(order=order)
    model.fit(ts, X=train_exog)
    test_dti = pd.date_range(start=train_dti[-1], periods=lookahead+1, freq=freq)
    harmonics = get_harmonics(test_dti[1:], freq=freq)
    predictions = model.predict(lookahead, X=harmonics.values)

    # real_pred = scaler.inverse_transform(predictions[:, np.newaxis]).squeeze()

    return predictions
