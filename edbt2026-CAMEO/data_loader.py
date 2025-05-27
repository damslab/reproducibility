import os
import shutil
import pandas as pd
from distutils.util import strtobool
import numpy as np
from datetime import datetime
from os.path import join as path_join


class Loader:
    data: pd.DataFrame = None
    name = 'loader'
    harmonics = dict()
    seasonality = None
    aggregation = None

    def __init__(self, split=0.8):
        self.split = split
        self.data = pd.DataFrame()

    def load(self, file_path):
        pass

    def get_all_data(self):
        return self.data.values[:, 0]

    def get_train_test_values(self):
        b = int(len(self.data)*self.split)
        train = self.data.values[:b, 0]
        test = self.data.values[b:, 0]

        return train.copy(), test.copy()

    def get_train_test_df(self):
        b = int(len(self.data)*self.split)
        train = self.data.iloc[:b]
        test = self.data.iloc[b:]

        return train.copy(), test.copy()

    def prepare_for_parquet(self):
        return self.data

    def get_train_test_ts(self):
        b = int(len(self.data)*self.split)
        train = self.data.index[:b]
        test = self.data.index[b:]

        return train.copy(), test.copy()

    def rename_to_prophet(self):
        return self.data

    def rename_to_hwes(self):
        return self.data

    def increase_size(self, n):
        self.data = self.data.loc[self.data.index.repeat(n)]

    def to_gzip(self, root_src: str, root_dst: str):
        self.prepare_for_parquet()
        df = self.data.copy()
        df['datetime'] = None
        src = path_join(root_src, self.name + '.csv.gz')
        df.to_csv(src, compression='gzip')
        dst = path_join(root_dst, self.name + '.csv.gz')
        shutil.copy(src, dst)



class DataFactory:
    def __init__(self, split=0.8):
        self.split = split
        self.loaders = {
            'hepc': HepcLoader,
            'min_temp': MinTemp,
            'pedestrian': PedestrianLoader,
            'uk_electrical_demand': UkElectricalDemand,
            'aus_electrical_demand': AusElectricalDemand,
            'humidity': HumidityLoader,
            'biotemp': IRBioTemp,
            'solar4seconds': Solar4Seconds,
            # 'ucr': UCRLoader
        }

    def load_data(self, data_name, root_path):
        if data_name not in self.loaders:
            raise Exception(f'Unknown file: {data_name}')

        loader = self.loaders[data_name](self.split)
        loader.load(root_path)

        return loader

    def create_copy(self, data_loader: Loader, interp):
        loader = self.loaders[data_loader.name](self.split)
        loader.data = data_loader.data.copy()
        b = int(self.split * len(loader.data))
        if loader.data.shape[1] > 1:
            loader.data.loc[loader.data.index[:b], 'y'] = interp
        else:
            loader.data.iloc[:b] = interp[:, np.newaxis]

        return loader


class HepcLoader(Loader):
    file_name = 'hepc.csv'
    freq = '15T'
    fs = 4./3600.
    name = 'hepc'
    seasonality = 48

    def load(self, file_path):
        self.data = pd.read_csv(path_join(file_path, self.file_name), index_col='datetime', parse_dates=True).sort_index()

    def prepare_for_parquet(self):
        self.data.rename({'Global_active_power-R': 'y'}, axis=1, inplace=True)
        self.data.reset_index(inplace=True)


class MinTemp(Loader):
    file_name = 'mintemp.csv'
    freq = 'D'
    fs = 1. / (24*3600)
    name = 'min_temp'
    seasonality = 365

    def __init__(self, split=0.7):
        super(MinTemp, self).__init__(0.7)
        self.split = 0.7

    def load(self, file_path):
        self.data = pd.read_csv(path_join(file_path, self.file_name), index_col='Date', parse_dates=True).sort_index()
        self.data.Temp = self.data.Temp.astype(float)
        date_range = pd.date_range(start=self.data.index.min(), end=self.data.index.max(), freq='D')
        self.data = self.data.reindex(date_range)
        self.data = self.data.interpolate()
        self.data[self.data.values == 0] = 0.01


