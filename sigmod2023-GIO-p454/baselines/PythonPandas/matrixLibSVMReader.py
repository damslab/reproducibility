import sys
import numpy as np
import pandas as pd

from sklearn.datasets import load_svmlight_file


class readLibSVM(object):
    def __init__(self, data_file_name, cols):
        self.data_file_name = data_file_name
        self.cols = cols
        self.data = None
        self.__load_data()

    def __load_data(self):
        X_train, y_train = load_svmlight_file(self.data_file_name, dtype=np.float64)
        self.data = pd.DataFrame(X_train.todense())
        self.data = self.data[self.cols]

if __name__ == "__main__":
    data_file_name = sys.argv[1]
    projection = sys.argv[2]
    projection_type = projection[0:1]
    cols = []
    if projection_type == "Q":  # Projection is for Queries
        if "susy" in data_file_name:
            if projection == "Q1":
                cols = [1]
            elif projection == "Q2":
                cols = [1, 4, 8, 12, 16]
        elif "mnist8m" in data_file_name:
            if projection == "Q1":
                cols = [1]
            elif projection == "Q2":
                cols = [1, 100, 200, 300, 400, 500]
    else:  # Projection for a range start from 0
        number_of_fields = projection[1:]
        cols = [0]
        if "mnist8m" in data_file_name:
            if number_of_fields == '0':
                cols = [0]
            else:
                cols = list(range(0, int(int(number_of_fields) * 28)))
        else:
            cols = list(range(0, int(number_of_fields)))

    readLibSVM(data_file_name=data_file_name, cols=cols)

