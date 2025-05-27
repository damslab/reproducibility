import numpy as np
from statsmodels.tsa.stattools import pacf
from scipy.stats import ttest_1samp, wilcoxon
from statsmodels.tsa.stattools import ccf
from statsmodels.tsa.stattools import acf



def nrmse(x, y):
    if len(x.shape) > 1:
        return nrmse_2d(x, y)
    return nrmse_1d(x, y)


def mae(x, y, axis=None):
    return np.mean(np.abs(x-y), axis=axis)


def mse(x, y):
    return np.mean((x-y)**2)


def mape(x, y):
    return np.mean(np.abs(x-y)/np.abs(x))


def smape(x, y):
    return np.mean(np.abs(x-y)/(np.abs(x)+np.abs(y))/2)


def vrage(x):
    return np.max(x) - np.min(x)


def psnr(x, y):
    return 20 * np.log10(vrage(x)) - 10 * np.log10(mse(x, y))


def nrmse_2d(x, y):
    return np.sqrt(np.mean((x-y)**2, axis=1))/(np.max(x, axis=1)-np.min(x, axis=1))


def nrmse_1d(x, y):
    return np.sqrt(mse(x, y))/vrage(x)


def all_acf_metric(raw_acf, mod_acf, prefix='acf_'):
    features = dict()

    # 1. Lag-by-Lag Difference
    features[prefix+'absolute_diff'] = np.abs(raw_acf - mod_acf)
    features[prefix+'signed_diff'] = raw_acf - mod_acf
    
    features[prefix+'mae'] = np.mean(np.abs(raw_acf - mod_acf))
    features[prefix + 'mse'] = np.mean((raw_acf - mod_acf)**2)

    # 2. Sum of Differences
    features[prefix+'sum_absolute_diff'] = np.sum(features[prefix+'absolute_diff'])
    features[prefix+'sum_signed_diff'] = np.sum(features[prefix+'signed_diff'])

    # 3. Mean and Variance of Differences
    # features['mean_diff'] = np.mean(features['signed_diff'])
    # features['variance_diff'] = np.var(features['signed_diff'])

    # 4. Peak Lags
    features[prefix+'lag_max_diff'] = np.argmax(features[prefix+'absolute_diff'])
    features[prefix+'magnitude_peak_diff'] = np.max(features[prefix+'absolute_diff'])
    features[prefix+'min_diff'] = np.min(features[prefix+'absolute_diff'])

    # 5. Cumulative Sum of Differences
    features[prefix+'cumulative_diff'] = np.cumsum(features[prefix+'absolute_diff'])

    # 6. Autocorrelation of the Difference Series
    features[prefix+'acf_diff'] = acf(features[prefix+'absolute_diff'], nlags=5)[1:]

    # 7. Area Between the Curves
    features[prefix+'area_diff'] = np.trapz(features[prefix+'absolute_diff'])

    # 8. Relative Differences
    features[prefix+'relative_absolute_diff'] = np.abs(raw_acf - mod_acf) / np.abs(raw_acf + np.finfo(float).eps)
    features[prefix+'ratio_acf'] = raw_acf / (mod_acf + np.finfo(float).eps)


    # 10. Significance of Differences
    features[prefix+'t-stest'], p_value = ttest_1samp(features[prefix+'absolute_diff'], 0)
    features[prefix+'wilcoxon'], p_value = wilcoxon(features[prefix+'absolute_diff']+np.finfo(float).eps)

    features[prefix+'curvature'] = np.diff(features[prefix+'signed_diff'], n=2)
    features[prefix+'smoothness'] = np.diff(features[prefix+'absolute_diff'], n=1)
    features[prefix+'curvature_noise'] = np.var(features[prefix+'curvature'])
    features[prefix+'mean_smoothness'] = np.mean(features[prefix+'smoothness'])

    # Lag values
    lags = np.arange(len(mod_acf))
    raw_coefficients = np.polyfit(lags, raw_acf, 2)  # 2 means second-order polynomial
    original_a, original_b, original_c = raw_coefficients
    mod_coefficients = np.polyfit(lags, mod_acf, 2)  # 2 means second-order polynomial
    mod_a, mod_b, mod_c = mod_coefficients

    features[prefix+'mod_a'] = np.abs(original_a-mod_a)
    features[prefix+'mod_b'] = np.abs(original_b - mod_b)
    features[prefix+'mod_c'] = np.abs(original_c - mod_c)

    features[prefix+'cross_corr'] = ccf(raw_acf, mod_acf, adjusted=False)

    return features