class PedestrianLoader(Loader):
    file_name = 'pedestrian.csv'
    freq = 'H'
    fs = 1. / 3600
    name = 'pedestrian'
    seasonality = 24

    def load(self, file_path):
        self.data = pd.read_csv(path_join(file_path, self.file_name), index_col='ds', parse_dates=True).sort_index()
        self.data.y = self.data.y.astype(float)
        date_range = pd.date_range(start=self.data.index.min(), end=self.data.index.max(), freq='h')
        self.data = self.data.reindex(date_range)


class UkElectricalDemand(Loader):
    file_name = 'ukelecdem.csv'
    freq = '30min'
    fs = 2. / 3600.
    name = 'uk_electrical_demand'
    seasonality = 48

    def load(self, file_path):
        self.data = pd.read_csv(path_join(file_path, self.file_name))
        ts = pd.date_range(start=self.data.SETTLEMENT_DATE.iloc[0],
                           periods=self.data.shape[0],
                           freq=self.freq, tz=None)
        self.data.set_index(ts, inplace=True)
        self.data = self.data[['ND']].astype(float)


class Solar4Seconds(Loader):
    file_name = 'solarpower.csv'
    freq = '30s'
    name = 'solar4seconds'
    aggregation = 120
    seasonality = 24
    fs = 2. / 3600.

    def load(self, file_path):
        self.data = pd.read_csv(path_join(file_path, self.file_name))
        timestamp = '01/01/2019'
        ts = pd.date_range(start=pd.to_datetime(timestamp), freq=self.freq, periods=len(self.data))
        self.data.set_index(ts, inplace=True)

    def prepare_for_parquet(self):
        self.data.reset_index(inplace=True)
        self.data.rename({'index': 'datetime'}, axis=1, inplace=True)


class AusElectricalDemand(Loader):
    file_name = 'auselecdem.csv'
    freq = '30min'
    fs = 2. / 3600.
    name = 'aus_electrical_demand'
    seasonality = 7
    aggregation = 48

    def load(self, file_path):
        self.data = pd.read_csv(path_join(file_path, self.file_name))
        timestamp = '01/01/2002'
        ts = pd.date_range(start=pd.to_datetime(timestamp), freq=self.freq, periods=len(self.data))
        self.data.set_index(ts, inplace=True)

    def rename_to_prophet(self):
        # .dt.tz_localize(None)
        if 'ds' not in self.data.columns:
            self.data['cap'] = 13000
            self.data['floor'] = 3000
            self.data = self.data.reset_index().rename({'index': 'ds'}, axis=1)
        # self.data.ds = self.data.ds.tz_localize(None)
        return self.data

    def get_own_harmonics(self, K):
        harmonics = pd.DataFrame({'date': self.data.index})
        harmonics['date'] = pd.PeriodIndex(harmonics['date'], freq=self.freq)
        harmonics.set_index('date', inplace=True)
        harmonics.sort_index(inplace=True)
        for k in range(1, K+1):
            harmonics[f'sin-{k}har'] = np.sin(
                k * 2 * np.pi * (harmonics.index.hour * 60 + harmonics.index.minute) / (24 * 60))
            harmonics[f'cos-{k}har'] = np.cos(
                k * 2 * np.pi * (harmonics.index.hour * 60 + harmonics.index.minute) / (24 * 60))

        return harmonics

    def prepare_for_parquet(self):
        self.data.reset_index(inplace=True)
        self.data.rename({'index': 'datetime'}, axis=1, inplace=True)


class IRBioTemp(Loader):
    file_name = 'irbiotemp.csv'
    freq = '1T'
    fs = 1 / 60.
    name = 'biotemp'
    seasonality = 24
    aggregation = 60

    def load(self, file_path):
        self.data = pd.read_csv(path_join(file_path, self.file_name))
        timestamp = '01/01/2016'
        ts = pd.date_range(start=pd.to_datetime(timestamp), freq=self.freq, periods=len(self.data))
        self.data.set_index(ts, inplace=True)

    def prepare_for_parquet(self):
        self.data.reset_index(inplace=True)
        self.data.rename({'index': 'datetime'}, axis=1, inplace=True)


