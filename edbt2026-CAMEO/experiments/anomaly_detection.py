import copy
from statsmodels.tsa.stattools import acf
from anomaly_detection.matrix_profile import detect_anomalies
from compression.factory import *

def get_seasonality_length(d):
    out = []
    while d:
        k = d.pop(0)
        d = [i for i in d if i % k != 0]
        out.append(k)
    return out

def get_mean(seasonality):
    seas = seasonality[0]
    mean = [seas]
    for i in range(1, len(seasonality)):
        if seasonality[i] - seas < 5:
            mean.append(seasonality[i])
            seas = seasonality[i]
        else:
            break

    return np.round(np.mean(mean))

def acf_detector(ts):
    ts_diff = ts
    ts_diff = np.diff(ts_diff)
    lags = 500
    ac, confint, qstat, qval = acf(ts_diff, nlags=lags, qstat=True, alpha=0.01)

    raw_seasonality = []
    for i, _int in enumerate(confint):
        if _int[0] >= 0 and i > 10 and _int[1] > 0.1:
            raw_seasonality.append(i)
    seasonality = get_seasonality_length(raw_seasonality)
    seasonality_detected = True if seasonality else False
    return seasonality_detected, seasonality


def get_anomalies(df, data_name, compressor, error_bound):
    cr = list()

    for index, row in df.iterrows():
        print("Compressing time series", index)
        compressor_class = CompressorFactory.get_compressor(compressor)
        ts = row.series.copy()
        try:
            x = compressor_class.compress(ts, error_bound, row.acf, row.seq)
        except IndexError as e:
            raise e

        cr.append(ts.shape[0] / x.shape[0])
        decomp_ts = compressor_class.decompress(x)

        if type(decomp_ts) is list:
            df.at[index, 'series'] = np.array(decomp_ts)
        else:
            df.at[index, 'series'] = decomp_ts

    print("Mean CR", np.mean(cr))

    detect_anomalies(df)


def compress_and_detect_anomaly(compressor, data_path, error_bound):
    loaded_data = []
    labels = []
    starts_disc = []
    ends_disc = []
    ends_training = []
    acfs = []
    seqs = []

    for _, _, filenames in os.walk(data_path):
        if len(filenames) == 0:
            print("Download the UCR dataset first!")
            exit(0)

        for filename in filenames:
            label = filename.split('_')
            end_training = int(label[-3])
            start_disc = int(label[-2])
            end_disc = int(label[-1].replace('.txt', ''))

            full_path = os.path.join(data_path, filename)
            elements = open(full_path, 'r').readlines()
            if len(elements) < 2:
                elements = elements[0].split('  ')

            ts = [float(e) for e in elements[end_training:]]
            seq = int(1)
            seasonality_detected, seasonality = acf_detector(ts)
            if seasonality_detected:
                acf_first_seasonality = get_mean(seasonality)
            else:
                acf_first_seasonality = 24

            acf = int(acf_first_seasonality)
            loaded_data.append(np.array(copy.copy(ts)))
            labels.append(int(label[0]))
            starts_disc.append(start_disc)
            ends_disc.append(end_disc)
            ends_training.append(end_training)
            acfs.append(acf)
            seqs.append(seq)

    df = pd.DataFrame({'label': labels,
                        'series': loaded_data,
                        'start_disc': starts_disc,
                        'end_disc': ends_disc,
                        'end_training': ends_training,
                        'acf': acfs,
                        'seq': seqs})

    df = df.sort_values('label').reset_index(drop=True)
    get_anomalies(df, 'ucr_anomaly_detection_' + compressor, compressor, error_bound)