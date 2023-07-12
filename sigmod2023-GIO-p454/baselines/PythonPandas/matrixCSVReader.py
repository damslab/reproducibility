import sys

import numpy as np
import pandas as pd


class readCSV(object):
    def __init__(self, data_file_name, cols):
        self.data_file_name = data_file_name
        self.cols = cols
        self.data = None
        self.__load_data()

    def __load_data(self):
        data = pd.read_csv(self.data_file_name, sep=',', header=None, usecols=self.cols, dtype=np.float64)
        self.data = pd.DataFrame(data)


if __name__ == "__main__":
    data_file_name = sys.argv[1]
    projection = sys.argv[2]
    projection_type = projection[0:1]
    cols = []
    if projection_type == "Q":  # Projection is for Queries
        if "higgs" in data_file_name:
            if projection == "Q1":
                cols = [1]
            elif projection == "Q2":
                cols = [1, 5, 10, 15, 20, 25]
    else:  # Projection for a range start from 0
        number_of_fields = projection[1:]
        cols = list(range(0, int(number_of_fields)))

    readCSV(data_file_name=data_file_name, cols=cols)