class HumidityLoader(Loader):
    file_name = 'humidity.csv'
    freq = '1min'
    fs = 1 / 60.
    name = 'humidity'
    seasonality = 24
    aggregation = 60

    def load(self, file_path):
        self.data = pd.read_csv(path_join(file_path, self.file_name))
        timestamp = '01/01/2016'
        ts = pd.date_range(start=pd.to_datetime(timestamp), freq=self.freq, periods=len(self.data))
        self.data.set_index(ts, inplace=True)

    def prepare_for_parquet(self):
        self.data.reset_index(inplace=True)
        self.data.rename({'index': 'datetime'}, axis=1, inplace=True)


class UCRLoader(Loader):
    file_name = 'UCR_anomaly_with_acf'

    def load(self, file_path):
        compiled_ucr_path = os.path.join('data', 'ucr.parquet')
        if os.path.exists(compiled_ucr_path):
            self.data = pd.read_parquet(compiled_ucr_path)
        else:
            ucr_path = os.path.join(file_path, self.file_name)
            loaded_data = []
            labels = []
            starts_disc = []
            ends_disc = []
            ends_training = []
            acfs = []
            for _, _, filenames in os.walk(ucr_path):
                for filename in filenames:
                    label = filename.split('_')
                    print(label)
                    acf = int(label[-4].split('.')[0])
                    end_training = int(label[-3])
                    start_disc = int(label[-2])
                    end_disc = int(label[-1].replace('.txt', ''))

                    full_path = os.path.join(ucr_path, filename)
                    elements = open(full_path, 'r').readlines()
                    if len(elements) < 2:
                        elements = elements[0].split('  ')

                    ts = [float(e) for e in elements[end_training:]]

                    loaded_data.append(np.array(ts))
                    labels.append(int(label[0]))
                    starts_disc.append(start_disc)
                    ends_disc.append(end_disc)
                    ends_training.append(end_training)
                    acfs.append(acf)

            new_tsf = pd.DataFrame({'label': labels,
                                    'series': loaded_data,
                                    'start_disc': starts_disc,
                                    'end_disc': ends_disc,
                                    'end_training': ends_training,
                                    'acf': acfs})

            self.data = new_tsf.sort_values('label').reset_index(drop=True)
            self.data.to_parquet(compiled_ucr_path)