def all_pacf_metrics(raw_data, decomp_data, nlags):
    raw_pacf = pacf(raw_data, nlags=nlags)
    decomp_pacf = pacf(decomp_data, nlags=nlags)
    return all_acf_metric(raw_pacf, decomp_pacf, prefix='pacf_')


def all_metrics(x, y):
    _mape = mape(x, y)
    _mae = mae(x, y)
    _mse = mse(x, y)
    _smape = smape(x, y)
    _nrmse = nrmse_1d(x, y)
    return _mae, _mse, _smape, _mape, _nrmse


# if __name__ == "__main__":
#     # Parameters
#     n = 1000  # Number of data points (about 42 days of hourly data)
#     seasonality_period = 24  # Hourly seasonality (24 hours)
#
#     # Generate a sinusoidal time series
#     time = np.arange(n)
#     amplitude = 1
#     frequency = 1 / seasonality_period
#     sin_wave = amplitude * np.sin(2 * np.pi * frequency * time)
#
#     # Calculate ACF up to lag 24 (1 day)
#     lags = 24
#     acf_original = acf(sin_wave, nlags=lags)
#
#     # Plot the ACF
#     plt.figure(figsize=(10, 4))
#     plt.stem(range(lags + 1), acf_original)
#     plt.title('ACF of the Original Sinusoidal Time Series')
#     plt.xlabel('Lag (hours)')
#     plt.ylabel('ACF')
#     plt.show()
#
#     # Add noise to the ACF
#     noise_level = 0.1
#     acf_noisy = acf_original + noise_level * np.random.randn(len(acf_original))
#
#     # Plot the noisy ACF
#     plt.figure(figsize=(10, 4))
#     plt.stem(range(lags + 1), acf_noisy)
#     plt.title('Noisy ACF')
#     plt.xlabel('Lag (hours)')
#     plt.ylabel('ACF')
#     plt.show()
#
#     # Calculate the second difference (curvature) for the noisy ACF
#     second_diff_noisy = np.diff(acf_noisy, n=2)
#
#     # Plot the second difference (curvature)
#     plt.figure(figsize=(10, 4))
#     plt.stem(range(len(second_diff_noisy)), second_diff_noisy)
#     plt.title('Curvature of the Noisy ACF')
#     plt.xlabel('Lag (hours)')
#     plt.ylabel('Second Difference (Curvature)')
#     plt.show()
#
#
#     # Apply exponential damping to the ACF
#     damping_factor = 0.95
#     acf_damped = acf_original * damping_factor ** np.arange(len(acf_original))
#
#     # Plot the damped ACF
#     plt.figure(figsize=(10, 4))
#     plt.stem(range(lags + 1), acf_damped)
#     plt.title('Damped ACF')
#     plt.xlabel('Lag (hours)')
#     plt.ylabel('ACF')
#     plt.show()
#
#     # Calculate the second difference (curvature) for the damped ACF
#     second_diff_damped = np.diff(acf_damped, n=2)
#
#     # Plot the second difference (curvature)
#     plt.figure(figsize=(10, 4))
#     plt.stem(range(len(second_diff_damped)), second_diff_damped)
#     plt.title('Curvature of the Damped ACF')
#     plt.xlabel('Lag (hours)')
#     plt.ylabel('Second Difference (Curvature)')
#     plt.show()
#
#
#     noisy_acf_features = all_acf_metric(raw_acf=acf_original, mod_acf=acf_noisy)
#     damped_acf_features = all_acf_metric(raw_acf=acf_original, mod_acf=acf_damped)