class TSFReader:
    raw_root_file = os.path.join('data')
    compressed_root_file = os.path.join('data', 'compressed')

    def convert_tsf_to_dataframe(self, full_file_path_and_name, replace_missing_vals_with="NaN", value_column_name="series_value"):
        col_names = []
        col_types = []
        all_data = {}
        line_count = 0
        frequency = None
        forecast_horizon = None
        contain_missing_values = None
        contain_equal_length = None
        found_data_tag = False
        found_data_section = False
        started_reading_data_section = False

        with open(full_file_path_and_name, "r", encoding="cp1252") as file:
            for line in file:
                # Strip white space from start/end of line
                line = line.strip()

                if line:
                    if line.startswith("@"):  # Read meta-data
                        if not line.startswith("@data"):
                            line_content = line.split(" ")
                            if line.startswith("@attribute"):
                                if (
                                        len(line_content) != 3
                                ):  # Attributes have both name and type
                                    raise Exception("Invalid meta-data specification.")

                                col_names.append(line_content[1])
                                col_types.append(line_content[2])
                            else:
                                if (
                                        len(line_content) != 2
                                ):  # Other meta-data have only values
                                    raise Exception("Invalid meta-data specification.")

                                if line.startswith("@frequency"):
                                    frequency = line_content[1]
                                elif line.startswith("@horizon"):
                                    forecast_horizon = int(line_content[1])
                                elif line.startswith("@missing"):
                                    contain_missing_values = bool(
                                        strtobool(line_content[1])
                                    )
                                elif line.startswith("@equallength"):
                                    contain_equal_length = bool(strtobool(line_content[1]))

                        else:
                            if len(col_names) == 0:
                                raise Exception(
                                    "Missing attribute section. Attribute section must come before data."
                                )

                            found_data_tag = True
                    elif not line.startswith("#"):
                        if len(col_names) == 0:
                            raise Exception(
                                "Missing attribute section. Attribute section must come before data."
                            )
                        elif not found_data_tag:
                            raise Exception("Missing @data tag.")
                        else:
                            if not started_reading_data_section:
                                started_reading_data_section = True
                                found_data_section = True
                                all_series = []

                                for col in col_names:
                                    all_data[col] = []

                            full_info = line.split(":")

                            if len(full_info) != (len(col_names) + 1):
                                raise Exception("Missing attributes/values in series.")

                            series = full_info[len(full_info) - 1]
                            series = series.split(",")

                            if len(series) == 0:
                                raise Exception(
                                    "A given series should contains a set of comma separated numeric values. "
                                    "At least one numeric value should be there in a series. "
                                    "Missing values should be indicated with ? symbol"
                                )

                            numeric_series = []

                            for val in series:
                                if val == "?":
                                    numeric_series.append(replace_missing_vals_with)
                                else:
                                    numeric_series.append(float(val))

                            if numeric_series.count(replace_missing_vals_with) == len(
                                    numeric_series
                            ):
                                raise Exception(
                                    "All series values are missing. A given series should contains a set of comma "
                                    "separated numeric values. At least one numeric value should be there in a series."
                                )

                            all_series.append(np.asarray(numeric_series))

                            for i in range(len(col_names)):
                                att_val = None
                                if col_types[i] == "numeric":
                                    att_val = int(full_info[i])
                                elif col_types[i] == "string":
                                    att_val = str(full_info[i])
                                elif col_types[i] == "date":
                                    att_val = datetime.strptime(
                                        full_info[i], "%Y-%m-%d %H-%M-%S"
                                    )
                                else:
                                    raise Exception(
                                        "Invalid attribute type."
                                    )  # Currently, the code supports only numeric, string
                                    # and date types. Extend this as required.

                                if att_val is None:
                                    raise Exception("Invalid attribute value.")
                                else:
                                    all_data[col_names[i]].append(att_val)

                    line_count = line_count + 1

            if line_count == 0:
                raise Exception("Empty file.")
            if len(col_names) == 0:
                raise Exception("Missing attribute section.")
            if not found_data_section:
                raise Exception("Missing series information under data section.")

            all_data[value_column_name] = all_series
            loaded_data = pd.DataFrame(all_data)

            return (
                loaded_data,
                frequency,
                forecast_horizon,
                contain_missing_values,
                contain_equal_length,
            )

    def read_raw_tsf(self, file_name):
        full_file_path_and_name = os.path.join(self.raw_root_file, file_name)
        return self.convert_tsf_to_dataframe(full_file_path_and_name)

    def convert_dataframe_to_tsf(self, root_path, file_name, data_frame):
        full_file_path_and_name = os.path.join(self.raw_root_file, file_name)
        new_file_path_name = os.path.join(self.compressed_root_file, root_path, file_name)
        new_tsf = ""
        data_flag = False
        i = 0
        np.set_printoptions(suppress=True)
        with open(full_file_path_and_name, "r", encoding="cp1252") as file:
            for line in file:
                # Strip white space from start/end of line
                line = line.strip()

                if data_flag:
                    full_info = line.split(":")
                    new_series = ''
                    for element in data_frame.series_value[i]:
                        if file_name.find('pedestrian') != -1:
                            new_series += str(round(element)) + ','
                        else:
                            new_series += '{:10.5f}'.format(element) + ','
                    new_tsf += ':'.join(full_info[:-1]) + ':' + new_series[:-1] + '\n'
                    i += 1
                else:
                    if line.startswith("@data"):
                        data_flag = True

                    new_tsf += line + '\n'

        os.makedirs(os.path.join(self.compressed_root_file, root_path), exist_ok=True)
        with open(new_file_path_name, "w", encoding="cp1252") as file:
            file.write(new_tsf)

